# 06 Validation and delivery

This document specifies how a job's work is tested, validated and delivered: Engineering's tests, Quality's validation and findings, what makes a pull request a tested pull request, the daemon's push, the draft pull request and its body, watching CI, the no-CI declaration, the failed-validation limit, and the end of a job. [05 Repositories and job branches](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/05-repositories-and-job-branches.md) specifies how accepted work reaches the job branch and how the branch is kept current.

## Rules

### Who tests and who validates

1. **Engineering tests its own work.** Engineering workers write tests along with the code (the tdd skill) and run the repository's checks before submitting. Each result names the commands run and their outcomes at its commit ([AssemblyAI#18](https://github.com/talvor/AssemblyAI/issues/18), [ADR 0007](https://github.com/talvor/AssemblyAI/blob/main/docs/adr/0007-asmai-delivers-tested-prs-with-its-own-roles.md)).
2. **Quality validates independently.** A Quality worker gets a read-only assignment fixed at one exact commit, in a clean workspace. It re-runs the repository's checks and reviews the change on code-review's two axes: Standards, against the repository instructions, and Spec, against the job's mandate and acceptance criteria. The job's intent is always given to it ([AssemblyAI#18](https://github.com/talvor/AssemblyAI/issues/18), [ADR 0007](https://github.com/talvor/AssemblyAI/blob/main/docs/adr/0007-asmai-delivers-tested-prs-with-its-own-roles.md)).
3. **Quality never fixes.** Validation never changes the work ([AssemblyAI#18](https://github.com/talvor/AssemblyAI/issues/18)).
4. **Never a self-review.** implement's review step is this validation, which the worker asks for through its Engineering leader ([AssemblyAI#18](https://github.com/talvor/AssemblyAI/issues/18), [08](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/08-skills-and-agent-instructions.md)).
5. **When.** Once on the finished job branch: after its last accepted writing assignment and after it has taken in the latest base, before it is offered to the user. Any leader may ask Quality to review a risky assignment earlier ([AssemblyAI#18](https://github.com/talvor/AssemblyAI/issues/18)).
6. **After a later change.** Every later change re-runs the repository's checks at the new head. A fix, or a merge whose conflicts a worker resolved, is also reviewed on both axes for what changed since the last validated commit, and Quality confirms that each earlier blocking finding is resolved. A clean merge of a moved base needs only the checks ([AssemblyAI#18](https://github.com/talvor/AssemblyAI/issues/18)).
7. **No tests at all.** A repository with no tests is stated as a gap. Setting tests up is a distinct approach, so it goes to the user ([AssemblyAI#18](https://github.com/talvor/AssemblyAI/issues/18), [01](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/01-roles-and-decisions.md)).

### Findings

8. **Three kinds.** Quality marks each finding as one of ([AssemblyAI#18](https://github.com/talvor/AssemblyAI/issues/18)):
   - **blocking**: it must be fixed, and the Engineering leader assigns the fix;
   - **advisory**: it is listed in the PR body, and no fix is required;
   - **needs-you**: it challenges the user's stated intent or a recorded decision, so it goes to the user word for word.
9. **Clearing a blocking finding.** Only Quality's re-validation or the user's decision clears it. If the Engineering leader disputes one, the two leaders reconcile, and anything still unresolved goes to the user ([AssemblyAI#18](https://github.com/talvor/AssemblyAI/issues/18)).
10. **The failed-validation limit.** After 3 failed validations of the same job, the job's delivery holds. A failed validation means blocking findings, or red CI after its one judged re-run (rule 28). The Engineering leader escalates to the user with the findings and what was tried, and other jobs continue ([AssemblyAI#18](https://github.com/talvor/AssemblyAI/issues/18)). Each fix is a new assignment, so the dispatch limit per assignment ([07](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/07-limits-holds-and-visibility.md)) would never catch this.

### A tested pull request

11. **The five conditions.** A pull request is a tested pull request when all of these hold ([AssemblyAI#18](https://github.com/talvor/AssemblyAI/issues/18)):
    1. Every writing assignment is accepted, and each result names the tests added and the checks run, with their outcomes.
    2. The job branch has taken in the latest base with no conflicts.
    3. Quality has validated that exact head commit: the repository's checks re-ran and passed, and no blocking finding is unresolved.
    4. The job branch is pushed, and CI on that head is green. A repository declared as having no CI says so, and the checks Quality ran stand in.
    5. The PR body states the evidence and every gap, skipped check or exception.
12. **Evidence goes stale.** Any later commit makes the evidence stale, so conditions 2 to 4 are met again for the new head ([AssemblyAI#18](https://github.com/talvor/AssemblyAI/issues/18)).
13. **Where the evidence lives.** The journal holds the results, Quality's report and the acceptances, and the PR body summarizes them. No GitHub review is posted, because agents act in the user's name ([AssemblyAI#18](https://github.com/talvor/AssemblyAI/issues/18)).
14. **A fixed order.** Delivery always runs in the order of rule 11: accepted work, the base taken in, validation, push and CI, then the ready mark ([ADR 0007](https://github.com/talvor/AssemblyAI/blob/main/docs/adr/0007-asmai-delivers-tested-prs-with-its-own-roles.md)).

### The delivery owner

15. **Engineering owns code delivery.** The Engineering leader owns the delivery of a job that changes code. It decides when the job branch is ready and hands validation to Quality, receives Quality's findings directly, owns the pull request, and follows CI through to a tested pull request. Coordination reports each step to the user ([AssemblyAI#18](https://github.com/talvor/AssemblyAI/issues/18)).
16. **Notes are delivered by their own leader.** A notes-only job is delivered by the leader whose notes they are, Planning or Research ([AssemblyAI#18](https://github.com/talvor/AssemblyAI/issues/18)). A repository-setup job is delivered the same way by Coordination's leader ([08](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/08-skills-and-agent-instructions.md), [answers](https://github.com/talvor/AssemblyAI/blob/main/.lavish/spec-doc-08-answers.json)).

### The push

17. **The daemon pushes.** The daemon pushes the job branch when the delivery owner asks, with a plain push that is never forced. It records the push as an effect, and it is the only party that ever moves the job branch, locally or on origin ([AssemblyAI#18](https://github.com/talvor/AssemblyAI/issues/18), [ADR 0007](https://github.com/talvor/AssemblyAI/blob/main/docs/adr/0007-asmai-delivers-tested-prs-with-its-own-roles.md)). The delivery owner asks with `asmai push <job>`, which only the delivery owner may run; it pushes the job branch, or refuses and records an outside change ([answers](https://github.com/talvor/AssemblyAI/blob/main/.lavish/spec-doc-06-answers.json)).
18. **Outside commits refuse the push.** If origin has commits AsmAI did not make, the push is refused and recorded as an outside change. A worker merges them in, and the push is retried ([AssemblyAI#18](https://github.com/talvor/AssemblyAI/issues/18), [05](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/05-repositories-and-job-branches.md)).
19. **When.** The job branch is pushed once, at delivery: when Quality passes the head, the job branch is pushed and a draft pull request is opened. A later change repeats the cycle on the same pull request ([AssemblyAI#18](https://github.com/talvor/AssemblyAI/issues/18)).
20. **Repository instructions never decide the push.** AsmAI's own delivery always pushes the job branch and opens the pull request. Repository instructions shape what goes into the pull request (templates, labels, checks to run) and Quality's Standards review, never how the branch is pushed. An instruction that would hand the branch to another tool, such as "push through no-mistakes", is listed as a gap in the PR body ([AssemblyAI#18](https://github.com/talvor/AssemblyAI/issues/18)).

### The pull request

21. **The leader opens it.** The delivery owner opens and updates the pull request itself with gh, and records each as an effect ([AssemblyAI#18](https://github.com/talvor/AssemblyAI/issues/18), [ADR 0007](https://github.com/talvor/AssemblyAI/blob/main/docs/adr/0007-asmai-delivers-tested-prs-with-its-own-roles.md)). The daemon learns which pull request to follow from that effect ([02](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/02-daemon-and-store.md)).
22. **Draft first.** The pull request opens as a draft. If GitHub refuses a draft, it opens normally with "[not ready]" at the start of its title until it is ready ([AssemblyAI#18](https://github.com/talvor/AssemblyAI/issues/18)).
23. **Workers write their part.** Every writing assignment's result includes a PR section for its own part, in the pr skill's form: what changed, plus before-and-after evidence. Changes made while merging the base in or resolving conflicts get their own section from the worker that made them ([AssemblyAI#18](https://github.com/talvor/AssemblyAI/issues/18), [08](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/08-skills-and-agent-instructions.md)).
24. **The leader composes the whole.** The Engineering leader composes the pull request from those sections, Quality's report and CI, and judges the merge danger of the whole change ([AssemblyAI#18](https://github.com/talvor/AssemblyAI/issues/18)).
25. **The body.** It follows the repository's PR template where there is one, and otherwise the pr skill's template. Either way it adds an AsmAI section covering the job and its mandate, the head commit Quality passed, the checks and CI results, the advisory findings, and the gaps ([AssemblyAI#18](https://github.com/talvor/AssemblyAI/issues/18)), including a rebase convention that could not be followed after the first push ([05](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/05-repositories-and-job-branches.md)). It links the originating issue with "Closes #n" only when the mandate is to resolve that issue, and with "Refs #n" otherwise. The body is updated whenever the evidence changes ([AssemblyAI#18](https://github.com/talvor/AssemblyAI/issues/18)).

### CI

26. **The daemon watches CI.** The daemon watches the checks on the pushed head through gh, using no worker and no allowance. A newer push replaces the old wait ([AssemblyAI#18](https://github.com/talvor/AssemblyAI/issues/18)).
27. **Green.** When the checks are green, the daemon marks the pull request ready for review (for a "[not ready]" pull request, by removing that prefix) and records the delivery, and Coordination reports it ([AssemblyAI#18](https://github.com/talvor/AssemblyAI/issues/18)).
28. **Red.** When they are red, the Engineering leader receives the failing checks. It may re-run the failed jobs once if it judges the failure unrelated to the change, recorded as a delegated decision. Otherwise it assigns a fix, which goes through Quality again ([AssemblyAI#18](https://github.com/talvor/AssemblyAI/issues/18)).
29. **An empty list is not green.** A head with no checks is never green unless the repository is declared as having no CI ([ADR 0007](https://github.com/talvor/AssemblyAI/blob/main/docs/adr/0007-asmai-delivers-tested-prs-with-its-own-roles.md)).

### No CI

30. **The declaration.** A repository's configuration can declare that it has no CI. Then Quality's checks stand in for CI, the PR body says so, and there is no wait and no hold ([AssemblyAI#18](https://github.com/talvor/AssemblyAI/issues/18), [AssemblyAI#12](https://github.com/talvor/AssemblyAI/issues/12)).
31. **Asked at setup.** Coordination's repository setup asks whether a newly added repository has CI, and the user can change the answer later ([AssemblyAI#18](https://github.com/talvor/AssemblyAI/issues/18)). The declaration exists only in the configuration, and only the user changes it: when the user answers, Coordination gives the configuration change to make, as it does for `asmai repo add`, and a job held for the answer resumes once the user applies it ([AssemblyAI#9](https://github.com/talvor/AssemblyAI/issues/9), [answers](https://github.com/talvor/AssemblyAI/blob/main/.lavish/spec-doc-06-answers.json)).
32. **The wait for a first check.** Without a declaration, AsmAI waits for at least one check on the head. If none appears within the first-check wait, the job holds and the user is asked whether the repository has CI ([AssemblyAI#18](https://github.com/talvor/AssemblyAI/issues/18)).

### Merging and the end of a job

33. **AsmAI never merges in v1.** The user merges on GitHub, and no grant can authorize a merge ([AssemblyAI#18](https://github.com/talvor/AssemblyAI/issues/18), [01](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/01-roles-and-decisions.md)). "Ready" never means merged ([ADR 0007](https://github.com/talvor/AssemblyAI/blob/main/docs/adr/0007-asmai-delivers-tested-prs-with-its-own-roles.md)).
34. **A code job ends at delivery.** A job that changes code ends when its tested pull request is delivered, and Coordination reports it with the link ([AssemblyAI#18](https://github.com/talvor/AssemblyAI/issues/18)).
35. **Afterwards is a follow-up.** Anything later is a follow-up job the user asks for, continuing on the same job branch and pull request: review comments, a conflict after another merge, or a CI failure on a moved base. AsmAI does not watch the pull request after the job ends ([AssemblyAI#18](https://github.com/talvor/AssemblyAI/issues/18), [05](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/05-repositories-and-job-branches.md)).
36. **The user's own tools.** The user may still run no-mistakes or anything else on a delivered pull request; a follow-up job takes in the commits it adds as outside changes ([AssemblyAI#18](https://github.com/talvor/AssemblyAI/issues/18)).

### Notes-only jobs and jobs without a repository

37. **No validation unless asked.** Neither gets Quality validation unless the mandate asks for an independent check. The owning leader accepts against the mandate, and its acceptance is the completion evidence. Results link their artifacts ([AssemblyAI#18](https://github.com/talvor/AssemblyAI/issues/18)).
38. **A notes pull request** has a short "notes only" body ([AssemblyAI#18](https://github.com/talvor/AssemblyAI/issues/18)). It is delivered through the same cycle as code: pushed, opened as a draft, and marked ready when CI is green on its head, or straight away in a repository declared as having no CI. The job then ends ([AssemblyAI#11](https://github.com/talvor/AssemblyAI/issues/11), [answers](https://github.com/talvor/AssemblyAI/blob/main/.lavish/spec-doc-06-answers.json)).
39. **A job without a repository** ends when its owning leader accepts the outcome against the mandate, and Coordination reports it with where the results are ([AssemblyAI#18](https://github.com/talvor/AssemblyAI/issues/18), [05](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/05-repositories-and-job-branches.md)).

### Recovering delivery

40. **A crash during a push** is recovered through reconciliation: the job branch is fetched from origin and compared with the recorded push before anything is pushed again ([AssemblyAI#8](https://github.com/talvor/AssemblyAI/issues/8), [AssemblyAI#11](https://github.com/talvor/AssemblyAI/issues/11), [02](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/02-daemon-and-store.md)).
41. **A crash between the push and the pull request** is reconciled by the delivery owner, which checks GitHub for a pull request from the job branch before opening one, so a pull request is never opened twice ([AssemblyAI#8](https://github.com/talvor/AssemblyAI/issues/8), [AssemblyAI#18](https://github.com/talvor/AssemblyAI/issues/18)).

## Interfaces

### Commands

| Who | Command | Purpose |
| --- | --- | --- |
| The delivery owner | `asmai push <job>` | Ask the daemon to push the job branch (rule 17) |
| The delivery owner | `gh pr create`, `gh pr edit`, then `asmai effect` | Open and update the pull request, and record each (rule 21) |
| The delivery owner | `asmai handoff send` | Hand validation to Quality ([01](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/01-roles-and-decisions.md)) |
| Quality workers | `asmai result` | Submit the validation report with its findings |
| Writing workers | `asmai result` | Submit a result with its tests, checks and PR section |

### Store records

| Record | Holds |
| --- | --- |
| Validation report | The exact head commit, the checks re-run and their outcomes, and each finding with its kind and text |
| Finding | Its kind (blocking, advisory or needs-you), text, the commit it was found at, and how it was cleared |
| Failed validation | The job, its count, and the findings or failing checks behind it |
| Push | The job branch, the commit pushed, and the result (pushed, or refused for outside commits) |
| Pull request | Its number, draft or "[not ready]" state, and each body update |
| CI watch | The head commit, the checks seen and their states, any judged re-run, and when the first-check wait started |
| Delivery | The pull request, the head commit, and when it was marked ready |

## Settings and defaults

[09](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/09-cli-and-configuration.md) names the fields.

| Setting | Scope | Default | Rule |
| --- | --- | --- | --- |
| Failed-validation limit | Factory | 3 failed validations per job | 10 |
| First-check wait | Factory | 15 minutes | 32 |
| No-CI declaration | Per repository | Not declared | 30 |

## Failure handling

| Failure | Handling |
| --- | --- |
| Blocking findings | The Engineering leader assigns the fix; Quality re-validates (rules 8, 9) |
| A disputed blocking finding | The leaders reconcile, then the user (rule 9) |
| 3 failed validations | The job's delivery holds and the user is told (rule 10) |
| Outside commits at push | Refused; a worker merges; the push is retried (rule 18) |
| GitHub refuses a draft | Opened with "[not ready]" (rule 22) |
| Red CI | One judged re-run, or a fix through Quality (rule 28) |
| No check within the first-check wait | The job holds and the user is asked (rule 32) |
| A crash during a push | Reconciled against origin (rule 40) |
| A crash between the push and the pull request | Reconciled against GitHub; never a second pull request (rule 41) |

## Qualification cases and proving scenarios

- **C40**: a crash during a push (rule 40).
- **C41**: the daemon's push, and its refusal when origin holds commits AsmAI did not make (rules 17, 18).
- **C42**: a draft pull request, and the "[not ready]" fallback when GitHub refuses a draft (rule 22).
- **C43**: CI watched through gh: green; red with one judged re-run; a newer push replacing the wait (rules 26 to 28).
- **C44**: the 15-minute wait for a first check, and the hold for a repository with no declared CI (rule 32).
- **C45**: marking the pull request ready when CI is green (rule 27).
- **C46**: a leader-opened pull request reconciled as an effect, including a crash between the push and the pull request (rules 21, 41).
- **S1**: Quality's report names the exact head with no blocking finding left; the push, the draft, green CI and the ready mark are in the journal; the body carries the AsmAI section; the link is reported and the job ends.
- **S4**: the fix meets S1's tested-PR evidence.
- **S6**: the no-CI declaration recorded, the PR body saying Quality's checks stand in, and no wait and no hold.
- **S2**: research notes delivered as a pull request with a "notes only" body.

## Sources

- [Define delegated authority and human escalation](https://github.com/talvor/AssemblyAI/issues/6#issuecomment-5968467874) (AssemblyAI#6)
- [Define work state and coordination contracts](https://github.com/talvor/AssemblyAI/issues/8#issuecomment-5976668034) (AssemblyAI#8)
- [Define concurrent repository work and integration](https://github.com/talvor/AssemblyAI/issues/11#issuecomment-5990301132) (AssemblyAI#11)
- [Define v1 acceptance scenarios and evidence](https://github.com/talvor/AssemblyAI/issues/12#issuecomment-5993314453) (AssemblyAI#12)
- [Choose validation and delivery ownership](https://github.com/talvor/AssemblyAI/issues/18#issuecomment-5992792804) (AssemblyAI#18)
- [ADR 0007](https://github.com/talvor/AssemblyAI/blob/main/docs/adr/0007-asmai-delivers-tested-prs-with-its-own-roles.md) and the [glossary](https://github.com/talvor/AssemblyAI/blob/main/GLOSSARY.md): Validation, Finding, Tested pull request, Job branch.
- The review of this document: [questions](https://github.com/talvor/AssemblyAI/blob/main/.lavish/spec-doc-06-round1-questions.json) and [answers](https://github.com/talvor/AssemblyAI/blob/main/.lavish/spec-doc-06-answers.json).
