## Resolution — confirmed by Phillip in Lavish

### Scope
This ticket settles which real tasks and observable evidence prove that v1 is useful, and what must pass before it launches. [Choose validation and delivery ownership](https://github.com/talvor/AssemblyAI/issues/18) had already settled what tested and ready for review mean. This ticket also settles how the 47 cases that nine earlier tickets deferred here are qualified, including the delivery mechanics from that ticket.

### What has to pass before v1 launches
- **Two gates.**
  - **Qualification:** the qualification cases pass for the release's pinned Claude Code, Codex and Lavish on a platform, which certifies that platform.
  - **Proving scenarios:** nine scenarios run end to end on real repositories with real tasks, on a certified platform, and Phillip gives a verdict on each.
- **Launch.** v1 launches when Linux is certified and every proving scenario has passed. macOS follows when it is certified.
- **No burn-in.** Nothing a burn-in period would find holds up launch; it becomes a fix in a later release.

### The proving ground
- **AssemblyAI** carries the headline feature: AsmAI's v2 notify command, whose design is kept in [Define operating limits and visibility](https://github.com/talvor/AssemblyAI/issues/14). Phillip asks for it in the conversation as a new feature. Planning asks him its questions in Lavish and writes the spec and tickets, Engineering implements them in several assignments, Quality validates, and it ends as a tested PR that he may merge or keep for v2. Jobs work in AsmAI's own clone, so working on AsmAI's code never touches the running executable.
- **otman** carries concurrent work in a second repository.
- **dev-setup**, which has no CI workflow, carries the no-CI path.
- **Standalone tasks are real AsmAI work:**
  - Research: an open fact AsmAI needs, such as whether a newer Codex offers a StopFailure-like signal or a per-session skill folder, delivered as notes.
  - Planning: Phillip and a Planning worker resolve one real Wayfinder ticket of AsmAI's next map, with its questions in Lavish.
  - Diagnosis: the first real defect found during qualification or the proving scenarios, diagnosed and then fixed as a tested PR.
  - One of the research or diagnosis jobs runs without a repository.

### The proving scenarios
Across all nine, each role runs at least once on Claude and once on Codex, and S1 mixes providers inside one job, for example Engineering workers on Codex and Quality on Claude.
- **S1 Feature to tested PR:** the headline feature, from Phillip's request to a tested PR. Planning's questions in Lavish, a spec and tickets, several Engineering assignments, Quality validation at the exact head, the daemon's push, a draft PR, green CI, marked ready, and the link reported.
- **S2 Research:** a research job delivered as notes, with its sources.
- **S3 Planning:** a Wayfinder ticket resolved with Phillip in Lavish, its resolution recorded in the tracker.
- **S4 Diagnosis:** a real defect diagnosed, then fixed as a tested PR.
- **S5 Concurrent repositories:** S1 runs while jobs run in two other repositories. A second job in S1's repository meets a conflict that a worker resolves, and full worker caps queue assignments.
- **S6 No CI:** a small real change in a repository declared as having no CI, delivered with Quality's checks standing in and the gap stated in the PR.
- **S7 Human decisions:** during the other scenarios:
  - a choice between distinct viable approaches answered in the conversation;
  - a request with several questions answered in Lavish;
  - an intervention where Phillip takes a worker, types a correction and releases it;
  - independent work continuing while a decision is pending;
  - one job paused and resumed, and another cancelled.
- **S8 Local continuity:** during S1 Phillip leaves and comes back to a catch-up, the daemon is killed, and the host reboots with the service installed. Work continues after reconciliation, and no effect is repeated.
- **S9 Remote continuity:** a job on a remote host driven with `asmai --host`. SSH drops mid-turn, Phillip reconnects and answers a Lavish decision through port forwarding, and the remote host reboots.

### The remote host for S9
- **S9 stays a launch requirement**, and launch waits for it, together with case C47.
- **The host is a virtual machine** that Phillip sets up, on this host or elsewhere, rather than a separate physical machine.
- **Setting it up blocks nothing** until S9 is about to run.

### Evidence and verdict
- **Checklist plus verdict.** A scenario passes when its evidence checklist is complete and Phillip's verdict is not "not usable". The verdict is one of "usable as delivered", "usable after my changes" or "not usable".
- **Where the evidence comes from.** The checklists are checked from the job's journal export (`asmai export`), the PR and its CI, and the terminal recordings.
- **Common to every scenario.** It runs on a certified platform with a qualified combination, and its journal export and recordings are kept with its record.
- **The record.** Each release's results go in a record of the proving scenarios in the AssemblyAI repository, quoting Phillip's verdicts. Each scenario's record also states its elapsed time, Phillip's time spent answering, and the allowance used. These are recorded, not a pass condition.
- **The checklists:**
  - **S1:**
    - The job opened from Phillip's witnessed message, with its mandate and acceptance criteria.
    - Planning's questions reached him in Lavish, and his answers are recorded word for word. The spec and tickets are in the tracker.
    - At least two writing assignments were accepted, each result naming its tests and checks, and at least one role ran on each provider.
    - Quality's report names the exact head commit, with no blocking finding left.
    - The push, the draft PR, green CI on that head and the ready mark are each in the journal. The PR body carries the AsmAI section.
    - Coordination reported the link, and the job ended.
  - **S2:** the notes are delivered (as a PR, or in the scratch workspace for a job without a repository), with every claim tied to a cited source. The Research leader accepted them against the mandate.
  - **S3:** every question reached Phillip as a Lavish decision request, and each recorded answer cites his own Lavish answer or witnessed message. No agent supplied an answer. The resolution is recorded in the tracker.
  - **S4:** a reproduction is recorded before the fix, and the fix meets S1's tested-PR evidence.
  - **S5:** the journal shows dispatches overlapping in three repositories. A worker resolved the conflict inside an assignment. Queued assignments were shown as queued, started first come first served, and never overflowed to the other provider.
  - **S6:** the repository's no-CI declaration is recorded, the PR body says that Quality's checks stand in, and there was no 15-minute wait and no hold.
  - **S7:**
    - Each decision version had one answer surface.
    - Each record attributed to Phillip cites a witnessed message or Lavish answer given after that version was shown.
    - The journal shows independent work continuing while a decision was pending.
    - The intervention record reached the owning leader, followed by a new dispatch.
    - Pause, resume and cancel each left their reported state.
  - **S8:** the catch-up was shown on his return. After the daemon was killed and the host rebooted, each affected assignment either continued or has a recorded reconciliation. No effect appears twice in the journal or on GitHub, and the job still ended as a tested PR.
  - **S9:** S8's evidence for the remote host, plus a Lavish answer given through the forwarded port and recorded, and the SSH drop leaving delivery running.

### Later releases
The proving scenarios gate v1. A later release reruns a scenario only when it changes what that scenario proves; for example, a delivery change reruns S1. Qualification covers everything else.

### Qualification
- **The list.** All 47 cases below are the v1 qualification cases. A case that depends on the provider runs for each combination of pinned versions; the others run once per platform.
- **How they are exercised.**
  - A qualification harness drives the real pinned providers on a real host, under a separate OS user with its own sign-in and its own factory. Sign-out and crash tests therefore never touch Phillip's own sessions or factory.
  - Crashes, and lost, duplicate, reordered and late hooks, are injected. Provider outages come from blocking an agent's network. Native modals are opened on purpose.
  - Recorded provider payloads are replayed only for what cannot be produced on demand: an allowance running out, and a modal the provider chooses to show. Those cases are marked as replayed.
  - Delivery cases run against a GitHub fixture repository Phillip owns, whose CI can be made red, slow or absent. If no repository available to the harness refuses a draft PR, the refusal is simulated at the `gh` boundary.
- **What passes.**
  - A case passes when AsmAI behaves as decided, through the provider's own signal or, when the signal is missing, through the safe default. The missing signal is recorded as a known limitation, which `asmai doctor` lists.
  - A case fails when AsmAI does anything unsafe:
    - types over a modal or over Phillip;
    - loses or misattributes a decision;
    - repeats an effect blindly;
    - force-pushes over commits it did not make;
    - reports work as done when it is not.
  - Any failing case leaves the combination unqualified.
- **Who runs it, and what a release carries.**
  - The maintainer runs the harness on a real host of each certified platform before each AsmAI release, and again whenever a pinned version changes.
  - The release carries a qualification record: the qualified combinations, the certified platforms and the known limitations. `asmai start` refuses anything else, and `asmai doctor` shows the record.
  - A platform is an operating system and CPU architecture, Linux x86_64 first.
  - A user's own host is not qualified again; `asmai doctor` runs a short read-only self-check there.
  - There is no `asmai qualify` command, and nothing runs in hosted CI.
- **Terminals.** Ghostty is qualified on each certified platform, both locally and over SSH to a remote host. Other terminals and multiplexers are best effort, and `asmai doctor` says so.

#### The 47 qualification cases
- **Platform and installation**, deferred by [Choose factory hosting and lifecycle](https://github.com/talvor/AssemblyAI/issues/7); [Define CLI setup and management experience](https://github.com/talvor/AssemblyAI/issues/9):
  - C1: Platform certification on Linux and on macOS; an uncertified platform refuses to start agents and says what to do.
  - C2: An unqualified provider version is refused before any dispatch; a provider CLI that upgraded itself holds its agent at the next restart.
  - C3: The pinned provider copies reuse your existing sign-in without a new login.
  - C4: Every agent session starts without provider API-key variables.
  - C5: Codex hook trust survives an AsmAI upgrade.
- **Terminals, input and intervention**, deferred by [Validate interactive CLI coordination and intervention](https://github.com/talvor/AssemblyAI/issues/19); [Choose factory hosting and lifecycle](https://github.com/talvor/AssemblyAI/issues/7); [Explore terminal conversation and Lavish decision flow](https://github.com/talvor/AssemblyAI/issues/10); [Define operating limits and visibility](https://github.com/talvor/AssemblyAI/issues/14):
  - C6: Native modals: any input state not on the allow-list (which starts empty) holds the agent instead of being typed over.
  - C7: Positive acknowledgment of each automated submission, never inferred from a successful PTY write.
  - C8: Taking an agent mid-turn and with an unsent automated draft: wait for the boundary or interrupt; the draft is recorded and cleared.
  - C9: The attach client's rendering of each provider's screen under the status line, at reduced height.
  - C10: Detecting your unsent text in the conversation and clearing the input box.
  - C11: Capturing witnessed messages and telling them apart from the daemon's nudges.
  - C12: Recognising an interrupted Claude turn (the probe saw no Interrupt hook from Claude).
  - C13: A second attach takes over; the older terminal only observes and its unsent text is saved.
  - C14: Terminal recording per dispatch, and replay.
- **Signals and work state**, deferred by [Define work state and coordination contracts](https://github.com/talvor/AssemblyAI/issues/8); [Validate interactive CLI coordination and intervention](https://github.com/talvor/AssemblyAI/issues/19); [Choose factory hosting and lifecycle](https://github.com/talvor/AssemblyAI/issues/7); [Define operating limits and visibility](https://github.com/talvor/AssemblyAI/issues/14):
  - C15: Lost, duplicate, reordered and late hooks and observations.
  - C16: A superseded leader or worker generation is rejected.
  - C17: Agent processes left by a previous daemon are terminated at start.
  - C18: A crash during an effect is recovered through reconciliation.
  - C19: Dispatches and results stay correlated and reconcilable across restarts.
  - C20: A working dispatch with no observation for 30 minutes becomes unknown.
- **Recovery and stopping**, deferred by [Choose factory hosting and lifecycle](https://github.com/talvor/AssemblyAI/issues/7):
  - C21: Agent crash: a leader restarts within its bound; a worker's assignment needs reconciliation.
  - C22: Daemon crash.
  - C23: Host reboot with the service installed.
  - C24: Terminal and SSH disconnect.
  - C25: `asmai stop` drains; `asmai stop --now` interrupts.
- **Providers, access and allowance**, deferred by [Validate interactive CLI coordination and intervention](https://github.com/talvor/AssemblyAI/issues/19); [Define operating limits and visibility](https://github.com/talvor/AssemblyAI/issues/14); [Choose runtime adapters and authentication](https://github.com/talvor/AssemblyAI/issues/15):
  - C26: Expired or revoked sign-in holds work, shows the native sign-in command, and resumes when sign-in is back.
  - C27: Allowance used and reset times, for each provider.
  - C28: Allowance used up: agents hold, then resume at the reset.
  - C29: A reported provider error resumes with backoff (Claude's StopFailure; Codex's equivalent is unknown); past the bound the provider is unavailable.
  - C30: Fallback to the other provider only before first dispatch, including a leader's on-demand start; afterwards you are asked.
  - C31: Leaders start when a message for their role arrives and stop after the idle grace.
  - C32: Below the free-space floor no new workspace is created.
- **Skills**, deferred by [Choose skill bundles and update policy](https://github.com/talvor/AssemblyAI/issues/17):
  - C33: Personal, provider built-in and repository skills are hidden, including Claude's built-in code-review next to the shipped one.
  - C34: Per-session skill delivery works although Claude namespaces plugin skills and upstream skills call each other by bare name.
  - C35: Codex finds the skills written into its workspace.
- **Repository work**, deferred by [Define concurrent repository work and integration](https://github.com/talvor/AssemblyAI/issues/11):
  - C36: Instruction files load without the repository's provider configuration.
  - C37: Provider write guards are switched on.
  - C38: Concurrent jobs in one repository.
  - C39: Outside commits are merged in and never force-pushed over.
  - C40: A crash during a push.
- **Delivery**, deferred by [Choose validation and delivery ownership](https://github.com/talvor/AssemblyAI/issues/18):
  - C41: The daemon's push, and its refusal when origin holds commits AsmAI did not make.
  - C42: A draft PR, and the "[not ready]" fallback when GitHub refuses a draft.
  - C43: CI watched through gh: green; red with one judged re-run; a newer push replacing the wait.
  - C44: The 15-minute wait for a first check, and the hold for a repository with no declared CI.
  - C45: Marking the PR ready when CI is green.
  - C46: A leader-opened PR reconciled as an effect, including a crash between the push and the PR.
- **Remote hosts**, deferred by [Define CLI setup and management experience](https://github.com/talvor/AssemblyAI/issues/9); [Choose factory hosting and lifecycle](https://github.com/talvor/AssemblyAI/issues/7):
  - C47: Remote use over SSH: `--host`, Lavish through port forwarding, and plain `ssh -t host asmai`.

### Glossary and ADR
- [GLOSSARY.md](https://github.com/talvor/AssemblyAI/blob/main/GLOSSARY.md) gains **Qualification**, **Certified platform**, **Qualification record**, **Known limitation**, **Proving scenario** and **Proving ground** (pending archive). The scenarios are called proving scenarios because acceptance already means a leader's verdict on a result.
- [ADR 0008](https://github.com/talvor/AssemblyAI/blob/main/docs/adr/0008-qualification-runs-real-provider-clis-on-real-hosts.md) records that qualification runs real provider CLIs on real hosts, never simulated providers or hosted CI (pending archive).

### Map follow-through
- **New ticket.** "Choose the specification's structure and implementation sequence" (grilling) graduates from the fog item about the final specification's structure and implementation sequencing. It is blocked by [Choose license, release packaging and upgrade migration](https://github.com/talvor/AssemblyAI/issues/20), so it is the last ticket on the map, and it can use the proving scenarios to order the implementation.
- **Fog.** That fog item is removed now that it is a ticket. The workflow-variation item is removed as settled: the proving scenarios name the kinds of job v1 must handle.
- **Notes** gain a pointer: what must pass before v1 launches, the proving ground and qualification are settled here.
- **Decisions so far** gains this ticket's line.
- **No implementation.** This is a planning resolution; it authorizes no implementation.

### Evidence
Three live Lavish rounds on 2026-10-05: 18 questions with recommendations, then confirmation. The answers are recorded verbatim here:
- **Round 1:**
  - Q1 A (two gates: qualification certifies the platform; the scenarios pass with my verdict)
  - Q2 A (AsmAI's v2 notify command on AssemblyAI; otman for a second repository; dev-setup for no CI)
  - Q3 A (real AsmAI work: a research question it needs, a Wayfinder ticket of its next map, the first real defect)
  - Q4 A (S1 to S9 as listed)
  - Q5 A (evidence checklist plus my verdict; passes unless I say 'not usable'; recorded in the repository)
  - Q6 A (all 47 cases; per version combination where the provider matters, per platform otherwise)
  - Q7 A (real providers under a separate OS user; injected faults; replay only for what cannot be caused; a GitHub fixture repository)
  - Q8 A (the safe default passes and is listed as a known limitation; any unsafe behaviour fails)
  - Q9 A (maintainer-run before each release and on any pinned-version change; the release carries the record)
  - Q10 A (one of my own Linux machines (named in my notes)), note: "I do not have that setup yet."
  - Q11 A (Ghostty, locally and over SSH; others best effort)
- **Round 2:**
  - R2-Q1 **B** (S9 waits for a separate physical machine; launch waits too), note: "I will setup a virtual machine either on this host or somewhere else.  Lets not block on this until its actually required."
  - R2-Q2 **B** (as drafted, plus each record states elapsed time, my time answering, and allowance used (recorded, not a pass condition))
  - R2-Q3 A (scenarios gate v1; later releases rerun only the scenarios they change)
  - R2-Q4 A (proving scenario and proving ground)
  - R2-Q5 A (add all four as written)
  - R2-Q6 A (record ADR 0008 as drafted)
  - R2-Q7 A (new ticket for the specification's structure and sequence, last on the map; workflow-variation fog removed)
- **Confirmation:** CONFIRM "Confirm and record", on a page holding the full resolution above.

Facts checked on 2026-10-05, used as evidence and not as qualification:
- otman: Go, CI (`go vet`, `go test`, a cross-platform build) green on 2026-10-05, 52 PRs; its own otman tracker holds only four test items.
- dev-setup: Shell and Nix, one test script, no CI workflow.
- This host: Linux x86_64 (Pop!_OS), Ghostty, no tmux, QEMU with KVM; Claude Code 2.1.283, Codex 0.157.0, Lavish 0.1.79.

The board, the round-by-round questions and answers, the gathered case list, ADR 0008 and the glossary terms were produced in a disposable worktree and are being archived separately.
