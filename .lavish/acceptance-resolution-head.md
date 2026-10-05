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
