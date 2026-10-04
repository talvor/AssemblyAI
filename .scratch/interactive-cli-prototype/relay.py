#!/usr/bin/env python3
"""THROWAWAY local PTY relay. Not a production supervisor or security boundary.

serve SOCKET -- COMMAND...; attach SOCKET; rpc SOCKET JSON
Ctrl-] detaches. Detaching leaves automation paused until an explicit release.
Only the attach connection may send human input. Socket is private to this user.
"""
import base64
import fcntl
import json
import os
import pty
import re
import select
import signal
import socket
import struct
import sys
import termios
import time
import tty
from pathlib import Path


def packet(conn, value):
    conn.sendall(json.dumps(value).encode() + b'\n')


def serve(path, command):
    os.umask(0o077)
    listener = socket.socket(socket.AF_UNIX)
    listener.bind(path)  # Refuse stale or occupied socket; never steal a session.
    listener.listen()
    child, master = pty.fork()
    if child == 0:
        os.execvp(command[0], command)
    fcntl.ioctl(master, termios.TIOCSWINSZ, struct.pack('HHHH', 30, 110, 0, 0))
    clients, buffers = set(), {}
    owner, human, epoch = 'automation', None, 0
    history = bytearray()
    alive, exit_status = True, None
    log = open(path + '.events.jsonl', 'a', buffering=1)

    def event(kind, **fields):
        log.write(json.dumps(dict(time=time.time(), kind=kind, epoch=epoch, **fields)) + '\n')

    def drop(conn):
        nonlocal owner, human
        if conn is human:
            owner, human = 'paused', None
            event('human_disconnected', owner=owner)
        clients.discard(conn)
        buffers.pop(conn, None)
        conn.close()

    event('started', pid=child, command=command)
    print(json.dumps(dict(socket=path, pid=child)), flush=True)
    try:
        while True:
            ready, _, _ = select.select([listener, *clients] + ([master] if alive else []), [], [], .2)
            for source in ready:
                if source is listener:
                    conn, _ = listener.accept()
                    clients.add(conn)
                    buffers[conn] = b''
                elif source == master:
                    try:
                        data = os.read(master, 65536)
                    except OSError:
                        data = b''
                    if not data:
                        alive = False
                        _, exit_status = os.waitpid(child, 0)
                        event('process_exited', wait_status=exit_status, assignment='unaccepted')
                    else:
                        history.extend(data)
                        if human:
                            try:
                                packet(human, {'output': base64.b64encode(data).decode()})
                            except OSError:
                                drop(human)
                else:
                    try:
                        data = source.recv(65536)
                        if not data:
                            drop(source)
                            continue
                        buffers[source] += data
                        while b'\n' in buffers[source]:
                            line, buffers[source] = buffers[source].split(b'\n', 1)
                            req = json.loads(line)
                            op = req['op']
                            reply = {'ok': True}
                            if op == 'status':
                                reply.update(owner=owner, epoch=epoch, alive=alive, exit_status=exit_status, assignment='unaccepted')
                            elif op == 'read':
                                offset = max(0, int(req.get('offset', 0)))
                                reply.update(output=base64.b64encode(history[offset:]).decode(), offset=len(history))
                            elif op == 'attach' and human is None:
                                epoch += 1
                                owner, human = 'human', source
                                rows, cols = req.get('size', [30, 110])
                                if alive:
                                    fcntl.ioctl(master, termios.TIOCSWINSZ, struct.pack('HHHH', rows, cols, 0, 0))
                                event('human_attached', owner=owner)
                                reply.update(output=base64.b64encode(history).decode(), epoch=epoch)
                            elif op == 'input' and alive and ((source is human and owner == 'human') or (owner == 'automation' and req.get('epoch') == epoch)):
                                raw = base64.b64decode(req['data'])
                                os.write(master, raw)
                                event('input', actor=owner, bytes=len(raw))
                            elif op == 'release' and owner == 'paused' and req.get('summary', '').strip():
                                epoch += 1
                                owner = 'automation'
                                event('intervention_released', summary=req['summary'], owner=owner)
                            elif op == 'close' and not alive:
                                packet(source, reply)
                                return
                            else:
                                reply = {'ok': False, 'reason': 'input ownership, epoch, process state, or operation rejected'}
                                event('rejected', operation=op, owner=owner)
                            packet(source, reply)
                    except (OSError, ValueError, KeyError):
                        drop(source)
    finally:
        for conn in list(clients):
            drop(conn)
        listener.close()
        os.close(master)
        if alive:
            os.kill(child, signal.SIGHUP)
        Path(path).unlink(missing_ok=True)
        log.close()


def connect(path):
    conn = socket.socket(socket.AF_UNIX)
    conn.connect(path)
    return conn


def attach(path):
    conn = connect(path)
    old = termios.tcgetattr(sys.stdin)
    size = os.get_terminal_size()
    packet(conn, {'op': 'attach', 'size': [size.lines, size.columns]})
    pending = b''
    keys = b''
    try:
        tty.setraw(sys.stdin)
        while True:
            ready, _, _ = select.select([conn, sys.stdin], [], [])
            if conn in ready:
                data = conn.recv(65536)
                if not data:
                    return
                pending += data
                while b'\n' in pending:
                    line, pending = pending.split(b'\n', 1)
                    result = json.loads(line)
                    if result.get('ok') is False:
                        os.write(1, ('\r\n' + str(result) + '\r\n').encode())
                        return
                    if 'output' in result:
                        os.write(1, base64.b64decode(result['output']))
            if sys.stdin in ready:
                data = os.read(sys.stdin.fileno(), 4096)
                keys += data
                # Kitty/CSI-u and xterm modifyOtherKeys encode Ctrl-] instead
                # of sending byte 0x1d. Native CLIs enable these modes.
                if (b'\x1d' in keys or re.search(rb'\x1b\[(?:93;5(?::[123])?u|29u|27;5;93~)', keys)):
                    return
                # Retain an incomplete escape sequence across socket reads.
                last_escape = keys.rfind(b'\x1b')
                if last_escape >= 0 and re.fullmatch(rb'\x1b(?:\[[0-9;:]*)?', keys[last_escape:]):
                    data, keys = keys[:last_escape], keys[last_escape:]
                else:
                    data, keys = keys, b''
                if data:
                    packet(conn, {'op': 'input', 'data': base64.b64encode(data).decode()})
    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old)
        conn.close()
        print('\033[<u\033[>4;0m\033[?1000l\033[?1002l\033[?1003l\033[?1006l\033[?2004l\033[?1004l\033[?1049l\033[?25h\nDetached; automation remains paused. Record your intervention before release.')


if __name__ == '__main__':
    mode, path = sys.argv[1:3]
    if mode == 'serve':
        assert sys.argv[3] == '--'
        serve(path, sys.argv[4:])
    elif mode == 'attach':
        attach(path)
    elif mode == 'rpc':
        conn = connect(path)
        packet(conn, json.loads(sys.argv[3]))
        print(conn.makefile('r').readline(), end='')
        conn.close()
