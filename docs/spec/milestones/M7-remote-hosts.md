# M7 Remote hosts

M7 makes a factory on a remote host as usable as a local one: `--host`, Lavish through SSH port forwarding, and plain `ssh -t host asmai`. It runs on the virtual machine Phillip sets up for it ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27)).

## What it adds

1. **`--host <ssh-destination>`** and `ASMAI_HOST`, running any command on a remote host through the user's SSH configuration, and forwarding the remote Lavish port for the conversation and attach ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27), [09](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/09-cli-and-configuration.md), [04](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/04-conversation-and-lavish.md)).
2. **Plain `ssh -t host asmai`** working too, with no registry of hosts and no combined view across them ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27), [09](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/09-cli-and-configuration.md)).
3. **The remote host for S9:** a virtual machine Phillip sets up now, on this host or elsewhere; setting it up blocked nothing before M7 ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27), [11](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/11-qualification-and-proving.md)).
4. **Ghostty over SSH,** qualified alongside C47 ([11](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/11-qualification-and-proving.md)).

## Builds on

[M6 Recovery](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/milestones/M6-recovery.md): disconnects, crashes and reboots recovered, which S9 repeats on a remote host.

## Rules delivered

Where a rule arrives in parts, the table names the part this milestone delivers.

**[04 Conversation and Lavish](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/04-conversation-and-lavish.md)**

| Rule | | Part delivered here |
| --- | --- | --- |
| 21 | Local only | --host forwarding |

**[09 CLI and configuration](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/09-cli-and-configuration.md)**

| Rule | | Part delivered here |
| --- | --- | --- |
| 18 | `--host` | All |
| 19 | Plain SSH works too | All |
| 20 | No host registry | All |
| 35 | Variables AsmAI reads or sets | ASMAI_HOST |

**[11 Qualification and proving](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/11-qualification-and-proving.md)**

| Rule | | Part delivered here |
| --- | --- | --- |
| 17 | Terminals | Ghostty over SSH |
| 31 | The remote host for S9 | All |

## Qualification cases

This passes in the harness on Linux at M7's end and has run on the Mac ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27), [11](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/11-qualification-and-proving.md)):

| Case | What is qualified |
| --- | --- |
| C47 | Remote use over SSH: `--host`, Lavish through port forwarding, and plain `ssh -t host asmai` |

## Demo path

S9, remote continuity, on the virtual machine with the fixture repository ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27), [11](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/11-qualification-and-proving.md)): a job on the remote host driven with `asmai --host`. SSH drops mid-turn and delivery keeps running; the user reconnects and answers a Lavish decision through the forwarded port; and the remote host reboots with the service installed. S8's evidence holds for the remote host, and the job ends as a tested pull request.

## Exit checks

M7 ends when ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27)):

- its tickets are closed;
- the development tests are green on Linux and on macOS;
- C47 passes in the harness on Linux and has run on the Mac; a macOS failure becomes a ticket in M8 and does not hold up M7;
- its demo path has run once on the fixture repository from the remote host, with the terminal recording kept for Phillip to watch.

## Not in M7

Releases, the install script, upgrades, store migrations and the enforced qualification record (M8).

## Sources

- [Choose the specification's structure and implementation sequence](https://github.com/talvor/AssemblyAI/issues/27#issuecomment-6004852593) (AssemblyAI#27)
- The component documents linked in Rules delivered, and the decision tickets they cite.
- The review of this document: [board](https://github.com/talvor/AssemblyAI/blob/main/.lavish/spec-doc-M7.html) and [answers](https://github.com/talvor/AssemblyAI/blob/main/.lavish/spec-doc-M7-answers.json).
