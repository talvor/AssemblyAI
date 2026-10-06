# 02 Daemon and store

This document specifies the per-user daemon and the store it keeps: starting, stopping and the optional service; the store and its journal; jobs; the life cycles of dispatches and assignments; the inbox and nudges; generations and fencing; effects; reconciliation; leaders on demand; and recovery. [03 Provider sessions and terminals](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/03-provider-sessions-and-terminals.md) specifies the terminals the daemon owns, and [01 Roles and decisions](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/01-roles-and-decisions.md) the records it keeps about roles and decisions.

## Rules

### The daemon

1. **One factory per user per host.** Each OS user runs at most one factory per host, installed without root. Factories on different hosts are independent and share no state ([AssemblyAI#7](https://github.com/talvor/AssemblyAI/issues/7)).
2. **The daemon owns the factory.** A per-user AsmAI daemon owns every provider PTY, the single-input-owner fence and passive hook intake ([03](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/03-provider-sessions-and-terminals.md)), supervises the factory's Lavish server ([04](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/04-conversation-and-lavish.md)), and is the only writer of the store ([ADR 0001](https://github.com/talvor/AssemblyAI/blob/main/docs/adr/0001-daemon-owns-agent-terminals.md), [ADR 0002](https://github.com/talvor/AssemblyAI/blob/main/docs/adr/0002-agents-coordinate-through-asmai-cli.md)).
3. **No network listener.** The factory opens no network listener. Agents and commands reach the daemon over a local Unix socket, and remote use goes through SSH only ([AssemblyAI#7](https://github.com/talvor/AssemblyAI/issues/7), [ADR 0002](https://github.com/talvor/AssemblyAI/blob/main/docs/adr/0002-agents-coordinate-through-asmai-cli.md)).
4. **One executable.** The same `asmai` executable is the daemon, the user's CLI and the agents' CLI ([AssemblyAI#9](https://github.com/talvor/AssemblyAI/issues/9)). Agents run the daemon's own copy of it, so they never meet another version ([AssemblyAI#20](https://github.com/talvor/AssemblyAI/issues/20), [10](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/10-release-install-and-upgrade.md)).

### Starting

5. **`asmai start` runs the daemon**, in the background, or in the foreground with `--foreground`. A bare `asmai` or `asmai chat` starts a stopped factory first and says so ([AssemblyAI#7](https://github.com/talvor/AssemblyAI/issues/7), [AssemblyAI#9](https://github.com/talvor/AssemblyAI/issues/9)).
6. **Checks before anything runs.** Start runs the setup checks and names any step that fails ([AssemblyAI#9](https://github.com/talvor/AssemblyAI/issues/9), [09](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/09-cli-and-configuration.md)). Before any dispatch it refuses an uncertified platform and any provider combination outside the release's qualification record, with actionable guidance ([AssemblyAI#7](https://github.com/talvor/AssemblyAI/issues/7), [AssemblyAI#12](https://github.com/talvor/AssemblyAI/issues/12)). It refuses a store it cannot use and migrates one that needs it ([AssemblyAI#20](https://github.com/talvor/AssemblyAI/issues/20), [10](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/10-release-install-and-upgrade.md)).
7. **Every start is a recovery.** Every start follows the same path, whether after `asmai stop`, a crash or a reboot: terminate what the previous daemon left behind (rule 55), restore the leaders, then reconcile ([AssemblyAI#7](https://github.com/talvor/AssemblyAI/issues/7), [ADR 0001](https://github.com/talvor/AssemblyAI/blob/main/docs/adr/0001-daemon-owns-agent-terminals.md)). Restoring the leaders starts Coordination and every leader whose role has open work ([AssemblyAI#14](https://github.com/talvor/AssemblyAI/issues/14)).

### The service

8. **Opt-in.** The daemon runs without a service manager. `asmai service install` registers a systemd user unit, with linger so it runs on a remote Linux host without a login session, or a launchd LaunchAgent, which starts at login. The factory then comes back after a reboot. `asmai service uninstall` and `asmai service status` remove it and report it ([AssemblyAI#7](https://github.com/talvor/AssemblyAI/issues/7), [AssemblyAI#9](https://github.com/talvor/AssemblyAI/issues/9)).

### Stopping

9. **`asmai stop` drains.** It dispatches nothing new, lets running turns reach a boundary (waiting, stopped or a result) for up to the drain timeout, interrupts the rest, persists state and exits. `asmai stop --now` skips the wait ([AssemblyAI#7](https://github.com/talvor/AssemblyAI/issues/7), [AssemblyAI#14](https://github.com/talvor/AssemblyAI/issues/14)).
10. **What survives a stop:** pending decisions, grants and queued requests ([AssemblyAI#7](https://github.com/talvor/AssemblyAI/issues/7)).
11. **Continuing after a stop.** An unclean stop recovers through the normal reconciliation path at the next start ([AssemblyAI#7](https://github.com/talvor/AssemblyAI/issues/7)). After a clean stop, the next start runs each worker whose dispatch stopped at a boundary again on the same provider, resuming its native session where possible, and continues its assignment with a new dispatch, which is a resumption and does not count toward the dispatch limit ([07](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/07-limits-holds-and-visibility.md)); an assignment whose native session cannot be resumed needs reconciliation ([AssemblyAI#14](https://github.com/talvor/AssemblyAI/issues/14), [answers](https://github.com/talvor/AssemblyAI/blob/main/.lavish/spec-doc-02-answers.json)).
12. **No factory-wide pause.** `asmai stop` is the only way to stop the whole factory; pausing applies to one job ([AssemblyAI#14](https://github.com/talvor/AssemblyAI/issues/14), [07](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/07-limits-holds-and-visibility.md)).

### The store and the journal

13. **The daemon is the only writer** to an embedded SQLite store. Agents never touch the database, and the user inspects it through `asmai` commands and the export, never by editing it ([AssemblyAI#8](https://github.com/talvor/AssemblyAI/issues/8), [ADR 0002](https://github.com/talvor/AssemblyAI/blob/main/docs/adr/0002-agents-coordinate-through-asmai-cli.md)).
14. **Current state and the journal together.** The store holds the current state of the factory's jobs and agents and an append-only journal of everything that happened: dispatches, observations, effects, decisions and acceptances. Each journal entry is written in the same transaction as the current-state change it records ([AssemblyAI#8](https://github.com/talvor/AssemblyAI/issues/8)).
15. **Kept in full.** The journal is never trimmed in v1 ([AssemblyAI#8](https://github.com/talvor/AssemblyAI/issues/8), [AssemblyAI#14](https://github.com/talvor/AssemblyAI/issues/14)).
16. **What is never recorded:** environment variables ([AssemblyAI#14](https://github.com/talvor/AssemblyAI/issues/14)).
17. **Every record knows its job and role.** Every handoff, assignment, decision request and inbox message is recorded with its job and role, so the daemon always knows each role's open work ([AssemblyAI#14](https://github.com/talvor/AssemblyAI/issues/14)).
18. **Copies.** `asmai backup <file>` takes a consistent copy of the store while the factory runs, and `asmai export` writes the journal out for inspection. Backups, restores and migrations act on the whole store ([AssemblyAI#9](https://github.com/talvor/AssemblyAI/issues/9), [AssemblyAI#20](https://github.com/talvor/AssemblyAI/issues/20)). The user is responsible for backing up the state directory ([AssemblyAI#7](https://github.com/talvor/AssemblyAI/issues/7)).

### Jobs

19. **A job** is one outcome the user requested through Coordination, with its mandate and acceptance criteria, against at most one registered repository or none. It owns its handoffs, assignments, decisions and grants ([AssemblyAI#8](https://github.com/talvor/AssemblyAI/issues/8)). Jobs are addressed by number ([AssemblyAI#9](https://github.com/talvor/AssemblyAI/issues/9)).
20. **Follow-ups** are new jobs linked to the job they follow ([AssemblyAI#8](https://github.com/talvor/AssemblyAI/issues/8)). [05](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/05-repositories-and-job-branches.md) specifies when a follow-up continues its predecessor's job branch.
21. **The end of a job.** A job ends when its outcome is delivered, as [06](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/06-validation-and-delivery.md) specifies, or when its cancellation completes ([07](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/07-limits-holds-and-visibility.md)). Nothing about a job is watched after it ends ([AssemblyAI#18](https://github.com/talvor/AssemblyAI/issues/18), [AssemblyAI#14](https://github.com/talvor/AssemblyAI/issues/14)).
22. **Briefs are the leaders' context.** `asmai brief <job>` is generated from the store and is canonical. It covers the job's open handoffs, assignments, pending decisions, grants and recent journal entries, and for a repository job it points to the leaders' view ([05](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/05-repositories-and-job-branches.md)). Leaders load it at every start and whenever they switch jobs; resuming a provider's native session is only a convenience ([AssemblyAI#8](https://github.com/talvor/AssemblyAI/issues/8), [AssemblyAI#11](https://github.com/talvor/AssemblyAI/issues/11)).

### Dispatches

23. **A dispatch** is one identified delivery of work to one agent session generation. A retry, a correction or a resumption is always a new dispatch ([AssemblyAI#8](https://github.com/talvor/AssemblyAI/issues/8)).
24. **Dispatch states:** created → nudged → delivered → working → stopped (with a result, a blocked report or a decision request), or unknown ([AssemblyAI#8](https://github.com/talvor/AssemblyAI/issues/8)).
25. **Only current evidence counts.** Only evidence correlated to the current dispatch changes its state. Older evidence is journaled but can never complete the current dispatch ([AssemblyAI#8](https://github.com/talvor/AssemblyAI/issues/8), [AssemblyAI#19](https://github.com/talvor/AssemblyAI/issues/19)).
26. **No inference from silence.** Readiness and completion are never inferred from silence, screen text, process exit or a successful PTY write. A stop that the provider reports is a turn boundary, never acceptance of the assignment ([AssemblyAI#19](https://github.com/talvor/AssemblyAI/issues/19)).
27. **Missing observations.** A working dispatch with no correlated lifecycle observation for the silence timeout becomes unknown, and its owning leader is told. Nothing is killed or retried automatically ([AssemblyAI#8](https://github.com/talvor/AssemblyAI/issues/8), [AssemblyAI#14](https://github.com/talvor/AssemblyAI/issues/14)).
28. **Duplicate, late, reordered and conflicting observations.** Duplicate, late and out-of-order observations are journaled, but only correlated observations of the current dispatch change state. Conflicting observations make the dispatch unknown ([AssemblyAI#8](https://github.com/talvor/AssemblyAI/issues/8)).
29. **What each dispatch records:** the skill bundle version it ran with and a fingerprint of any added or repository skill ([AssemblyAI#17](https://github.com/talvor/AssemblyAI/issues/17)); its token counts ([AssemblyAI#14](https://github.com/talvor/AssemblyAI/issues/14)); where the provider wrote its transcript ([AssemblyAI#14](https://github.com/talvor/AssemblyAI/issues/14)); and its terminal recording ([03](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/03-provider-sessions-and-terminals.md)).

### Assignments

30. **Assignment states:** active → result submitted → accepted; or rejected, which returns it to active with the same worker; or needs reconciliation; or cancelled ([AssemblyAI#8](https://github.com/talvor/AssemblyAI/issues/8)). Before its first dispatch an assignment may be queued for a worker slot, and at any time it may be held; [07](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/07-limits-holds-and-visibility.md) specifies both ([AssemblyAI#14](https://github.com/talvor/AssemblyAI/issues/14)).
31. **A moved job branch is not a rejection.** If the job branch moved after a result was submitted, the work returns to the same worker to take in the new tip and submit again ([AssemblyAI#11](https://github.com/talvor/AssemblyAI/issues/11), [05](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/05-repositories-and-job-branches.md)).
32. **Automatic retries** happen only for an assignment its owning leader explicitly declared side-effect-free, such as read-only research or analysis. They are bounded, and each is a new dispatch. Everything else goes through reconciliation ([AssemblyAI#8](https://github.com/talvor/AssemblyAI/issues/8), [AssemblyAI#14](https://github.com/talvor/AssemblyAI/issues/14)).

### The inbox and nudges

33. **A durable inbox.** Messages, handoffs and work for an agent wait in its durable inbox ([AssemblyAI#8](https://github.com/talvor/AssemblyAI/issues/8)).
34. **Content never travels through the terminal.** At a known input-ready boundary, while automation owns the agent's input, the daemon types a one-line nudge carrying only the dispatch ID ([AssemblyAI#8](https://github.com/talvor/AssemblyAI/issues/8), [ADR 0002](https://github.com/talvor/AssemblyAI/blob/main/docs/adr/0002-agents-coordinate-through-asmai-cli.md)).
35. **The fetch is the evidence.** The agent pulls the content with `asmai inbox`, and that fetch is the positive evidence of delivery. A successful PTY write is not ([AssemblyAI#8](https://github.com/talvor/AssemblyAI/issues/8)).
36. **Nudges may repeat**, because reads are idempotent by message ID ([AssemblyAI#8](https://github.com/talvor/AssemblyAI/issues/8)).
37. **No boundary, no nudge.** While the user holds an agent's input, while the agent is at an unknown input state, or at any other time there is no deliverable boundary, its messages wait durably ([AssemblyAI#8](https://github.com/talvor/AssemblyAI/issues/8), [03](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/03-provider-sessions-and-terminals.md)).

### Generations and fencing

38. **Identity.** Each `asmai` call from an agent carries its session's credential from the environment, and the daemon checks the call against that session's identity and generation ([AssemblyAI#8](https://github.com/talvor/AssemblyAI/issues/8), [ADR 0002](https://github.com/talvor/AssemblyAI/blob/main/docs/adr/0002-agents-coordinate-through-asmai-cli.md)).
39. **Generations.** Every leader and worker session gets a generation from the daemon, which rejects factory-state calls from any superseded generation ([AssemblyAI#8](https://github.com/talvor/AssemblyAI/issues/8)).
40. **No stale writer.** Before starting a replacement session, the daemon terminates the superseded session's process group, so no stale writer remains on the host ([AssemblyAI#8](https://github.com/talvor/AssemblyAI/issues/8)).
41. **One leader per role.** Fencing keeps at most one leader per role at any instant: a stale or resumed leader process is rejected. There are no standby leaders ([AssemblyAI#7](https://github.com/talvor/AssemblyAI/issues/7)).

### Effects

42. **Recorded as they happen.** A worker records each consequential effect (a commit, a push, a pull request created or updated, a comment, a write outside its workspace) with `asmai effect <kind> <ref>` immediately after making it, tagged with its dispatch, and lists its effects again in its result ([AssemblyAI#8](https://github.com/talvor/AssemblyAI/issues/8)).
43. **Leaders and the daemon record theirs too.** The delivering leader records each pull request it opens or updates as an effect, and the daemon records each push it makes ([AssemblyAI#18](https://github.com/talvor/AssemblyAI/issues/18), [ADR 0007](https://github.com/talvor/AssemblyAI/blob/main/docs/adr/0007-asmai-delivers-tested-prs-with-its-own-roles.md)).
44. **Evidence, not proof.** External actions (git, GitHub) are not routed through `asmai`. The effect ledger is evidence, and reconciliation checks it against the real repository and GitHub ([AssemblyAI#8](https://github.com/talvor/AssemblyAI/issues/8), [ADR 0002](https://github.com/talvor/AssemblyAI/blob/main/docs/adr/0002-agents-coordinate-through-asmai-cli.md)).
45. **No exactly-once claim.** AsmAI never assumes an effect happened exactly once and never blindly repeats one ([AssemblyAI#19](https://github.com/talvor/AssemblyAI/issues/19)).

### Reconciliation

46. **The owning leader reconciles** a dispatch whose outcome is unknown, and an assignment that needs reconciliation. It inspects the recorded effects, the real state of the repository and GitHub, and the transcript where available ([AssemblyAI#8](https://github.com/talvor/AssemblyAI/issues/8)).
47. **The record.** It records what is known, what is not, and its choice: a new dispatch to the same worker, a fresh worker, abandoning the work, or escalating. The record is a delegated decision ([AssemblyAI#8](https://github.com/talvor/AssemblyAI/issues/8), [01](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/01-roles-and-decisions.md)).
48. **When the user is asked.** Only when distinct viable recovery approaches remain or the needed action is outside the mandate ([AssemblyAI#8](https://github.com/talvor/AssemblyAI/issues/8)).
49. **Reporting.** Coordination reports changed plans, and effects that cannot be undone, to the user ([AssemblyAI#8](https://github.com/talvor/AssemblyAI/issues/8)).

### Leaders on demand

50. **Coordination always runs** while the factory runs ([AssemblyAI#14](https://github.com/talvor/AssemblyAI/issues/14)).
51. **Starting a leader.** The daemon starts a role's leader when a message for that role arrives and none is running. Coordination makes sure a leader runs by handing work to its role; it never manages processes ([AssemblyAI#14](https://github.com/talvor/AssemblyAI/issues/14)).
52. **Stopping a leader.** The daemon stops a leader at a boundary, after the leader idle grace, once its role has no open work in any unpaused job: no open handoffs to it, no assignments it owns, no decision it requested still pending, and nothing in its inbox. A paused job's work does not keep a leader running. A role with no running leader and no work is normal, not a fault ([AssemblyAI#14](https://github.com/talvor/AssemblyAI/issues/14)).
53. **A leader's provider.** A leader that starts while its role has no open work in any job, paused or not, counts as before first dispatch, so it may start on the other configured, compatible provider; [07](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/07-limits-holds-and-visibility.md) specifies when ([AssemblyAI#14](https://github.com/talvor/AssemblyAI/issues/14)).

### Recovery

54. **What v1 recovers from**, with work intact after reconciliation: a terminal or SSH disconnect, an agent process crash, a daemon crash and a host reboot. Losing the host, or moving a factory to another host, is out of scope ([AssemblyAI#7](https://github.com/talvor/AssemblyAI/issues/7)).
55. **Orphans.** At start, the daemon terminates and records every agent process its previous instance left, and their assignments need reconciliation. It never tries to re-adopt them ([AssemblyAI#8](https://github.com/talvor/AssemblyAI/issues/8)).
56. **A leader crash.** A crashed leader is restarted automatically on the same provider, resuming its native session where possible, up to the leader restart bound. Past that bound its role holds and Coordination tells the user; if Coordination itself cannot be restored, `asmai status` reports it ([AssemblyAI#7](https://github.com/talvor/AssemblyAI/issues/7), [AssemblyAI#14](https://github.com/talvor/AssemblyAI/issues/14)).
57. **A worker crash.** A crashed worker is not restarted. Its assignment needs reconciliation, and its owning leader decides whether to dispatch again after checking effects. There is never a blind retry ([AssemblyAI#7](https://github.com/talvor/AssemblyAI/issues/7)).
58. **A provider CLI that fails to start** follows the leader crash rule for a leader; a worker's assignment needs reconciliation ([AssemblyAI#14](https://github.com/talvor/AssemblyAI/issues/14)).
59. **Workers outlive their leader's restart.** A worker keeps running through its leader's restart, and its result waits for the new leader generation's acceptance ([AssemblyAI#8](https://github.com/talvor/AssemblyAI/issues/8)).
60. **A daemon crash** goes through the same path as every start (rule 7) ([ADR 0001](https://github.com/talvor/AssemblyAI/blob/main/docs/adr/0001-daemon-owns-agent-terminals.md)).
61. **A host reboot** brings the factory back through the service, when installed, and then the same path ([AssemblyAI#7](https://github.com/talvor/AssemblyAI/issues/7)).
62. **A terminal or SSH disconnect** never stops agents, because the daemon owns their terminals. Detaching from an agent the user holds leaves it paused for input ([AssemblyAI#7](https://github.com/talvor/AssemblyAI/issues/7), [03](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/03-provider-sessions-and-terminals.md)).
63. **Unknown means reconcile.** Missing, conflicting or stale signals always mean unknown or needs reconciliation ([AssemblyAI#19](https://github.com/talvor/AssemblyAI/issues/19), [AssemblyAI#7](https://github.com/talvor/AssemblyAI/issues/7)).
64. **After a restore,** every open assignment needs reconciliation at the next start ([AssemblyAI#20](https://github.com/talvor/AssemblyAI/issues/20), [10](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/10-release-install-and-upgrade.md)).

## Interfaces

### Commands

[09](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/09-cli-and-configuration.md) gives each command's syntax and output ([AssemblyAI#9](https://github.com/talvor/AssemblyAI/issues/9)).

| Who | Command | Purpose |
| --- | --- | --- |
| The user | `asmai start [--foreground]` | Start the daemon (rules 5 to 7) |
| The user | `asmai stop [--now]` | Drain and stop (rule 9) |
| The user | `asmai service install\|uninstall\|status` | The optional service (rule 8) |
| The user | `asmai jobs`, `asmai job <n>`, `asmai agents` | Look at jobs and agents |
| The user | `asmai journal [--job\|--agent] [--follow]` | Read the journal |
| The user | `asmai export` | Write the journal out |
| The user | `asmai backup <file>` | A consistent copy of the store while running |
| Every agent | `asmai inbox`, `asmai inbox show` | Fetch messages (the delivery evidence); show one |
| Every agent | `asmai brief <job>` | The job's brief |
| Every agent | `asmai status`, `asmai jobs`, `asmai agents` | Read-only views |
| Workers and the delivering leader | `asmai effect <kind> <ref>` | Record an effect |
| Leaders | `asmai reconcile` | Record a reconciliation |

### Store records

| Record | Holds |
| --- | --- |
| Agent session | Its address (`name@role`), role, leader or worker, generation, provider and model, process group and state |
| Dispatch | Its assignment or message, the session generation it went to, its state, the bundle version and skill fingerprints, token counts, the transcript location and the recording |
| Observation | A hook event or other lifecycle signal, the dispatch it correlates to (if any), and when it arrived |
| Inbox message | Its ID, recipient, job and role, content, and when it was fetched |
| Effect | Its kind, reference, dispatch, and the agent or the daemon that made it |
| Reconciliation | What is known, what is not, and the choice (rule 47) |
| Journal entry | Every change above, in the transaction that made it |

[01](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/01-roles-and-decisions.md) lists the job, handoff, assignment, result and decision records.

### Files

- **The state directory**, `~/.local/state/asmai`, holds the store and everything else the factory keeps on the host: AsmAI's clones and workspaces ([05](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/05-repositories-and-job-branches.md)), recordings ([03](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/03-provider-sessions-and-terminals.md)), pre-migration backups and the daemon's copy of the executable ([10](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/10-release-install-and-upgrade.md)) ([AssemblyAI#9](https://github.com/talvor/AssemblyAI/issues/9), [AssemblyAI#20](https://github.com/talvor/AssemblyAI/issues/20)).
- **The configuration file** is `~/.config/asmai/config.toml` ([09](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/09-cli-and-configuration.md)).
- **The service definition** is a systemd user unit or a launchd LaunchAgent, written only by `asmai service install` (rule 8).

## Settings and defaults

[09](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/09-cli-and-configuration.md) gives each field's name and type; all are factory-wide ([AssemblyAI#14](https://github.com/talvor/AssemblyAI/issues/14)).

| Setting | Default | Rule |
| --- | --- | --- |
| Leader idle grace | 10 minutes | 52 |
| Leader restart bound | 3 restarts within 15 minutes | 56 |
| Silence timeout | 30 minutes ([07](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/07-limits-holds-and-visibility.md)) | 27 |
| Drain timeout | 10 minutes ([07](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/07-limits-holds-and-visibility.md)) | 9 |
| Automatic retries of a side-effect-free assignment | 2 ([07](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/07-limits-holds-and-visibility.md)) | 32 |

## Failure handling

| Failure | Handling |
| --- | --- |
| Agent process crash | Leader: restarted within the bound, then its role holds (rule 56). Worker: needs reconciliation (rule 57) |
| Daemon crash | Next start terminates orphans, restores leaders and reconciles (rules 7, 55) |
| Host reboot | The service restarts the daemon, then rule 7 (rule 61) |
| Terminal or SSH disconnect | Agents keep running (rule 62) |
| Unclean stop | Reconciliation at the next start (rule 11) |
| Dispatch silent past the timeout | Unknown; the owning leader is told; nothing killed or retried (rule 27) |
| Conflicting observations | Unknown (rule 28) |
| Call from a superseded generation | Rejected (rule 39) |
| Crash during an effect | Reconciliation against the real repository and GitHub (rules 44, 46) |
| No deliverable boundary | Messages wait in the inbox (rule 37) |
| Store unusable at start | Start refuses and explains ([10](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/10-release-install-and-upgrade.md)) |

## Qualification cases and proving scenarios

- **C15**: lost, duplicate, reordered and late hooks and observations (rules 25 to 28).
- **C16**: a superseded leader or worker generation is rejected (rules 39 to 41).
- **C17**: agent processes left by a previous daemon are terminated at start (rule 55).
- **C18**: a crash during an effect is recovered through reconciliation (rules 42 to 47).
- **C19**: dispatches and results stay correlated and reconcilable across restarts (rules 23 to 25).
- **C20**: a working dispatch with no observation for 30 minutes becomes unknown (rule 27).
- **C21**: agent crash: a leader restarts within its bound; a worker's assignment needs reconciliation (rules 56, 57).
- **C22**: daemon crash (rules 7, 60).
- **C23**: host reboot with the service installed (rules 8, 61).
- **C24**: terminal and SSH disconnect (rule 62; [03](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/03-provider-sessions-and-terminals.md) qualifies it).
- **C25**: `asmai stop` drains; `asmai stop --now` interrupts (rule 9).
- **C31**: leaders start when a message for their role arrives and stop after the idle grace (rules 51, 52).
- **S8** and **S9**: the daemon killed and the host rebooted mid-job; every affected assignment continues or has a recorded reconciliation, and no effect appears twice.
- **S1** and **S5**: the journal holds the evidence their checklists are checked from, including dispatches overlapping across three repositories.

## Sources

- [Choose factory hosting and lifecycle](https://github.com/talvor/AssemblyAI/issues/7#issuecomment-5976506834) (AssemblyAI#7)
- [Define work state and coordination contracts](https://github.com/talvor/AssemblyAI/issues/8#issuecomment-5976668034) (AssemblyAI#8)
- [Define CLI setup and management experience](https://github.com/talvor/AssemblyAI/issues/9#issuecomment-5979143255) (AssemblyAI#9)
- [Define concurrent repository work and integration](https://github.com/talvor/AssemblyAI/issues/11#issuecomment-5990301132) (AssemblyAI#11)
- [Define v1 acceptance scenarios and evidence](https://github.com/talvor/AssemblyAI/issues/12#issuecomment-5993314453) (AssemblyAI#12)
- [Define operating limits and visibility](https://github.com/talvor/AssemblyAI/issues/14#issuecomment-5991304507) (AssemblyAI#14)
- [Choose skill bundles and update policy](https://github.com/talvor/AssemblyAI/issues/17#issuecomment-5992055697) (AssemblyAI#17)
- [Choose validation and delivery ownership](https://github.com/talvor/AssemblyAI/issues/18#issuecomment-5992792804) (AssemblyAI#18)
- [Validate interactive CLI coordination and intervention](https://github.com/talvor/AssemblyAI/issues/19#issuecomment-5976021294) (AssemblyAI#19)
- [Choose license, release packaging and upgrade migration](https://github.com/talvor/AssemblyAI/issues/20#issuecomment-6004145724) (AssemblyAI#20)
- [ADR 0001](https://github.com/talvor/AssemblyAI/blob/main/docs/adr/0001-daemon-owns-agent-terminals.md), [ADR 0002](https://github.com/talvor/AssemblyAI/blob/main/docs/adr/0002-agents-coordinate-through-asmai-cli.md), [ADR 0007](https://github.com/talvor/AssemblyAI/blob/main/docs/adr/0007-asmai-delivers-tested-prs-with-its-own-roles.md) and the [glossary](https://github.com/talvor/AssemblyAI/blob/main/GLOSSARY.md): Host, Store, Job, Dispatch, Reconciliation, Hold.
- The review of this document: [questions](https://github.com/talvor/AssemblyAI/blob/main/.lavish/spec-doc-02-round1-questions.json) and [answers](https://github.com/talvor/AssemblyAI/blob/main/.lavish/spec-doc-02-answers.json).
