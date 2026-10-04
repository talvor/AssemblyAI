# THROWAWAY: interactive CLI feasibility probe

This is a captured planning experiment, not AsmAI implementation or a production supervisor.
The canonical human decision lives in [Validate interactive CLI coordination and intervention](https://github.com/talvor/AssemblyAI/issues/19).

## What is here

- `relay.py`: a same-user Unix-socket/PTY relay, direct terminal attachment, input ownership epochs, pause on detach and explicit release with an intervention summary.
- `observe_hook.py`: passive native lifecycle recorder; never makes permission decisions.
- `launch_hooks.py` and provider settings: exact observed hook configurations. Codex required live human hook review; Claude used explicit hook settings after a safe-mode smoke test.
- `accept_recall.py`: bounded owner acceptance of this experiment's expected session, current dispatch, assignment ID and human-selected label. A stopped turn alone is insufficient.
- `*-hooks.jsonl`: actual passive events. `human-decisions.json` records submitted choices and a marked summary of the intervention report.
- `evidence.json`: observations and qualification limits.
- `relay-transitions.json`: selected attach/detach, rejection, release and exit events; keyboard content was never logged.
- `codex-lifecycle-excerpts.json`: scoped native turn events supporting the cancellation interpretation.

## Reproduction shape

Requires the user's existing native subscription login on the execution host. Never copy credentials or invoke login from this harness. Versions observed: Codex 0.157.0 (GPT-6-Astra) and Claude Code 2.1.283 (Opus 5.5), local Linux.

For a fresh run, launch new interactive conversations in a disposable directory, record their native session IDs, and update the session IDs and expected assignment contract in the captured scripts. The hardcoded IDs refer to this experiment, not portable fixtures. Regenerate hook command paths for the checkout location. Review hook trust natively.

A server can be started in a supervised foreground terminal with:

    python3 relay.py serve /private/path/probe.sock -- codex --no-daemon --no-alt-screen -s read-only -a on-request

Attach from another terminal:

    python3 relay.py attach /private/path/probe.sock

Ctrl-] detaches, including observed extended keyboard modes. Reattach preserves the provider process. `rpc SOCKET JSON` exposes status, read, input, release and close operations. Automated input requires the current epoch; human input is bound to its attach connection. Release requires a summary and a paused session. Close requires the provider process to have exited. Do not enter real credentials into the test conversation.

## Deliberate limits and findings

The relay is a disposable single-process mechanism, not a security boundary against the same user or an agent with equivalent host access. It has no durable journal recovery, bounded backpressure, complete terminal emulation, remote transport, resize handling after attach, input acknowledgments, or exactly-once delivery. Replay of raw terminal history is not a robust screen reconstruction. It does not enforce the full subscription/fallback policy; that is a confirmed contract for the future adapter, not code implemented here.

A partial automatic prompt survived a human ownership change. Production must reconcile drafts and in-flight work before releasing input; a writer lock alone is insufficient. Full mid-generation takeover was not qualified.

The first detach implementation missed extended keyboard encoding. The client was disconnected without ending Codex, patched, and Phillip confirmed the shortcut in both clients. A stale-result bug in the first acceptance probe was corrected to invalidate an older Stop after a new dispatch; interrupted probes remained unaccepted afterward.

Claude allowed the harmless sleep command despite manual permission mode. Its Write request produced PermissionRequest; canceling it produced an error tool result, not an observed Interrupt hook. Codex produced PermissionRequest and Interrupt. Native screen text said Ran after human cancellation; the sentinel files were absent and native Codex turn events were aborted. Do not classify execution from screen labels.

Missing, conflicting or stale evidence must leave affected work unknown/paused pending reconciliation. Actual access exhaustion, revoked login, fallback, adverse hook delivery, host crashes, remote hosts and other platforms were not tested. Neither version/configuration is launch-certified by this experiment.

## Documentation consulted

- https://learn.chatgpt.com/docs/hooks
- https://code.claude.com/docs/en/hooks

Documentation informed candidate events; the JSONL files show what this run actually observed.

## Late modal-interception finding

Claude acknowledged the final adapter decision. Codex did not: a native rate-limit/model-switch dialog intercepted the automated message. The visible selection retained the current model and selected never show again; the relay may have changed that reminder preference. No provider or model switch was observed. This demonstrates that successful PTY writes are not dispatch acceptance. Production requires positive submission correlation and known input readiness; unknown modal states must pause for human reconciliation.

The resulting `hide_rate_limit_model_nudge = true` preference was confirmed and restored to `false` with user approval, preserving visible reminders. No model or auth setting was changed.
