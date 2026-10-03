# Agent runtimes and persistent sessions

Research snapshot: 2026-10-03. This answers feasibility and boundaries, not runtime selection. No agents or services were launched. Local inspection found Codex at `/home/phillip/.nix-profile/bin/codex`, reporting `codex-cli 0.157.0`; no relevant product runtime implementation was found in the workspace. Only non-secret config keys were inspected. Current online documentation can describe capabilities newer than this installed binary; pin versions and verify adapters before implementation.

## Supported integration surfaces

| Surface | Session and completion contract | Hosting implications |
| --- | --- | --- |
| Codex non-interactive CLI | `codex exec --json` emits JSONL including thread start, turn completion/failure and item events. Resume is documented. | A subprocess suitable for jobs; persist structured events and identity rather than scraping terminal output. [Official non-interactive guide](https://learn.chatgpt.com/docs/non-interactive-mode) |
| Codex SDK | TypeScript starts, continues and resumes local threads; Python drives local app-server and published builds pin a runtime dependency. | Server-side/local process integration; can run on a remote machine you operate. “Local” identifies the execution host, not necessarily the user's laptop. [Official SDK guide](https://learn.chatgpt.com/docs/codex-sdk) |
| Codex app-server | JSON-RPC exposes start/resume/fork, turn start/steer/interrupt, approvals and events. `turn/completed` distinguishes completed, interrupted and failed. | Stdio is the default. Remote WebSocket/terminal access exists, but the page explicitly marks WebSocket experimental and unsupported for production. Remote exposure requires authentication and TLS or an SSH tunnel. Generate schemas from the selected installed version. [Official app-server guide](https://learn.chatgpt.com/docs/app-server) |
| Claude Agent SDK | Python/TypeScript embed Claude Code's agent loop, permissions, hooks and sessions; custom subagents are supported. | Operate its process locally or on infrastructure you control. It is distinct from the raw model client SDK. [Official SDK overview](https://code.claude.com/docs/en/agent-sdk/overview) |
| Claude non-interactive CLI | `claude -p` supports JSON output and resume; exit status separates successful and failed runs. SIGTERM may leave an unfinished turn without a result. | A scriptable subprocess. Its own background task behavior is bounded and version-dependent; do not treat it as a permanent factory supervisor. [Official headless guide](https://code.claude.com/docs/en/headless) |

Claude SDK subagents have their own context and can use specialized instructions/tools. They can be declared programmatically; the parent receives a final result. This supports research/test/implementation workers, but does not itself define durable factory roles. [Subagents](https://code.claude.com/docs/en/agent-sdk/subagents)

For Codex, the official Sign in with ChatGPT preview documentation explicitly supports local child-agent coordination through function/custom tools. This is distinct from a hosted `multi_agent` Responses parameter, which that preview does not accept. A factory can also schedule distinct SDK threads as its own workers; that is an architectural inference, not a documented singleton-role service. [Preview limitations](https://developers.openai.com/siwc/token-sharing-open-source/preview-limitations)

Managed hosting is another category: OpenAI's Agents API documents a hosted Codex harness with hosted or self-hosted execution environments; with self-hosting, your application owns provisioning, reconnects, shutdown and preserved files. Anthropic's SDK overview points to Managed Agents with hosted or self-hosted sandboxes. These are alternatives to supervising local CLI processes, not evidence that a consumer CLI subscription includes managed hosting. Access, cost and maturity need a separate check if selected. [OpenAI architecture](https://developers.openai.com/api/docs/guides/agents-api/architecture), [Claude overview](https://code.claude.com/docs/en/agent-sdk/overview)

## Four different kinds of persistence

1. **Conversation:** preserve provider thread/session identity and transcript storage. Claude explicitly says sessions preserve conversations, not files; a `SessionStore` adapter can mirror transcripts across hosts. Forking a session does not isolate the working tree. [Claude sessions](https://code.claude.com/docs/en/agent-sdk/sessions)
2. **Process:** tmux lets a terminal client detach while programs continue. It is useful for human inspection and SSH disconnects. It does not establish an application-level restart/reconciliation contract. [tmux getting started](https://github.com/tmux/tmux/wiki/Getting-Started)
3. **Service:** a supervisor can restart failed processes; systemd documents restart and watchdog policies. Restarting a process is not proof that an interrupted tool operation is safe to repeat. [systemd service specification](https://github.com/systemd/systemd/blob/main/man/systemd.service.xml)
4. **Factory task:** application-owned durable state must identify assignment, attempt, worker session, workspace, accepted result and unresolved side effects. This is a design inference from the separation above. A transcript is insufficient evidence that a PR was opened once, a test ran against the final commit, or a task result reached its coordinator.

Browser closure, SSH detachment, agent crash, and host reboot therefore need different acceptance tests. Claude Remote Control explicitly keeps computation on the host, requires its process to remain alive and suggests tmux/screen for SSH detachment. A remote browser is a control surface, not the execution host. [Remote Control](https://code.claude.com/docs/en/remote-control)

A robust completion record should distinguish **agent turn ended**, **worker task produced a result**, and **factory accepted that result against the required tests/commit**. That three-level distinction is proposed vocabulary, not a provider guarantee. On reconnect, reconcile durable state and existing effects before retrying; missing events should produce an unknown/reconciling state, not automatic success.

## Authentication constraints

Codex documents ChatGPT subscription sign-in and usage-billed API keys for local clients; cloud requires ChatGPT sign-in. Its authentication page recommends API keys for programmatic CLI workflows and also describes enterprise access tokens for trusted automation. Account/workspace controls still apply. This research does not establish the user's plan or entitlements. [Codex authentication](https://learn.chatgpt.com/docs/auth)

OpenAI separately documents a Sign in with ChatGPT preview for app-server integrations, with specific token renewal and transport limitations. Do not generalize it into unrestricted subscription-backed API access. [App-server plan integration](https://developers.openai.com/siwc/token-sharing-open-source/codex-app-server), [Preview limitations](https://developers.openai.com/siwc/token-sharing-open-source/preview-limitations)

Anthropic says third-party developers may not offer claude.ai login or rate limits for products without prior approval; the SDK overview directs them to API-key authentication. This is a distribution constraint even if the first customer is Phillip. Claude CLI bare mode does not use subscription login. Personal use of the standard CLI and shipping a subscription-backed third-party product must be assessed separately. [SDK overview](https://code.claude.com/docs/en/agent-sdk/overview), [Headless authentication](https://code.claude.com/docs/en/headless)

## Exactly one leader per role

Treat this as an authority invariant, not “one terminal window” or “one named tmux session.” Proposed precise wording: **at most one owner may authorize work for each (factory, role) at any instant; a healthy factory eventually restores one owner after failure.** Continuous exactly-one availability cannot be promised through all crash/failover intervals.

An implementation must define atomic acquisition, ownership loss, takeover, and rejection of stale owners. Lease expiry alone is insufficient if a paused old process resumes and can still mutate external systems; use fencing/conditional acceptance at the mutation boundary or explicitly limit failover. Exactly-once effects are a separate property from single leadership. These are design requirements/inferences, not a selection of storage technology. etcd's primary documentation illustrates atomic transactions, revisions and expiring leases as available primitives; it is not a recommendation to deploy etcd. [etcd API](https://etcd.io/docs/v3.6/learning/api/)

Clarify whether the leader is per factory, repository or project, and whether a role may have parallel workers underneath its one leader. A process supervisor and provider session API do not independently enforce this product invariant.

## Remaining decisions and validation boundary

- Choose initial provider adapters and whether both must work at launch.
- Choose self-operated local/remote execution versus managed harnesses; decide supported OS and remote connectivity.
- Define detach, stop, crash recovery, reboot recovery and host migration separately.
- Define leadership scope and whether automatic takeover is required in v1.
- Define durable task/result acceptance, retry policy and workspace isolation.
- Decide whether API-key billing is acceptable; investigate distribution authorization if subscription-backed operation is required.

No integration, entitlement, concurrency, reconnect or crash test was performed. No runtime was selected. Before committing to one, a focused prototype should test structured completion, approval pauses, disconnect/reconnect, crash during a side effect, duplicate dispatch and stale-leader rejection against pinned versions.
