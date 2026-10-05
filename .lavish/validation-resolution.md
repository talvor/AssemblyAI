## Resolution — confirmed by Phillip in Lavish

### Scope
This ticket settles, as narrowed by [Define concurrent repository work and integration](https://github.com/talvor/AssemblyAI/issues/11):
- who validates, reviews and tests;
- what makes a PR a tested PR, and where the evidence is recorded;
- when and by whom the job branch is pushed and its PR opened;
- no-mistakes;
- the line between a tested PR and a merge.

### Who tests and who validates
- **Engineering tests its own work.** Engineering workers write tests along with the code (tdd) and run the repository's checks before submitting. Each result names the commands and their outcomes at its commit.
- **Quality validates independently.** A Quality worker gets a read-only assignment fixed at one exact commit, in a clean workspace. It re-runs the repository's checks and reviews on code-review's two axes:
  - Standards, against the repository instructions;
  - Spec, against the job's mandate and acceptance criteria.

  Quality never fixes anything.
- **implement's review step.** The operating guide maps implement's "use /code-review" onto this validation, which the worker asks for through its Engineering leader. It is never a self-review.
- **When.** Once on the finished job branch, after its last accepted writing assignment and after it has taken in the latest base, before it is offered to Phillip. Any leader may ask Quality to review a risky assignment earlier.
- **After a later change.** Every later change re-runs the repository's checks at the new head. A fix, or a merge whose conflicts a worker resolved, is also reviewed on both axes for what changed since the last validated commit, and Quality confirms that each earlier blocking finding is resolved. A clean merge of a moved base needs only the checks.

### Findings
- **Three kinds.** Quality marks each finding as one of:
  - **blocking:** it must be fixed, and the Engineering leader assigns the fix;
  - **advisory:** it is listed in the PR body, and no fix is required;
  - **needs-you:** it challenges Phillip's stated intent or a recorded decision, so it goes to him word for word.
- **Clearing a blocking finding.** Only Quality's re-validation or Phillip's decision clears it. If the Engineering leader disputes one, the two leaders reconcile, and anything still unresolved goes to Phillip.
- **Work that keeps failing.** After 3 failed validations of the same job, the job's delivery holds. A failed validation means blocking findings, or red CI after its one judged re-run. The Engineering leader escalates to Phillip with the findings and what was tried, and other jobs continue. The number is a factory-wide setting. Each fix is a new assignment, so the 5-dispatch limit per assignment from [Define operating limits and visibility](https://github.com/talvor/AssemblyAI/issues/14) would never catch this.

### A tested pull request
A PR is a tested PR when all of the following hold:
1. Every writing assignment is accepted, and each result names the tests added and the checks run, with their outcomes.
2. The job branch has taken in the latest base with no conflicts.
3. Quality has validated that exact head commit: the repository's checks re-ran and passed, and no blocking finding is unresolved.
4. The job branch is pushed, and CI on that head is green. A repository declared as having no CI says so, and the checks Quality ran stand in.
5. The PR body states the evidence and every gap, skipped check or exception.

Any later commit makes the evidence stale, so steps 2 to 4 are repeated. A repository with no tests at all is stated as a gap. Setting tests up is a distinct approach, so it goes to Phillip.

**Where the evidence lives.** The journal holds the results, Quality's report and the acceptances. The PR body summarizes them. No GitHub review is posted, because agents act in Phillip's name.

### Delivery
- **Owner.** The Engineering leader owns the delivery of a job that changes code:
  - it decides when the job branch is ready and hands validation to Quality;
  - it receives Quality's findings directly;
  - it owns the PR and follows CI through to a tested PR.

  Coordination reports each step to Phillip. A notes-only job is delivered by the leader whose notes they are (Planning or Research).
- **Push.** The daemon pushes the job branch when the delivery owner asks, with a plain push that is never forced. If origin has commits AsmAI did not make, the push is refused and recorded as an outside change. A worker merges them in, and the push is retried. The daemon records the push as an effect, and it is the only party that ever moves the job branch, locally or on origin.
- **When.** Once, at delivery. When Quality passes the head, the job branch is pushed and a draft PR is opened. When CI is green on that head, the PR is marked ready for review and Coordination reports it. If GitHub refuses a draft, the PR opens normally with "[not ready]" at the start of its title until then. A later change repeats the cycle on the same PR.
- **Writing the PR.**
  - Every writing assignment's result includes a PR section for its own part, in the pr skill's form: what changed, plus before-and-after evidence. Changes made while merging the base in or resolving conflicts get their own section from the worker that made them.
  - The Engineering leader composes the PR from those sections, Quality's report and CI, and judges the merge danger of the whole change. It opens and updates the PR itself with gh and records each as an effect.
  - The body follows the repository's PR template where there is one, and otherwise the pr skill's template. Either way it adds an AsmAI section covering the job and its mandate, the head commit Quality passed, the checks and CI results, advisory findings and gaps.
  - It links the originating issue with "Closes #n" only when the mandate is to resolve that issue, and with "Refs #n" otherwise. The body is updated whenever the evidence changes.
  - A notes-only job gets a short "notes only" body.
- **CI.** The daemon watches the checks on the pushed head through gh, using no worker or allowance.
  - When they are green, it marks the PR ready and records the delivery.
  - When they are red, the Engineering leader receives the failing checks. It may re-run the failed jobs once if it judges the failure unrelated to the change, recorded as a delegated decision. Otherwise it assigns a fix, which goes through Quality again.
  - A newer push replaces the old wait.
- **No CI.** A repository's configuration can declare that it has no CI. Coordination's repository setup asks when a repository is added, and Phillip can change the answer later. Otherwise AsmAI waits for at least one check on the head. If none appears within 15 minutes (a factory-wide setting), the job holds and Phillip is asked whether the repository has CI.
- **Repository instructions.** AsmAI's own delivery always pushes the job branch and opens the PR. Repository instructions shape what goes into the PR (templates, labels, checks to run) and Quality's Standards review, but never how the branch is pushed. An instruction that would hand the branch to another tool, such as "push through no-mistakes", is listed as a gap in the PR body.

### Merge and the end of a job
- **AsmAI never merges in v1.** Phillip merges on GitHub, and no grant can authorize a merge in v1. This narrows [Define delegated authority and human escalation](https://github.com/talvor/AssemblyAI/issues/6), which allowed a merge under explicit authorization.
- **The job ends when its tested PR is delivered.** Coordination reports it with the link. Anything later is a follow-up job that Phillip asks for, continuing on the same job branch and PR: review comments, a conflict after another merge, or a CI failure on a moved base. AsmAI does not watch the PR after the job ends.

### Notes-only jobs and jobs without a repository
Neither gets Quality validation unless the mandate asks for an independent check. The owning leader accepts against the mandate, and its acceptance is the completion evidence. A notes PR says "notes only" in its body, and results link their artifacts.

### no-mistakes
- **Not adopted in v1.** It is not shipped and is on no skill list. Its ideas carry over:
  - a fixed order of checks;
  - the job's intent handed to the reviewer;
  - findings that challenge Phillip's intent go to him;
  - "ready" never means merged;
  - a push never discards commits it did not make;
  - an empty list of CI checks is not green without a no-CI declaration.
- **An optional v2 feature**, as Phillip noted. The map's Out of scope section records it.
- **What v2 starts from.** v2 must resolve the conflicts found here:
  - its agents run outside the daemon-owned terminals, caps, recordings and skill lists, on the user's personal provider copies;
  - its init writes `~/.claude`;
  - its rebase and its pushes after checks pass move the job branch outside the daemon.

  The custody considered here: one Quality worker as the single outer executor; the job branch belonging to the run while it is active; its agents pointed at AsmAI's pinned providers; its ask-user findings becoming decision requests; switched on per repository.
- **Phillip's own use.** He can still run no-mistakes himself on a delivered PR. A follow-up job takes in any commits it adds as outside changes.

### Skill lists and the operating guide
- **pr** stays on Engineering's worker list and is added to the Engineering leader's list, for composing the PR. Planning and Research leaders write the short notes body without it.
- **code-review** stays on Quality's worker list only.
- The operating guide gains three mappings:
  - implement's "use /code-review" means asking the Engineering leader for Quality validation;
  - in a worker, the pr skill writes its PR section into the result instead of opening a PR;
  - "commit your work to the current branch" means the assignment branch.

### Glossary and ADR
- [GLOSSARY.md](https://github.com/talvor/AssemblyAI/blob/main/GLOSSARY.md) gains **Validation**, **Finding** and **Tested pull request** (pending archive).
- [ADR 0007](https://github.com/talvor/AssemblyAI/blob/main/docs/adr/0007-asmai-delivers-tested-prs-with-its-own-roles.md) records that AsmAI delivers tested pull requests with its own roles and that no-mistakes is not adopted in v1 (pending archive).

### Deferred to existing tickets
[Define v1 acceptance scenarios and evidence](https://github.com/talvor/AssemblyAI/issues/12): what "tested" and "ready for review" mean is settled here. That ticket keeps the proving-ground task and the scenarios that show it, and it qualifies:
- the daemon's push, and its refusal when origin holds outside commits;
- draft PRs and the "[not ready]" fallback;
- CI watching through gh, including the 15-minute wait and its hold for a repository with no declared CI;
- marking the PR ready when CI is green;
- a leader-opened PR and the reconciliation of its effect, including a crash between the push and the PR.

### Map follow-through
- **No new ticket.**
- **Define v1 acceptance scenarios and evidence** gets a "Narrowed by" section saying that the definition of a tested PR is settled here.
- **Notes** gain a pointer: who validates and delivers a tested PR is settled here.
- **Out of scope** gains a line: no-mistakes as an optional delivery pipeline is a v2 candidate.
- **Configuration and prompts fog.** The configuration schema now also covers the per-repository no-CI declaration, the CI wait and the failed-validation limit. The agent prompts it covers include the PR section in results and the operating-guide mappings for implement and pr.
- **Workflow-variation fog.** Narrowed: how much validation each kind of job gets is settled here.
- **No implementation.** This is a planning resolution; it authorizes no implementation.

### Evidence
Three live Lavish rounds on 2026-10-05: 20 questions with recommendations, plus two questions of Phillip's own, which were answered on the board, after which round 2 continued. Then confirmation. The answers are recorded verbatim here:
- **Round 1:**
  - Q1 A (not adopted in v1; AsmAI's own roles validate and deliver, using its ideas), note: "Add this as an optional v2 feature"
  - Q2 A (Engineering tests its own work; Quality re-runs checks and reviews independently, never fixes)
  - Q3 A (once on the finished job branch, again after any later change; earlier on request)
  - Q4 A (accepted assignments, base taken in, Quality pass at that head, CI green on that head, gaps stated)
  - Q5 A (journal, summarized in the PR body; no GitHub review in my name)
  - Q6 A (AsmAI never merges in v1; I merge on GitHub)
  - Q7 A (the job ends when the tested PR is delivered; later changes are follow-up jobs)
  - Q8 A (blocking, advisory or needs-you; disputes go leader to leader, then to me)
  - Q9 A (no Quality validation unless the mandate asks; the owning leader's acceptance is the evidence)
- **Round 2:**
  - First a question: "For R2-Q1 I am leading towards B: Coordinator, but I want to understand if there are any downsides to this." Answered on the board, which added a split option C.
  - R2-Q1 A (Engineering owns delivery; notes-only jobs: the notes' own leader)
  - R2-Q2 A (the daemon, when the delivery owner asks; never forced)
  - R2-Q3 A (once, at delivery: pushed, draft PR, ready when CI is green)
  - Then a question: "For R2-Q4, I am thinking that the leader should raise the PR with the information it receives from workers.  A job may require multiple workers to be involved.  Will this raise any issues?" Answered on the board, which added option C.
  - R2-Q4 **C** (workers write their part; the leader composes and opens it)
  - R2-Q5 A (the daemon watches; red goes to the Engineering leader, with one judged re-run allowed)
  - R2-Q6 A (declared per repository; otherwise wait, then hold and ask me)
  - R2-Q7 A (AsmAI's delivery always pushes; such an instruction is listed as a gap)
  - R2-Q8 A (add all three glossary terms as written)
- **Round 3:**
  - R3-Q1 A (proportionate: checks always; review only fixes and resolved conflicts)
  - R3-Q2 A (hold and escalate after 3 failed validations of a job)
  - R3-Q3 A (record ADR 0007 as drafted)

Facts checked on 2026-10-05, used as evidence and not as qualification:
- no-mistakes v1.84.0 is installed and is the latest stable release. It is MIT-licensed, and 176 releases have shipped since v1.0.0 in April 2026.
- Its init adds a `no-mistakes` remote, creates a gate under `~/.no-mistakes`, installs its skill into `~/.claude/skills` and `~/.agents/skills`, and runs a per-user daemon.
- Its fixed pipeline (intent, rebase, review, test, document, lint, push, PR, CI) runs in its own checkouts, with claude or codex subprocesses taken from `PATH`. After checks pass, it keeps watching the PR and re-pushing.

The board, the round-by-round questions and answers, ADR 0007 and the glossary terms were produced in a disposable worktree and are being archived separately.
