# 03 Provider sessions and terminals

This document specifies how agents run: AsmAI's pinned provider copies and the settings passed to each session, the daemon-owned terminals and hook intake, the input fence and positive submission acknowledgment, the allow-list of qualified modals, the attach client and its status line, taking and releasing an agent and the intervention record, and terminal recordings. [02 Daemon and store](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/02-daemon-and-store.md) specifies what the daemon does with the observations and dispatches described here; [04 Conversation and Lavish](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/04-conversation-and-lavish.md) specifies the conversation, which is not an intervention.

## Rules

### Pinned provider copies

1. **Never the user's copies.** Agents and the Lavish server run AsmAI's own pinned, qualified copies of Claude Code, Codex and Lavish, never the user's personal installations, so the user's copies can keep updating freely ([AssemblyAI#9](https://github.com/talvor/AssemblyAI/issues/9), [ADR 0003](https://github.com/talvor/AssemblyAI/blob/main/docs/adr/0003-go-executable-runs-pinned-providers.md)).
2. **Installed on the user's command.** `asmai providers install` fetches the pinned Claude Code and Codex from their official channels, and the pinned Lavish build from talvor/asmai (rule 3), after the user confirms; AsmAI never redistributes Claude Code or Codex. The pinned versions of all three live in one committed pins file in talvor/asmai, which each release embeds. `asmai providers list` shows what is installed ([AssemblyAI#9](https://github.com/talvor/AssemblyAI/issues/9), [AssemblyAI#20](https://github.com/talvor/AssemblyAI/issues/20), [ADR 0010](https://github.com/talvor/AssemblyAI/blob/main/docs/adr/0010-lavish-is-a-deno-compiled-executable-built-per-pin.md), [answers](https://github.com/talvor/AssemblyAI/blob/main/.lavish/lavish-delivery-answers.json)). [10](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/10-release-install-and-upgrade.md) specifies how new pins arrive with an upgrade.
3. **Lavish needs no Node.** AsmAI's Lavish is one executable per certified platform, compiled with deno compile from the pinned lavish-axi release and its locked dependencies, so the host needs no Node. It is built only when the pinned lavish-axi or Deno version changes, as a Lavish build that every release keeping that pin reuses ([ADR 0010](https://github.com/talvor/AssemblyAI/blob/main/docs/adr/0010-lavish-is-a-deno-compiled-executable-built-per-pin.md), [answers](https://github.com/talvor/AssemblyAI/blob/main/.lavish/lavish-delivery-answers.json), [10](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/10-release-install-and-upgrade.md)).
4. **Only qualified combinations run.** The daemon checks the provider versions at start and refuses any combination outside the release's qualification record before any dispatch, with an actionable message ([AssemblyAI#7](https://github.com/talvor/AssemblyAI/issues/7), [AssemblyAI#15](https://github.com/talvor/AssemblyAI/issues/15), [AssemblyAI#12](https://github.com/talvor/AssemblyAI/issues/12)). A development build may start an unqualified combination and says so ([ADR 0009](https://github.com/talvor/AssemblyAI/blob/main/docs/adr/0009-a-release-is-the-qualified-commit-plus-its-record.md)).
5. **A provider that updated itself.** An agent whose provider CLI upgraded itself holds at its next restart until that combination is qualified ([AssemblyAI#7](https://github.com/talvor/AssemblyAI/issues/7), [AssemblyAI#14](https://github.com/talvor/AssemblyAI/issues/14)).

### Sign-in

6. **Subscription only.** The user installs and signs in to each provider themselves on the host. AsmAI never starts a sign-in, never collects, reads or transfers provider tokens, and never falls back to API billing. The pinned copies read the user's existing sign-in themselves ([AssemblyAI#15](https://github.com/talvor/AssemblyAI/issues/15), [AssemblyAI#9](https://github.com/talvor/AssemblyAI/issues/9)).
7. **Checking readiness.** AsmAI checks each pinned CLI's sign-in through that CLI's own status check, which reports the sign-in method only, never a secret. An API-key or unknown sign-in method fails the check, and AsmAI prints the native command for the user to run ([AssemblyAI#9](https://github.com/talvor/AssemblyAI/issues/9), [AssemblyAI#15](https://github.com/talvor/AssemblyAI/issues/15)). Readiness is not a guarantee of allowance ([AssemblyAI#19](https://github.com/talvor/AssemblyAI/issues/19)); [07](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/07-limits-holds-and-visibility.md) specifies a sign-in lost while running.
8. **No API keys in sessions.** Every agent session starts without provider API-key variables, so a stray key cannot switch an agent to API billing ([AssemblyAI#9](https://github.com/talvor/AssemblyAI/issues/9)).

### Per-session settings

9. **Passed per session only.** Hooks, the `asmai` allow-list entry, role instructions and role skills go on each agent's command line: for Claude Code `--settings`, `--setting-sources` and `--plugin-dir`; for Codex `-c` ([AssemblyAI#9](https://github.com/talvor/AssemblyAI/issues/9), [ADR 0003](https://github.com/talvor/AssemblyAI/blob/main/docs/adr/0003-go-executable-runs-pinned-providers.md)).
10. **The user's provider configuration is never written.** AsmAI never writes `~/.claude` or `~/.codex` ([AssemblyAI#9](https://github.com/talvor/AssemblyAI/issues/9)).
11. **`asmai` is allowed.** Each provider's permission allow-list covers `asmai`, so coordination calls never raise a native permission prompt ([ADR 0002](https://github.com/talvor/AssemblyAI/blob/main/docs/adr/0002-agents-coordinate-through-asmai-cli.md), [AssemblyAI#8](https://github.com/talvor/AssemblyAI/issues/8)).
12. **Native review is kept.** AsmAI keeps the providers' native permission prompts and hook-trust review; it never bypasses an approval ([AssemblyAI#19](https://github.com/talvor/AssemblyAI/issues/19), [AssemblyAI#15](https://github.com/talvor/AssemblyAI/issues/15)). Codex's hook definitions need the user's one-time native trust review ([AssemblyAI#9](https://github.com/talvor/AssemblyAI/issues/9)).
13. **Hooks name a fixed path.** Hook definitions name the daemon's copy of the executable at its one fixed path, never a versioned path, so Codex's trust in them can survive an upgrade ([AssemblyAI#20](https://github.com/talvor/AssemblyAI/issues/20), [10](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/10-release-install-and-upgrade.md)).
14. **Elsewhere.** The repository's own provider configuration is never loaded and the qualified write guards are switched on ([05](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/05-repositories-and-job-branches.md)); skills are delivered and hidden per provider ([08](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/08-skills-and-agent-instructions.md)).
15. **What runs without a prompt.** Agents run inside the provider's qualified write guard, which keeps their writes in the workspace. Commands the guard allows run without a native prompt, including git and gh with network access; anything it does not allow raises the native prompt and waits for the user in that agent's terminal. The exact settings for each provider version are qualified ([AssemblyAI#11](https://github.com/talvor/AssemblyAI/issues/11), [AssemblyAI#19](https://github.com/talvor/AssemblyAI/issues/19), [answers](https://github.com/talvor/AssemblyAI/blob/main/.lavish/spec-doc-03-answers.json)).

### Daemon-owned terminals and hooks

16. **Unmodified interactive CLIs.** Agents run the providers' unmodified interactive CLIs, each in a PTY the daemon owns, with provider-specific passive lifecycle hooks ([AssemblyAI#19](https://github.com/talvor/AssemblyAI/issues/19), [ADR 0001](https://github.com/talvor/AssemblyAI/blob/main/docs/adr/0001-daemon-owns-agent-terminals.md)).
17. **Terminal emulation is AsmAI's.** The daemon emulates each agent's terminal, and its fidelity is qualified per platform ([ADR 0001](https://github.com/talvor/AssemblyAI/blob/main/docs/adr/0001-daemon-owns-agent-terminals.md)).
18. **Hook intake.** The hooks report lifecycle events to the daemon as observations, among them session start, prompt submission, permission requests and turn stops, and, where the provider has them, interrupts and turns that ended on an error. The daemon correlates each to a dispatch ([AssemblyAI#19](https://github.com/talvor/AssemblyAI/issues/19), [AssemblyAI#14](https://github.com/talvor/AssemblyAI/issues/14), [02](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/02-daemon-and-store.md)).
19. **Separate states.** Process, turn, decision and assignment state are kept apart. A turn that stops may carry a result, a blocked report or a decision request, each identified by its assignment or decision and correlated to the current dispatch. A hook, an idle terminal or a process exit is never completion of an assignment; only the owning leader's acceptance is ([AssemblyAI#19](https://github.com/talvor/AssemblyAI/issues/19)).
20. **Missing signals.** Where a provider version lacks a signal, AsmAI's safe default stands in, and the gap is listed as a known limitation ([AssemblyAI#12](https://github.com/talvor/AssemblyAI/issues/12), [ADR 0008](https://github.com/talvor/AssemblyAI/blob/main/docs/adr/0008-qualification-runs-real-provider-clis-on-real-hosts.md)). For example, the feasibility probe saw no interrupt hook from Claude Code, so an interrupted Claude turn must be recognized by a qualified means, or its state is unknown ([AssemblyAI#10](https://github.com/talvor/AssemblyAI/issues/10), [AssemblyAI#19](https://github.com/talvor/AssemblyAI/issues/19)).

### The input fence

21. **One input owner.** Each agent session has exactly one input owner at any time, automation or the user, and one current assignment. Human and automated input never compete ([AssemblyAI#19](https://github.com/talvor/AssemblyAI/issues/19), [AssemblyAI#15](https://github.com/talvor/AssemblyAI/issues/15)).
22. **Typing only at a known boundary.** The daemon types into an agent only while automation owns its input and the agent is at a known input-ready boundary ([AssemblyAI#8](https://github.com/talvor/AssemblyAI/issues/8), [AssemblyAI#7](https://github.com/talvor/AssemblyAI/issues/7)).
23. **Positive submission acknowledgment.** An automated submission counts as submitted only when the provider positively acknowledges it with a correlated observation. A successful PTY write never counts, and an unacknowledged submission leaves the agent's input state unknown ([AssemblyAI#19](https://github.com/talvor/AssemblyAI/issues/19), [AssemblyAI#7](https://github.com/talvor/AssemblyAI/issues/7)).
24. **The modal allow-list.** For each qualified provider version, the release carries an allow-list of qualified modals, each with a safe default answer. It starts empty. No allow-listed answer may change the provider, the model, the sign-in or permissions ([AssemblyAI#7](https://github.com/talvor/AssemblyAI/issues/7)).
25. **Unknown input states hold.** Any input state not on the allow-list, such as a provider modal AsmAI does not recognize, holds that agent instead of being typed over, and Coordination brings it to the user while independent work continues. Automatic cancel-and-retry is never used ([AssemblyAI#7](https://github.com/talvor/AssemblyAI/issues/7), [AssemblyAI#14](https://github.com/talvor/AssemblyAI/issues/14), [AssemblyAI#19](https://github.com/talvor/AssemblyAI/issues/19)).
26. **Witnessed messages.** Because the daemon owns the input, it can tell the user's own submissions from its nudges and journals the user's word for word ([AssemblyAI#10](https://github.com/talvor/AssemblyAI/issues/10), [01](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/01-roles-and-decisions.md)).

### The attach client and the status line

27. **Attaching observes.** `asmai attach <agent>` shows the agent's terminal and observes by default ([AssemblyAI#7](https://github.com/talvor/AssemblyAI/issues/7), [AssemblyAI#9](https://github.com/talvor/AssemblyAI/issues/9)). Agents are addressed as `name@role`, and a bare role name means its leader ([09](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/09-cli-and-configuration.md)).
28. **The client draws the screen.** The attach client renders the provider's screen itself, as tmux does, and gives the provider one row less ([ADR 0004](https://github.com/talvor/AssemblyAI/blob/main/docs/adr/0004-attach-client-draws-status-line.md)).
29. **The status line.** The freed row is a status line drawn from daemon state in every attached terminal, the conversation and every agent alike. It shows what is waiting on the user (decisions, agents stopped at native prompts, input the user still holds), the focused job, the running jobs and any agent whose input the user holds. It costs no model tokens and is current even in the middle of a turn ([ADR 0004](https://github.com/talvor/AssemblyAI/blob/main/docs/adr/0004-attach-client-draws-status-line.md), [AssemblyAI#10](https://github.com/talvor/AssemblyAI/issues/10)). It also shows holds and their causes, queued assignments, and a newer installed version waiting for a restart ([AssemblyAI#14](https://github.com/talvor/AssemblyAI/issues/14), [AssemblyAI#20](https://github.com/talvor/AssemblyAI/issues/20), [07](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/07-limits-holds-and-visibility.md)).
30. **The Ctrl-] menu.** Inside an attached terminal, Ctrl-] opens a menu to detach, take, release or interrupt, and lists the conversation and every agent, those waiting on the user first, to move this terminal there ([AssemblyAI#9](https://github.com/talvor/AssemblyAI/issues/9), [AssemblyAI#10](https://github.com/talvor/AssemblyAI/issues/10)). Leaving the conversation this way counts as leaving it ([04](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/04-conversation-and-lavish.md)).
31. **Terminals.** Ghostty is qualified on each certified platform, locally and over SSH. Other terminals and multiplexers, including running the attach client inside tmux, are best effort, and `asmai doctor` says so ([AssemblyAI#12](https://github.com/talvor/AssemblyAI/issues/12), [ADR 0001](https://github.com/talvor/AssemblyAI/blob/main/docs/adr/0001-daemon-owns-agent-terminals.md)).

### Taking and releasing an agent

32. **Taking input is explicit.** `asmai take <agent>` (or the menu) makes the user the input owner. If a turn is running, the default is to wait for its boundary; `--interrupt` interrupts it instead ([AssemblyAI#7](https://github.com/talvor/AssemblyAI/issues/7), [AssemblyAI#9](https://github.com/talvor/AssemblyAI/issues/9)).
33. **Drafts are cleared, not kept typing.** Any unsent automated draft is recorded and cleared before input is handed to the user ([AssemblyAI#7](https://github.com/talvor/AssemblyAI/issues/7), [AssemblyAI#19](https://github.com/talvor/AssemblyAI/issues/19)).
34. **Native prompts.** A native permission prompt counts as a boundary, and the user can answer it directly in the agent's terminal; the answer is recorded ([AssemblyAI#7](https://github.com/talvor/AssemblyAI/issues/7), [AssemblyAI#15](https://github.com/talvor/AssemblyAI/issues/15)).
35. **While the user holds input,** automated input waits: messages for the agent wait in its inbox and are delivered after release ([AssemblyAI#8](https://github.com/talvor/AssemblyAI/issues/8), [AssemblyAI#10](https://github.com/talvor/AssemblyAI/issues/10)). The owning leader keeps control of the worker's scope and priority ([AssemblyAI#15](https://github.com/talvor/AssemblyAI/issues/15)).
36. **Release is explicit.** `asmai release <agent>` (or the menu) returns input to automation. Detaching without releasing leaves the agent paused, and the status line keeps reminding the user that they hold its input ([AssemblyAI#7](https://github.com/talvor/AssemblyAI/issues/7), [ADR 0004](https://github.com/talvor/AssemblyAI/blob/main/docs/adr/0004-attach-client-draws-status-line.md)).
37. **What release does.** If the user only answered native prompts, the same dispatch continues. If the user typed any message, that dispatch is superseded: the owning leader receives the intervention record, reconciles, and resumes the worker with a new dispatch ([AssemblyAI#10](https://github.com/talvor/AssemblyAI/issues/10)). That dispatch counts toward the assignment's dispatch limit ([AssemblyAI#14](https://github.com/talvor/AssemblyAI/issues/14), [07](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/07-limits-holds-and-visibility.md)).
38. **The intervention record** holds the user's messages word for word, the prompt answers, the drafts that were cleared, the effects recorded meanwhile, and an optional note the user gives at release ([AssemblyAI#10](https://github.com/talvor/AssemblyAI/issues/10)).
39. **A newer take moves the hold.** A newer `take` of an agent whose input the user already holds moves the hold to the new terminal ([AssemblyAI#10](https://github.com/talvor/AssemblyAI/issues/10)).
40. **Only the user takes.** Take and release refuse an agent's credential ([AssemblyAI#9](https://github.com/talvor/AssemblyAI/issues/9), [09](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/09-cli-and-configuration.md)).

### Recordings

41. **Every dispatch is recorded.** Every agent terminal is recorded per dispatch and compressed, and the journal records where ([AssemblyAI#14](https://github.com/talvor/AssemblyAI/issues/14)).
42. **Replay.** `asmai replay <agent> [--dispatch <id>]` replays a recording ([AssemblyAI#14](https://github.com/talvor/AssemblyAI/issues/14)).
43. **Retention.** Recordings are deleted a set time after their job ends ([AssemblyAI#14](https://github.com/talvor/AssemblyAI/issues/14)).
44. **Transcripts stay put.** Provider transcripts stay where the provider writes them, and the journal records their location per dispatch ([AssemblyAI#14](https://github.com/talvor/AssemblyAI/issues/14)).

### Not a security boundary

45. The same-user terminal relay, the agent command guard and the write guards prevent mistakes; none is a security boundary against a process with the user's own access ([AssemblyAI#19](https://github.com/talvor/AssemblyAI/issues/19), [AssemblyAI#9](https://github.com/talvor/AssemblyAI/issues/9), [AssemblyAI#11](https://github.com/talvor/AssemblyAI/issues/11)).

## Interfaces

### Commands

| Who | Command | Purpose |
| --- | --- | --- |
| The user | `asmai providers install\|list` | Install the pinned providers after confirming; list them |
| The user | `asmai attach <agent>` | Observe an agent's terminal |
| The user | `asmai take <agent> [--interrupt]` | Take its input, at the boundary or by interrupting |
| The user | `asmai release <agent>` | Return its input to automation |
| The user | Ctrl-] in an attached terminal | Detach, take, release, interrupt, or move to the conversation or another agent |
| The user | `asmai replay <agent> [--dispatch <id>]` | Replay a recording |

[09](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/09-cli-and-configuration.md) gives the syntax, and `--host` for remote use.

### Store records

| Record | Holds |
| --- | --- |
| Provider install | Each pinned provider's name, version and where AsmAI keeps it |
| Session start | The provider version, the per-session settings passed (never environment variables) and the session generation ([02](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/02-daemon-and-store.md)) |
| Input owner | Who owns each agent's input, and since when |
| Cleared draft | The automated draft text cleared at a take |
| Native prompt answer | The prompt, the user's answer and the dispatch |
| Intervention | The fields in rule 38, the agent and dispatch, and whether the dispatch continued or was superseded |
| Recording | Its dispatch, file and size |

### Files

- **The pinned provider copies**, kept by AsmAI apart from the user's own installations ([AssemblyAI#9](https://github.com/talvor/AssemblyAI/issues/9)).
- **The modal allow-list**, carried by the release for each qualified provider version (rule 24).
- **Recordings**, compressed, in the state directory ([02](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/02-daemon-and-store.md)).

## Settings and defaults

| Setting | Default | Rule |
| --- | --- | --- |
| Recording retention after a job ends | 14 days | 43 |

The modal allow-list and the pinned versions belong to the release, not the configuration (rules 4, 24); the pinned versions come from the release's pins file (rule 2). [09](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/09-cli-and-configuration.md) names the field ([AssemblyAI#14](https://github.com/talvor/AssemblyAI/issues/14)).

## Failure handling

| Failure | Handling |
| --- | --- |
| Unqualified provider version at start | Refused before any dispatch, with what to do (rule 4) |
| Provider CLI upgraded itself | Its agent holds at the next restart (rule 5) |
| API-key or unknown sign-in | The check fails and prints the native command (rule 7) |
| Unknown input state or unrecognized modal | The agent holds; Coordination brings it to the user (rule 25) |
| Submission not acknowledged | Input state unknown; no blind retype (rule 23) |
| Missing provider signal | The safe default; listed as a known limitation (rule 20) |
| The user detaches without releasing | The agent stays paused; the status line reminds the user (rule 36) |
| Terminal or SSH disconnect | Agents keep running in the daemon's terminals; the user reattaches ([02](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/02-daemon-and-store.md)) |

## Qualification cases and proving scenarios

- **C2**: an unqualified provider version is refused before any dispatch; a provider CLI that upgraded itself holds its agent at the next restart (rules 4, 5).
- **C3**: the pinned copies reuse the user's existing sign-in without a new login (rule 6).
- **C4**: every agent session starts without provider API-key variables (rule 8).
- **C6**: any input state not on the allow-list holds the agent instead of being typed over (rules 24, 25).
- **C7**: positive acknowledgment of each automated submission (rule 23).
- **C8**: taking an agent mid-turn and with an unsent automated draft (rules 32, 33).
- **C9**: the attach client's rendering under the status line, at reduced height (rules 28, 29).
- **C11**: capturing witnessed messages and telling them apart from nudges (rule 26).
- **C12**: recognising an interrupted Claude turn (rule 20).
- **C14**: terminal recording per dispatch, and replay (rules 41, 42).
- **C24**: terminal and SSH disconnect.
- **C5** relies on rule 13 ([10](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/10-release-install-and-upgrade.md)); **C37** on rule 15 ([05](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/05-repositories-and-job-branches.md)).
- **S7**: an intervention where the user takes a worker, types a correction and releases it; the intervention record reaches the owning leader, followed by a new dispatch.
- **S8** and **S9**: leaving and coming back, an SSH drop mid-turn; the recordings are part of every scenario's evidence.

## Sources

- [Choose factory hosting and lifecycle](https://github.com/talvor/AssemblyAI/issues/7#issuecomment-5976506834) (AssemblyAI#7)
- [Define work state and coordination contracts](https://github.com/talvor/AssemblyAI/issues/8#issuecomment-5976668034) (AssemblyAI#8)
- [Define CLI setup and management experience](https://github.com/talvor/AssemblyAI/issues/9#issuecomment-5979143255) (AssemblyAI#9)
- [Explore terminal conversation and Lavish decision flow](https://github.com/talvor/AssemblyAI/issues/10#issuecomment-5989237516) (AssemblyAI#10)
- [Define concurrent repository work and integration](https://github.com/talvor/AssemblyAI/issues/11#issuecomment-5990301132) (AssemblyAI#11)
- [Define v1 acceptance scenarios and evidence](https://github.com/talvor/AssemblyAI/issues/12#issuecomment-5993314453) (AssemblyAI#12)
- [Define operating limits and visibility](https://github.com/talvor/AssemblyAI/issues/14#issuecomment-5991304507) (AssemblyAI#14)
- [Choose runtime adapters and authentication](https://github.com/talvor/AssemblyAI/issues/15#issuecomment-5968867443) (AssemblyAI#15)
- [Validate interactive CLI coordination and intervention](https://github.com/talvor/AssemblyAI/issues/19#issuecomment-5976021294) (AssemblyAI#19), with its [prototype notes](https://github.com/talvor/AssemblyAI/blob/13423d97798b26b4a825f799e803e4cd705fcd7b/.scratch/interactive-cli-prototype/README.md) and [observed evidence](https://github.com/talvor/AssemblyAI/blob/13423d97798b26b4a825f799e803e4cd705fcd7b/.scratch/interactive-cli-prototype/evidence.json)
- [Choose license, release packaging and upgrade migration](https://github.com/talvor/AssemblyAI/issues/20#issuecomment-6004145724) (AssemblyAI#20)
- Research behind it: [Research agent runtimes and persistent sessions](https://github.com/talvor/AssemblyAI/issues/4#issuecomment-5968137383) (AssemblyAI#4) and the [runtime adapter check](https://github.com/talvor/AssemblyAI/blob/main/docs/research/runtime-adapter-check.md)
- [ADR 0001](https://github.com/talvor/AssemblyAI/blob/main/docs/adr/0001-daemon-owns-agent-terminals.md), [ADR 0002](https://github.com/talvor/AssemblyAI/blob/main/docs/adr/0002-agents-coordinate-through-asmai-cli.md), [ADR 0003](https://github.com/talvor/AssemblyAI/blob/main/docs/adr/0003-go-executable-runs-pinned-providers.md), [ADR 0004](https://github.com/talvor/AssemblyAI/blob/main/docs/adr/0004-attach-client-draws-status-line.md), [ADR 0009](https://github.com/talvor/AssemblyAI/blob/main/docs/adr/0009-a-release-is-the-qualified-commit-plus-its-record.md) and the [glossary](https://github.com/talvor/AssemblyAI/blob/main/GLOSSARY.md): Intervention, Witnessed message, Hold, Known limitation, Lavish build.
- The [Lavish and skill delivery review](https://github.com/talvor/AssemblyAI/blob/main/.lavish/lavish-delivery-answers.json) (2026-10-07), with the [Lavish deno compile check](https://github.com/talvor/AssemblyAI/blob/main/docs/research/lavish-deno-compile-check.md) and [ADR 0010](https://github.com/talvor/AssemblyAI/blob/main/docs/adr/0010-lavish-is-a-deno-compiled-executable-built-per-pin.md): Lavish built as a Deno-compiled executable when its pin moves, and how the daemon runs it.
- The review of this document: [questions](https://github.com/talvor/AssemblyAI/blob/main/.lavish/spec-doc-03-round1-questions.json) and [answers](https://github.com/talvor/AssemblyAI/blob/main/.lavish/spec-doc-03-answers.json).
