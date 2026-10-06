# 11 Qualification and proving

This document specifies what must pass before v1 launches and how it is shown: development tests, the qualification harness and its separate OS user, fault injection and replay, the fixture repository, the 47 qualification cases, the qualification record and `asmai doctor`'s self-check, and the nine proving scenarios with their checklists, verdicts and record. [10 Release, install and upgrade](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/10-release-install-and-upgrade.md) specifies how the record goes into a release.

## Rules

### The two gates

1. **Qualification and proving.** v1 launches after two gates ([AssemblyAI#12](https://github.com/talvor/AssemblyAI/issues/12)):
   - **qualification**: the qualification cases pass for the release's pinned Claude Code, Codex and Lavish on a platform, which certifies that platform;
   - **proving scenarios**: nine scenarios run end to end on real repositories with real tasks, on a certified platform, and the user gives a verdict on each.
2. **Launch.** v1.0.0 launches when Linux x86_64 is certified and every proving scenario has passed. macOS follows when it is certified, in a later release ([AssemblyAI#12](https://github.com/talvor/AssemblyAI/issues/12), [AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27)).
3. **No burn-in.** Nothing a burn-in period would find holds up the launch; it becomes a fix in a later release ([AssemblyAI#12](https://github.com/talvor/AssemblyAI/issues/12)).

### Development tests

4. **On every PR.** Every pull request to talvor/asmai runs development tests in hosted CI, on Linux and on GitHub's hosted macOS runners ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27)).
5. **A scripted fake provider.** Development tests use a scripted fake provider CLI that plays hook payloads and screens recorded from the real pinned versions. The fake never counts toward qualification and never certifies a combination ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27), [ADR 0008](https://github.com/talvor/AssemblyAI/blob/main/docs/adr/0008-qualification-runs-real-provider-clis-on-real-hosts.md)).

### The harness

6. **Real providers on a real host.** A qualification harness drives the release's real pinned providers on a real host of each platform, under a separate OS user with its own sign-in and its own factory, so sign-out and crash tests never touch the user's own sessions or factory ([AssemblyAI#12](https://github.com/talvor/AssemblyAI/issues/12), [ADR 0008](https://github.com/talvor/AssemblyAI/blob/main/docs/adr/0008-qualification-runs-real-provider-clis-on-real-hosts.md)).
7. **Where it lives.** The harness lives in talvor/asmai, in its own directory, and is built only into development builds, never into a release executable, so it and the code it qualifies always share a commit ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27)).
8. **Faults are injected.** Crashes, and lost, duplicate, reordered and late hooks, are injected. Provider outages come from blocking an agent's network. Native modals are opened on purpose ([AssemblyAI#12](https://github.com/talvor/AssemblyAI/issues/12)).
9. **Replay only what cannot be caused.** Recorded provider payloads are replayed only for what cannot be produced on demand: an allowance running out, and a modal the provider chooses when to show. Those cases are marked as replayed ([AssemblyAI#12](https://github.com/talvor/AssemblyAI/issues/12), [ADR 0008](https://github.com/talvor/AssemblyAI/blob/main/docs/adr/0008-qualification-runs-real-provider-clis-on-real-hosts.md)).
10. **The fixture repository.** Delivery cases run against a GitHub fixture repository that Phillip owns, separate from talvor/asmai (for example talvor/asmai-fixture), whose CI can be made red, slow or absent. If no repository available to the harness refuses a draft pull request, the refusal is simulated at the gh boundary ([AssemblyAI#12](https://github.com/talvor/AssemblyAI/issues/12), [AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27)).
11. **The hosts.** M0 sets up the harness's separate OS users on this host and on a Mac Phillip already has ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27)).

### Running qualification

12. **Per combination or per platform.** A case that depends on the provider runs for each combination of pinned versions; the others run once per platform ([AssemblyAI#12](https://github.com/talvor/AssemblyAI/issues/12)).
13. **What passes.** A case passes when AsmAI behaves as decided, through the provider's own signal or, when that signal is missing, through AsmAI's safe default. The missing signal is recorded as a known limitation, which `asmai doctor` lists ([AssemblyAI#12](https://github.com/talvor/AssemblyAI/issues/12), [ADR 0008](https://github.com/talvor/AssemblyAI/blob/main/docs/adr/0008-qualification-runs-real-provider-clis-on-real-hosts.md)).
14. **What fails.** A case fails when AsmAI does anything unsafe: types over a modal or over the user; loses or misattributes a decision; repeats an effect blindly; force-pushes over commits it did not make; or reports work as done when it is not. Any failing case leaves the combination unqualified ([AssemblyAI#12](https://github.com/talvor/AssemblyAI/issues/12)).
15. **Who and when.** The maintainer runs the harness on a real host of each certified platform before each AsmAI release, and again whenever a pinned version changes ([AssemblyAI#12](https://github.com/talvor/AssemblyAI/issues/12), [ADR 0008](https://github.com/talvor/AssemblyAI/blob/main/docs/adr/0008-qualification-runs-real-provider-clis-on-real-hosts.md)).
16. **Never in hosted CI, and no command.** Nothing qualifies in hosted CI, because provider sign-in never leaves the user's host, and there is no `asmai qualify` command ([AssemblyAI#12](https://github.com/talvor/AssemblyAI/issues/12), [ADR 0008](https://github.com/talvor/AssemblyAI/blob/main/docs/adr/0008-qualification-runs-real-provider-clis-on-real-hosts.md)).
17. **Terminals.** Ghostty is qualified on each certified platform, both locally and over SSH to a remote host. Other terminals and multiplexers are best effort, and `asmai doctor` says so ([AssemblyAI#12](https://github.com/talvor/AssemblyAI/issues/12)).
18. **macOS alongside.** At the end of each milestone, its cases also run in the harness on the Mac. A macOS failure becomes a ticket in the next milestone and never holds up the Linux release candidate ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27)).

### The qualification record

19. **What it holds:** the qualified combinations of pinned versions, the certified platforms, and the known limitations ([AssemblyAI#12](https://github.com/talvor/AssemblyAI/issues/12)).
20. **Inside the release.** The harness produces the record from a development build of the candidate commit; the maintainer commits it, and the release is that commit ([ADR 0009](https://github.com/talvor/AssemblyAI/blob/main/docs/adr/0009-a-release-is-the-qualified-commit-plus-its-record.md), [10](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/10-release-install-and-upgrade.md)).
21. **Enforced.** `asmai start` refuses anything outside the record, and `asmai doctor` shows it ([AssemblyAI#12](https://github.com/talvor/AssemblyAI/issues/12), [ADR 0008](https://github.com/talvor/AssemblyAI/blob/main/docs/adr/0008-qualification-runs-real-provider-clis-on-real-hosts.md)).
22. **A platform** is an operating system and CPU architecture, Linux x86_64 first ([AssemblyAI#12](https://github.com/talvor/AssemblyAI/issues/12)).
23. **The user's host is not qualified again.** `asmai doctor` runs a short read-only self-check there ([AssemblyAI#12](https://github.com/talvor/AssemblyAI/issues/12)).

### The 47 qualification cases

24. **All 47 are the v1 qualification cases.** Each is listed with the documents whose rules it qualifies and the milestone at whose end it first passes; all 47 run together on the candidate commit in M8 and again on Linux x86_64 for the launch ([AssemblyAI#12](https://github.com/talvor/AssemblyAI/issues/12), [AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27), [00](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/00-overview.md)).

| Case | What is qualified | Document | Milestone |
| --- | --- | --- | --- |
| **Platform and installation** | | | |
| C1 | Platform certification on Linux and on macOS; an uncertified platform refuses to start agents and says what to do | 09 | M2 |
| C2 | An unqualified provider version is refused before any dispatch; a provider CLI that upgraded itself holds its agent at the next restart | 03 | M2 |
| C3 | The pinned provider copies reuse the user's existing sign-in without a new login | 03 | M1 |
| C4 | Every agent session starts without provider API-key variables | 03 | M1 |
| C5 | Codex hook trust survives an AsmAI upgrade | 10 | M8 |
| **Terminals, input and intervention** | | | |
| C6 | Native modals: any input state not on the allow-list (which starts empty) holds the agent instead of being typed over | 03 | M4 |
| C7 | Positive acknowledgment of each automated submission, never inferred from a successful PTY write | 03 | M1 |
| C8 | Taking an agent mid-turn and with an unsent automated draft: wait for the boundary or interrupt; the draft is recorded and cleared | 03 | M4 |
| C9 | The attach client's rendering of each provider's screen under the status line, at reduced height | 03 | M4 |
| C10 | Detecting the user's unsent text in the conversation and clearing the input box | 04 | M4 |
| C11 | Capturing witnessed messages and telling them apart from the daemon's nudges | 03 | M1 |
| C12 | Recognising an interrupted Claude turn (the probe saw no Interrupt hook from Claude) | 03 | M4 |
| C13 | A second attach takes over; the older terminal only observes and its unsent text is saved | 04 | M4 |
| C14 | Terminal recording per dispatch, and replay | 03 | M4 |
| **Signals and work state** | | | |
| C15 | Lost, duplicate, reordered and late hooks and observations | 02 | M6 |
| C16 | A superseded leader or worker generation is rejected | 02 | M6 |
| C17 | Agent processes left by a previous daemon are terminated at start | 02 | M6 |
| C18 | A crash during an effect is recovered through reconciliation | 02 | M6 |
| C19 | Dispatches and results stay correlated and reconcilable across restarts | 02 | M1 |
| C20 | A working dispatch with no observation for 30 minutes becomes unknown | 02 | M6 |
| **Recovery and stopping** | | | |
| C21 | Agent crash: a leader restarts within its bound; a worker's assignment needs reconciliation | 02 | M6 |
| C22 | Daemon crash | 02 | M6 |
| C23 | Host reboot with the service installed | 02 | M6 |
| C24 | Terminal and SSH disconnect | 03 | M6 |
| C25 | `asmai stop` drains; `asmai stop --now` interrupts | 02 | M6 |
| **Providers, access and allowance** | | | |
| C26 | Expired or revoked sign-in holds work, shows the native sign-in command, and resumes when sign-in is back | 07 | M5 |
| C27 | Allowance used and reset times, for each provider | 07 | M5 |
| C28 | Allowance used up: agents hold, then resume at the reset (replayed) | 07 | M5 |
| C29 | A reported provider error resumes with backoff (Claude's StopFailure; Codex's equivalent is unknown); past the bound the provider is unavailable | 07 | M5 |
| C30 | Fallback to the other provider only before first dispatch, including a leader's on-demand start; afterwards the user is asked | 07 | M5 |
| C31 | Leaders start when a message for their role arrives and stop after the idle grace | 02 | M5 |
| C32 | Below the free-space floor no new workspace is created | 07 | M5 |
| **Skills** | | | |
| C33 | Personal, provider built-in and repository skills are hidden, including Claude's built-in code-review next to the shipped one | 08 | M2 |
| C34 | Per-session skill delivery works although Claude namespaces plugin skills and upstream skills call each other by bare name | 08 | M2 |
| C35 | Codex finds the skills written into its workspace | 08 | M2 |
| **Repository work** | | | |
| C36 | Instruction files load without the repository's provider configuration | 05 | M1 |
| C37 | Provider write guards are switched on | 05 | M1 |
| C38 | Concurrent jobs in one repository | 05 | M5 |
| C39 | Outside commits are merged in and never force-pushed over | 05 | M5 |
| C40 | A crash during a push | 06 | M6 |
| **Delivery** | | | |
| C41 | The daemon's push, and its refusal when origin holds commits AsmAI did not make | 06 | M1 |
| C42 | A draft pull request, and the "[not ready]" fallback when GitHub refuses a draft | 06 | M1 |
| C43 | CI watched through gh: green; red with one judged re-run; a newer push replacing the wait | 06 | M1 |
| C44 | The 15-minute wait for a first check, and the hold for a repository with no declared CI | 06 | M5 |
| C45 | Marking the pull request ready when CI is green | 06 | M1 |
| C46 | A leader-opened pull request reconciled as an effect, including a crash between the push and the pull request | 06 | M6 |
| **Remote hosts** | | | |
| C47 | Remote use over SSH: `--host`, Lavish through port forwarding, and plain `ssh -t host asmai` | 09 | M7 |

### The proving ground

25. **talvor/asmai** carries the headline feature, AsmAI's v2 notify command, whose design is kept in [AssemblyAI#14](https://github.com/talvor/AssemblyAI/issues/14). The user asks for it in the conversation as a new feature. Planning asks its questions in Lavish and writes the specification and tickets, Engineering implements them in several assignments, Quality validates, and it ends as a tested pull request that the user may merge or keep for v2. Jobs work in AsmAI's own clone, so working on AsmAI's code never touches the running executable ([AssemblyAI#12](https://github.com/talvor/AssemblyAI/issues/12), [AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27)).
26. **otman** carries concurrent work in a second repository, and **dev-setup**, which has no CI workflow, carries the no-CI path ([AssemblyAI#12](https://github.com/talvor/AssemblyAI/issues/12)).
27. **Standalone tasks are real AsmAI work** ([AssemblyAI#12](https://github.com/talvor/AssemblyAI/issues/12), [AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27)):
    - **Research:** an open fact AsmAI needs, such as whether a newer Codex offers a StopFailure-like signal or a per-session skill folder, delivered as notes.
    - **Planning:** the user and a Planning worker resolve one real Wayfinder ticket of AsmAI's next map, with its questions in Lavish. The next map and its Wayfinder tickets are issues in talvor/asmai, and S3 resolves one of them there ([answers](https://github.com/talvor/AssemblyAI/blob/main/.lavish/spec-doc-11-answers.json)).
    - **Diagnosis:** the first real defect found during qualification or the proving scenarios, diagnosed and then fixed as a tested pull request in talvor/asmai.
    - One of the research or diagnosis jobs runs without a repository.
28. **AsmAI works on itself from the release candidate.** The proving scenarios are where AsmAI first works on its own code ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27)).

### The proving scenarios

29. **Providers across the scenarios.** Across all nine, each role runs at least once on Claude and once on Codex, and S1 mixes providers inside one job, for example Engineering workers on Codex and Quality on Claude ([AssemblyAI#12](https://github.com/talvor/AssemblyAI/issues/12)).
30. **The nine** ([AssemblyAI#12](https://github.com/talvor/AssemblyAI/issues/12)):
    - **S1 Feature to tested PR:** the headline feature, from the user's request to a tested pull request: Planning's questions in Lavish, a specification and tickets, several Engineering assignments, Quality's validation at the exact head, the daemon's push, a draft pull request, green CI, the ready mark, and the link reported.
    - **S2 Research:** a research job delivered as notes, with its sources.
    - **S3 Planning:** a Wayfinder ticket resolved with the user in Lavish, its resolution recorded in the tracker.
    - **S4 Diagnosis:** a real defect diagnosed, then fixed as a tested pull request.
    - **S5 Concurrent repositories:** S1 runs while jobs run in two other repositories. A second job in S1's repository meets a conflict that a worker resolves, and full worker caps queue assignments.
    - **S6 No CI:** a small real change in a repository declared as having no CI, delivered with Quality's checks standing in and the gap stated in the pull request.
    - **S7 Human decisions,** during the other scenarios: a choice between distinct viable approaches answered in the conversation; a request with several questions answered in Lavish; an intervention where the user takes a worker, types a correction and releases it; independent work continuing while a decision is pending; one job paused and resumed, and another cancelled.
    - **S8 Local continuity:** during S1 the user leaves and comes back to a catch-up, the daemon is killed, and the host reboots with the service installed. Work continues after reconciliation, and no effect is repeated.
    - **S9 Remote continuity:** a job on a remote host driven with `asmai --host`. SSH drops mid-turn, the user reconnects and answers a Lavish decision through port forwarding, and the remote host reboots.
31. **The remote host for S9** is a virtual machine Phillip sets up, on this host or elsewhere, when S9 is about to run; setting it up blocks nothing before then. S9 stays a launch requirement, together with C47 ([AssemblyAI#12](https://github.com/talvor/AssemblyAI/issues/12)).

### Evidence and verdict

32. **Checklist plus verdict.** A scenario passes when its evidence checklist is complete and the user's verdict is not "not usable". The verdict is one of "usable as delivered", "usable after my changes" or "not usable" ([AssemblyAI#12](https://github.com/talvor/AssemblyAI/issues/12)).
33. **Where the evidence comes from.** The checklists are checked from the job's journal export (`asmai export`), the pull request and its CI, and the terminal recordings ([AssemblyAI#12](https://github.com/talvor/AssemblyAI/issues/12)).
34. **Common to every scenario.** It runs on a certified platform with a qualified combination, and its journal export and recordings are kept with its record ([AssemblyAI#12](https://github.com/talvor/AssemblyAI/issues/12)).
35. **The checklists** ([AssemblyAI#12](https://github.com/talvor/AssemblyAI/issues/12)):

| Scenario | Evidence |
| --- | --- |
| S1 | The job opened from the user's witnessed message, with its mandate and acceptance criteria. Planning's questions reached the user in Lavish, and the answers are recorded word for word; the specification and tickets are in the tracker. At least two writing assignments were accepted, each result naming its tests and checks, and at least one role ran on each provider. Quality's report names the exact head commit, with no blocking finding left. The push, the draft pull request, green CI on that head and the ready mark are each in the journal, and the PR body carries the AsmAI section. Coordination reported the link, and the job ended. |
| S2 | The notes are delivered (as a pull request, or in the scratch workspace for a job without a repository), with every claim tied to a cited source. The Research leader accepted them against the mandate. |
| S3 | Every question reached the user as a Lavish decision request, and each recorded answer cites the user's own Lavish answer or witnessed message. No agent supplied an answer. The resolution is recorded in the tracker. |
| S4 | A reproduction is recorded before the fix, and the fix meets S1's tested-PR evidence. |
| S5 | The journal shows dispatches overlapping in three repositories. A worker resolved the conflict inside an assignment. Queued assignments were shown as queued, started first come first served, and never overflowed to the other provider. |
| S6 | The repository's no-CI declaration is recorded, the PR body says that Quality's checks stand in, and there was no 15-minute wait and no hold. |
| S7 | Each decision version had one answer surface. Each record attributed to the user cites a witnessed message or Lavish answer given after that version was shown. The journal shows independent work continuing while a decision was pending. The intervention record reached the owning leader, followed by a new dispatch. Pause, resume and cancel each left their reported state. |
| S8 | The catch-up was shown on the user's return. After the daemon was killed and the host rebooted, each affected assignment either continued or has a recorded reconciliation. No effect appears twice in the journal or on GitHub, and the job still ended as a tested pull request. |
| S9 | S8's evidence for the remote host, plus a Lavish answer given through the forwarded port and recorded, and the SSH drop leaving delivery running. |

36. **The record.** Each release's results go in a record of the proving scenarios in talvor/asmai, beside the releases it judges, quoting the user's verdicts. Each scenario's record also states its elapsed time, the user's time spent answering, and the allowance used; these are recorded, not pass conditions ([AssemblyAI#12](https://github.com/talvor/AssemblyAI/issues/12), [AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27)).
37. **Later releases** rerun a scenario only when they change what it proves; for example, a delivery change reruns S1. Qualification covers everything else ([AssemblyAI#12](https://github.com/talvor/AssemblyAI/issues/12)).

### Proving and launch

38. **After M8.** The proving scenarios run on the release candidate, with Phillip's verdicts; AsmAI builds the v2 notify command (S1) and fixes a real defect (S4) in talvor/asmai; all 47 cases pass on Linux x86_64; and v1.0.0 is released on Linux. macOS is certified by a later release ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27)). The milestone at whose end each scenario first becomes possible is in [00](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/00-overview.md).

## Interfaces

### Commands

| Who | Command | Purpose |
| --- | --- | --- |
| The user | `asmai doctor` | The qualification record, known limitations and the self-check (rules 21, 23) |
| The user | `asmai export` | The journal export the checklists are checked from (rule 33) |
| The user | `asmai replay` | The recordings kept as evidence (rule 33) |
| The maintainer | The harness, in a development build | Runs the qualification cases (rules 6 to 16) |

### Files

| File | Where | Holds |
| --- | --- | --- |
| The qualification record | Committed in talvor/asmai and embedded in the release | Rule 19 |
| The harness | Its own directory in talvor/asmai; development builds only | Rule 7 |
| Recorded payloads and screens | talvor/asmai | What the fake provider plays (rule 5) and what replayed cases use (rule 9) |
| The proving-scenario record | talvor/asmai, beside the releases | Each scenario's checklist, verdict, elapsed time, the user's time and the allowance used, with its journal export and recordings (rules 34, 36) |

## Settings and defaults

None; qualification runs a development build under the harness's own OS user and its own configuration.

## Failure handling

| Failure | Handling |
| --- | --- |
| A case fails | The combination stays unqualified; nothing is released for it (rule 14) |
| A provider signal is missing but the safe default holds | The case passes; the gap is a known limitation listed by `asmai doctor` (rule 13) |
| A macOS failure at a milestone's end | A ticket in the next milestone; the Linux release candidate is not held (rule 18) |
| A scenario's verdict is "not usable" | It does not pass; launch waits for a fix and a rerun (rules 2, 32) |
| A defect found during qualification or proving | It is S4's diagnosis task (rule 27) |

## Qualification cases and proving scenarios

This document holds all 47 cases (rule 24) and all nine scenarios (rule 30).

## Sources

- [Validate interactive CLI coordination and intervention](https://github.com/talvor/AssemblyAI/issues/19#issuecomment-5976021294) (AssemblyAI#19), whose qualification gaps the cases cover
- [Define v1 acceptance scenarios and evidence](https://github.com/talvor/AssemblyAI/issues/12#issuecomment-5993314453) (AssemblyAI#12), with its [gathered cases](https://github.com/talvor/AssemblyAI/blob/main/.lavish/acceptance-cases.md) and [answers](https://github.com/talvor/AssemblyAI/blob/main/.lavish/acceptance-answers.json)
- [Define operating limits and visibility](https://github.com/talvor/AssemblyAI/issues/14#issuecomment-5991304507) (AssemblyAI#14), for the notify command's design
- [Choose the specification's structure and implementation sequence](https://github.com/talvor/AssemblyAI/issues/27#issuecomment-6004852593) (AssemblyAI#27)
- [ADR 0008](https://github.com/talvor/AssemblyAI/blob/main/docs/adr/0008-qualification-runs-real-provider-clis-on-real-hosts.md), [ADR 0009](https://github.com/talvor/AssemblyAI/blob/main/docs/adr/0009-a-release-is-the-qualified-commit-plus-its-record.md) and the [glossary](https://github.com/talvor/AssemblyAI/blob/main/GLOSSARY.md): Qualification, Certified platform, Qualification record, Known limitation, Proving scenario, Proving ground.
- The review of this document: [questions](https://github.com/talvor/AssemblyAI/blob/main/.lavish/spec-doc-11-round1-questions.json) and [answers](https://github.com/talvor/AssemblyAI/blob/main/.lavish/spec-doc-11-answers.json).
