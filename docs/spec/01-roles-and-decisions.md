# 01 Roles and decisions

This document specifies who does what in the factory and who decides what: the five roles, leaders and workers, handoffs, assignments and acceptance, mandates and grants, delegated decisions, escalation to the user, versioned decision requests, answer surfaces and witnessed messages. [02 Daemon and store](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/02-daemon-and-store.md) specifies how the daemon records and delivers all of this. [04 Conversation and Lavish](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/04-conversation-and-lavish.md) specifies how decisions are shown and answered.

## Rules

### Roles

1. **Five factory-wide roles** ([AssemblyAI#5](https://github.com/talvor/AssemblyAI/issues/5)):
   - **Coordination** owns the user's conversation, routing of requests, and end-to-end delivery progress. It is the user's single counterpart: it carries every exchange between the user and the other roles and returns the user's answers to them faithfully. It tracks work across roles and reports each delivery step to the user ([AssemblyAI#18](https://github.com/talvor/AssemblyAI/issues/18)).
   - **Planning** owns requirements, decision maps and specifications. It prepares and interprets planning questions, and Coordination carries the exchange with the user. It coordinates the exploration of UI prototypes, which Engineering workers produce for the user's review.
   - **Research** owns gathering evidence. Its findings inform decisions; they never stand in for the user's answers.
   - **Engineering** owns implementation, technical diagnosis, technical prototypes and operational work. It owns the delivery of a job that changes code ([06](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/06-validation-and-delivery.md)).
   - **Quality** owns independent review and validation. Its assessment stays separate from Engineering's implementation, and it never fixes the work it validates ([AssemblyAI#18](https://github.com/talvor/AssemblyAI/issues/18)).
2. **Roles are responsibilities, not stages.** A job uses the roles its outcome needs; the five are not a sequence every job passes through ([AssemblyAI#5](https://github.com/talvor/AssemblyAI/issues/5)).
3. **One leader per role.** Each role has one leader, accountable for the role's decisions and coordination across every job and repository, keeping separate context for each job. Concurrent jobs never create another set of leaders ([AssemblyAI#5](https://github.com/talvor/AssemblyAI/issues/5)).
4. **At most one leader process per role at any instant**, enforced by fencing. Coordination always runs while the factory runs; the other leaders run on demand. While a role has no leader, its requests wait durably and nothing it would authorize proceeds. [02](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/02-daemon-and-store.md) specifies leaders on demand and fencing ([AssemblyAI#7](https://github.com/talvor/AssemblyAI/issues/7), [AssemblyAI#14](https://github.com/talvor/AssemblyAI/issues/14)).
5. **What a leader does itself.** A leader inspects context, reasons, converses, accepts or rejects results and keeps the coordination records. Substantive research, implementation, prototype creation and independent validation always run as worker assignments ([AssemblyAI#5](https://github.com/talvor/AssemblyAI/issues/5)). Workers run the skills, in every role ([AssemblyAI#17](https://github.com/talvor/AssemblyAI/issues/17), [08](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/08-skills-and-agent-instructions.md)).

### Workers and assignments

6. **One owner, one assignment.** A worker has one owning leader and carries one bounded assignment at a time. Other leaders may give it information, but changes to its scope, priority or cancellation go through its owning leader ([AssemblyAI#5](https://github.com/talvor/AssemblyAI/issues/5)).
7. **What an assignment states.** An assignment has an outcome and acceptance criteria. The owning leader may name the skill the worker is to use, narrow the worker's skill list, override the role's default provider and model, and declare the assignment side-effect-free ([AssemblyAI#9](https://github.com/talvor/AssemblyAI/issues/9), [AssemblyAI#17](https://github.com/talvor/AssemblyAI/issues/17), [AssemblyAI#8](https://github.com/talvor/AssemblyAI/issues/8)).
8. **Cross-role work** is asked for leader to leader, by handoff. The receiving leader chooses its own workers ([AssemblyAI#5](https://github.com/talvor/AssemblyAI/issues/5)).
9. **Results.** A result links to its artifacts and evidence and discloses every unresolved gap. A message saying "done" is never a result. The owning leader checks the result against the assignment's acceptance criteria ([AssemblyAI#5](https://github.com/talvor/AssemblyAI/issues/5)). [06](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/06-validation-and-delivery.md) adds what a writing assignment's result must contain.
10. **Acceptance and rejection.** The owning leader accepts or rejects a result. Rejected work returns to the same worker for correction, in a new dispatch. Acceptance ends the assignment, and any later work is a new assignment ([AssemblyAI#5](https://github.com/talvor/AssemblyAI/issues/5), [AssemblyAI#8](https://github.com/talvor/AssemblyAI/issues/8)).
11. **Reusing a session.** A worker's provider session may be reused for a new assignment only if job isolation and the new assignment's ownership are kept ([AssemblyAI#5](https://github.com/talvor/AssemblyAI/issues/5)).

### Handoffs

12. **What a handoff carries:** the job, the requested outcome, the relevant decisions and evidence, the constraints and the permissions already granted, the acceptance criteria, and the accountable receiving leader ([AssemblyAI#5](https://github.com/talvor/AssemblyAI/issues/5)).
13. **Answering a handoff.** The receiving leader explicitly accepts it, asks for clarification, or declines it with a reason. It checks the results of the work it takes on against the handoff's acceptance criteria, and Coordination tracks the job's progress across roles ([AssemblyAI#5](https://github.com/talvor/AssemblyAI/issues/5)).
14. **Disagreements.** Leaders first reconcile a disagreement against the agreed requirements and the evidence in their own areas. Coordination owns any cross-role trade-off they cannot settle and takes every decision that needs the user's judgment to the user. No role, Coordination included, may mark a failed validation as passed ([AssemblyAI#5](https://github.com/talvor/AssemblyAI/issues/5)). A disputed blocking finding follows the same path: the two leaders reconcile, and anything still unresolved goes to the user ([AssemblyAI#18](https://github.com/talvor/AssemblyAI/issues/18)).
15. **Changes of scope** go back to Planning and to the affected owning leaders, and workers receive them only through their owners ([AssemblyAI#5](https://github.com/talvor/AssemblyAI/issues/5)).

### Jobs and mandates

16. **Opening a job.** Only Coordination opens a job, from the user's witnessed message, with its mandate and acceptance criteria. Coordination's reading of the request is stored beside the user's words. A follow-up is a new job linked to the one before it ([AssemblyAI#8](https://github.com/talvor/AssemblyAI/issues/8), [AssemblyAI#9](https://github.com/talvor/AssemblyAI/issues/9), [AssemblyAI#10](https://github.com/talvor/AssemblyAI/issues/10), [AssemblyAI#12](https://github.com/talvor/AssemblyAI/issues/12)).
17. **The default mandate.** A requested outcome authorizes the ordinary work needed to deliver it, within the agreed scope, the repository instructions, the operating limits and the acceptance criteria ([AssemblyAI#6](https://github.com/talvor/AssemblyAI/issues/6)):
    - **A tested-PR job** is authorized to inspect, plan, research, make scoped edits, run checks, commit, push its assignment branches and job branch, and open and update its pull request ([AssemblyAI#6](https://github.com/talvor/AssemblyAI/issues/6), [AssemblyAI#11](https://github.com/talvor/AssemblyAI/issues/11)).
    - **A planning-only or research-only job** is authorized only to produce that outcome. In a repository, that still includes pushing its assignment branches and job branch and opening the pull request that holds its notes ([AssemblyAI#6](https://github.com/talvor/AssemblyAI/issues/6), [AssemblyAI#11](https://github.com/talvor/AssemblyAI/issues/11)).
18. **What a mandate never covers without a grant:** deployment, spending money, and destructive changes outside the job. Each needs the user's separate authorization, unless a standing grant already covers it ([AssemblyAI#6](https://github.com/talvor/AssemblyAI/issues/6)).
19. **Spending.** The spending budget is zero unless granted: any action that would spend money needs the user's grant naming the amount and the scope ([AssemblyAI#14](https://github.com/talvor/AssemblyAI/issues/14)).
20. **Merging.** AsmAI never merges in v1, and no grant can authorize a merge. Accepting a tested pull request means it meets the review-ready criteria; it never means it may be merged ([AssemblyAI#18](https://github.com/talvor/AssemblyAI/issues/18), [AssemblyAI#6](https://github.com/talvor/AssemblyAI/issues/6)).
21. **Limits outside the mandate.** The providers' own tool restrictions and permission prompts apply regardless of the mandate ([AssemblyAI#6](https://github.com/talvor/AssemblyAI/issues/6)). Repository instructions decide how work is done in a repository but never widen a mandate; a conflict between them and the mandate is escalated ([AssemblyAI#11](https://github.com/talvor/AssemblyAI/issues/11)).

### Choosing between approaches

22. **Ask the user whenever more than one distinct viable approach remains** after applying the agreed constraints, the repository's conventions and any applicable grant. This holds even when both approaches are reversible and the leader has a clear recommendation, and the recommendation never makes an alternative non-viable ([AssemblyAI#6](https://github.com/talvor/AssemblyAI/issues/6)).
23. **What counts as distinct.** Approaches are distinct when they differ in behavior, dependencies, interfaces, cost, maintenance or operational consequences. Equivalent ways of expressing the same thing, and routine choices that conventions or grants already settle, are not distinct and need no question. For example, an existing library and a custom helper that both meet the constraints are a choice for the user ([AssemblyAI#6](https://github.com/talvor/AssemblyAI/issues/6)).
24. **Settled routes continue.** Ordinary authorized work along an already-settled route continues without a question ([AssemblyAI#6](https://github.com/talvor/AssemblyAI/issues/6)). Instances of this rule elsewhere: resolving a merge conflict is ordinary writing work unless it poses a choice between approaches ([AssemblyAI#11](https://github.com/talvor/AssemblyAI/issues/11)); setting tests up in a repository that has none is a distinct approach ([AssemblyAI#18](https://github.com/talvor/AssemblyAI/issues/18)); a skill the user's request or the job's mandate does not call for is proposed to the user ([AssemblyAI#17](https://github.com/talvor/AssemblyAI/issues/17), [08](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/08-skills-and-agent-instructions.md)).

### Delegated decisions and acceptance

25. **Recording decisions.** A decision that affects later work is recorded with the accountable leader, the job, the mandate or grant relied on, the choice, its rationale and evidence, its material assumptions, and the conditions that would reopen it. Its source is marked delegated or human; a human decision keeps its actual source. Routine edits need no decision record ([AssemblyAI#6](https://github.com/talvor/AssemblyAI/issues/6)).
26. **Passing decisions on.** The owning leader passes the relevant decision records to its workers in their assignments, and they travel with handoffs and survive restarts. Each job's brief carries its decisions ([AssemblyAI#6](https://github.com/talvor/AssemblyAI/issues/6), [AssemblyAI#8](https://github.com/talvor/AssemblyAI/issues/8)).
27. **Leaders may accept** results against agreed, checkable criteria and report the evidence. The user's input is still needed when acceptance depends on an unresolved preference, a changed requirement or a workflow's explicit human review ([AssemblyAI#6](https://github.com/talvor/AssemblyAI/issues/6)).
28. **Genuine human gates.** Grilling, Wayfinder exchanges and subjective reviews need the user's own response. Agents never supply the human side of them, and a delegated decision can never resolve a ticket or a skill step that requires a live exchange with the user ([AssemblyAI#5](https://github.com/talvor/AssemblyAI/issues/5), [AssemblyAI#6](https://github.com/talvor/AssemblyAI/issues/6), [AssemblyAI#17](https://github.com/talvor/AssemblyAI/issues/17)).
29. **Reconciliation is a delegated decision** of the owning leader. The user is asked only when distinct viable recovery approaches remain or the needed action is outside the mandate ([AssemblyAI#8](https://github.com/talvor/AssemblyAI/issues/8), [02](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/02-daemon-and-store.md)).

### Grants and reuse of approvals

30. **What a grant records:** the exact decision or action approved, its scope (a job, a repository or the whole factory), its conditions, and its source ([AssemblyAI#6](https://github.com/talvor/AssemblyAI/issues/6)). The user gives a grant in words, in the conversation or in answer to a decision request. A leader records it with `asmai decision record` at its scope, citing those words: Coordination records a grant given in the conversation, and the requesting leader one given in an answer. The daemon refuses a grant without a valid citation (rule 46) ([answers](https://github.com/talvor/AssemblyAI/blob/main/.lavish/spec-doc-01-answers.json)).
31. **Scope.** An approval given in a job stays with that job. Reuse across a repository or the whole factory needs an explicit grant at that scope ([AssemblyAI#6](https://github.com/talvor/AssemblyAI/issues/6)).
32. **Reuse.** A grant is carried through assignments, handoffs and resumed sessions and reused while its scope and conditions hold. A changed scope or an invalidated condition needs a new decision; a handoff or a restart alone does not ([AssemblyAI#6](https://github.com/talvor/AssemblyAI/issues/6)).
33. **Skills' human steps** are satisfied by a recorded decision of the user's, or a grant, whose scope covers them; [08](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/08-skills-and-agent-instructions.md) specifies which steps and how ([AssemblyAI#17](https://github.com/talvor/AssemblyAI/issues/17)).
34. **Revocation and changed context.** Current authority is carried into assignments and re-checked before each consequential action it affects. A withdrawal or a material change of context invalidates the permission for every later affected action. The owning leader stops or revises the affected assignments and obtains a fresh decision where one is needed. An action that already happened or is in flight is reported as it actually stands, with the authorized ways to recover; revocation never claims to undo it ([AssemblyAI#6](https://github.com/talvor/AssemblyAI/issues/6)). The user revokes a grant with `asmai grant revoke <id>` ([AssemblyAI#9](https://github.com/talvor/AssemblyAI/issues/9)).

### Escalation and decision requests

35. **Routing.** A worker never asks the user directly. Its decision request goes to its owning leader, which answers it from the records (the job's decisions in its brief, the repository's setup, factory-wide grants) or escalates it through Coordination ([AssemblyAI#9](https://github.com/talvor/AssemblyAI/issues/9), [AssemblyAI#17](https://github.com/talvor/AssemblyAI/issues/17)). A worker's result names the record it relied on ([AssemblyAI#17](https://github.com/talvor/AssemblyAI/issues/17)).
36. **Ownership of a question.** The leader that requests a decision owns its substance. Coordination presents it faithfully and returns the answer ([AssemblyAI#5](https://github.com/talvor/AssemblyAI/issues/5)).
37. **Versions.** Every decision request is versioned. A decision is escalated once; when material new evidence arrives, the requesting leader issues a new version, which replaces the old one ([AssemblyAI#6](https://github.com/talvor/AssemblyAI/issues/6), [AssemblyAI#8](https://github.com/talvor/AssemblyAI/issues/8)).
38. **Answers match versions.** An answer applies only to the version it answers, and a reply to an older version can never approve a changed one ([AssemblyAI#6](https://github.com/talvor/AssemblyAI/issues/6), [AssemblyAI#8](https://github.com/talvor/AssemblyAI/issues/8)).
39. **While an answer is pending,** work that depends on the choice waits. Independent authorized work and evidence gathering continue within the mandate and the operating limits. Silence or elapsed time is never approval ([AssemblyAI#6](https://github.com/talvor/AssemblyAI/issues/6)).
40. **Pause and cancel.** A paused job's pending decisions stay answerable, and their answers apply when it resumes. Cancelling a job withdraws its pending decisions ([AssemblyAI#14](https://github.com/talvor/AssemblyAI/issues/14), [07](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/07-limits-holds-and-visibility.md)).
41. **Kinds of decision the user always makes,** besides choices between distinct approaches: a provider change for an agent after its first dispatch, or for a leader while its role has open work ([AssemblyAI#15](https://github.com/talvor/AssemblyAI/issues/15), [AssemblyAI#14](https://github.com/talvor/AssemblyAI/issues/14), [07](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/07-limits-holds-and-visibility.md)); a needs-you finding, given to the user word for word ([AssemblyAI#18](https://github.com/talvor/AssemblyAI/issues/18)); a disputed blocking finding the leaders cannot settle ([AssemblyAI#18](https://github.com/talvor/AssemblyAI/issues/18)); and anything outside the mandate ([AssemblyAI#6](https://github.com/talvor/AssemblyAI/issues/6)).

### Answer surfaces

42. **One answer surface per version.** Each version of a decision request has exactly one answer surface, the conversation or Lavish, fixed when it is presented and shown with it, so a conversation reply and a Lavish answer can never race ([AssemblyAI#10](https://github.com/talvor/AssemblyAI/issues/10)).
43. **Which surface.** A single-choice escalation, such as a choice between two viable approaches or a provider replacement, is answered in the conversation. Everything else is answered in Lavish: reviews, all grilling and Wayfinder questions, and requests with several questions ([AssemblyAI#10](https://github.com/talvor/AssemblyAI/issues/10)).
44. **Listing is not answering.** `asmai decisions` lists pending decisions; it is not another way to answer them ([AssemblyAI#10](https://github.com/talvor/AssemblyAI/issues/10)).

### Witnessed messages and attribution

45. **What is witnessed.** The daemon journals, word for word, every message the user submits from their own keyboard in any agent's terminal. It tells them apart from its own nudges because it owns the input ([AssemblyAI#10](https://github.com/talvor/AssemblyAI/issues/10)).
46. **Attribution.** Anything attributed to the user (a decision answer, a grant, a mandate or a scope change) must cite a witnessed message, or a Lavish answer the daemon collected, given after the decision version it answers was shown ([AssemblyAI#10](https://github.com/talvor/AssemblyAI/issues/10), [AssemblyAI#12](https://github.com/talvor/AssemblyAI/issues/12)).
47. **Reading and words together.** For an answer given in the conversation, Coordination's reading of the user's words is stored beside them, and the owning leader receives both ([AssemblyAI#10](https://github.com/talvor/AssemblyAI/issues/10)).
48. **Refusals.** A record citing a message typed against an older version, or citing a nudge, is refused, and Coordination presents the current version again ([AssemblyAI#10](https://github.com/talvor/AssemblyAI/issues/10)).
49. **Not a security boundary.** Like the agent command guard, attribution guards against mistakes, not against a hostile process running as the user ([AssemblyAI#10](https://github.com/talvor/AssemblyAI/issues/10)).

## Interfaces

### Commands

[09 CLI and configuration](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/09-cli-and-configuration.md) gives every command's syntax, output and guard. The daemon checks each agent call against the caller's role, whether it is a leader or a worker, and the assignments it owns ([AssemblyAI#9](https://github.com/talvor/AssemblyAI/issues/9)).

| Who | Command | Purpose here |
| --- | --- | --- |
| The user | `asmai decisions` | List pending decisions, with their answer surface |
| The user | `asmai grants`, `asmai grant revoke <id>` | List grants; revoke one |
| Coordination | `asmai job open`, `asmai job link` | Open a job from a witnessed message; link a follow-up to its predecessor |
| Leaders | `asmai handoff send\|accept\|clarify\|decline` | Send a handoff; answer one |
| Leaders | `asmai assign` | Create an assignment, optionally with a provider override and `--side-effect-free` |
| Leaders | `asmai accept`, `asmai reject` | Accept or reject a result |
| Leaders | `asmai cancel` | Cancel an assignment the leader owns |
| Leaders | `asmai reconcile` | Record a reconciliation ([02](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/02-daemon-and-store.md)) |
| Leaders | `asmai decision record` | Record a delegated decision, or a user's answer or grant citing its source |
| Leaders and workers | `asmai decision request` | Request a decision; a worker's goes to its owning leader |
| Workers | `asmai result`, `asmai blocked` | Submit a result; report being blocked |

### Store records

The daemon keeps these records in the store, each with its job and role, and journals every change ([AssemblyAI#8](https://github.com/talvor/AssemblyAI/issues/8), [AssemblyAI#14](https://github.com/talvor/AssemblyAI/issues/14)):

| Record | Holds |
| --- | --- |
| Job | Its number, the witnessed message it opened from, Coordination's reading, the mandate and acceptance criteria, its repository or none, and the job it follows, if any |
| Handoff | The fields in rule 12, the sending and receiving leaders, and its state: sent, accepted, clarification requested, or declined with a reason |
| Assignment | Its owning leader and worker, outcome, acceptance criteria, named skill, narrowed skill list, provider override, side-effect-free flag, the decision records passed to it, and its state ([02](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/02-daemon-and-store.md)) |
| Result | Its assignment and dispatch, links to artifacts and evidence, gaps, the effects it lists and the records it relied on |
| Acceptance or rejection | The result, the deciding leader and its reasons |
| Decision request | Its version, the requesting leader, the questions (each with an id, title, body, options and a recommendation), the answer surface, and its state: pending, answered, replaced by a newer version, or withdrawn |
| Decision record | The fields in rule 25, its source (delegated, or human with the witnessed message or Lavish answer it cites) and, for a conversation answer, Coordination's reading |
| Grant | The fields in rule 30, and whether it is revoked |
| Witnessed message | The user's words verbatim, the terminal and agent they were typed into, and when |

## Settings and defaults

- **Staffing.** Each role has a provider and model for its leader and a default for its workers; an assignment may override them. [09](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/09-cli-and-configuration.md) lists the fields ([AssemblyAI#9](https://github.com/talvor/AssemblyAI/issues/9), [AssemblyAI#15](https://github.com/talvor/AssemblyAI/issues/15)).
- **Skill lists** for each role's leader and workers are in [08](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/08-skills-and-agent-instructions.md).
- **Spending** has no setting: it is zero unless the user grants an amount and scope (rule 19).

## Failure handling

- **No leader for a role.** Requests to the role wait durably, and nothing it would authorize proceeds until one leader is running again ([AssemblyAI#7](https://github.com/talvor/AssemblyAI/issues/7)).
- **A declined handoff** goes back to the sending leader with its reason. A cross-role trade-off that the leaders cannot settle goes to Coordination, and to the user when it needs the user's judgment ([AssemblyAI#5](https://github.com/talvor/AssemblyAI/issues/5)).
- **A stale or misattributed answer** is refused, and Coordination presents the current version again (rule 48). An answer on an old Lavish page is refused ([AssemblyAI#10](https://github.com/talvor/AssemblyAI/issues/10)).
- **An unanswered decision** never times out into approval. Dependent work waits and independent work continues (rule 39).
- **Withdrawn authority** stops the affected assignments; effects already made are reported as they stand (rule 34).
- **A repository instruction that conflicts with the mandate** is escalated, never followed against the mandate (rule 21).
- **Work that keeps failing** is held and escalated by its owning leader ([07](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/07-limits-holds-and-visibility.md), [06](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/06-validation-and-delivery.md)).

## Qualification cases and proving scenarios

- **C11**: capturing witnessed messages and telling them apart from the daemon's nudges ([03](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/03-provider-sessions-and-terminals.md) qualifies the capture; attribution relies on it).
- **C30**: fallback to the other provider only before first dispatch; afterwards the user is asked (rule 41).
- **S1**: the job opens from the user's witnessed message with its mandate and acceptance criteria; writing assignments are accepted against their criteria.
- **S3**: every question reaches the user as a Lavish decision request, each recorded answer cites the user's own Lavish answer or witnessed message, and no agent supplies an answer.
- **S7**: a choice between distinct viable approaches answered in the conversation; a request with several questions answered in Lavish; one answer surface per decision version; every record attributed to the user cites a witnessed message or Lavish answer given after that version was shown; independent work continuing while a decision is pending.

## Sources

- [Define roles and leader-worker contracts](https://github.com/talvor/AssemblyAI/issues/5#issuecomment-5968317664) (AssemblyAI#5)
- [Define delegated authority and human escalation](https://github.com/talvor/AssemblyAI/issues/6#issuecomment-5968467874) (AssemblyAI#6)
- [Choose factory hosting and lifecycle](https://github.com/talvor/AssemblyAI/issues/7#issuecomment-5976506834) (AssemblyAI#7)
- [Define work state and coordination contracts](https://github.com/talvor/AssemblyAI/issues/8#issuecomment-5976668034) (AssemblyAI#8)
- [Define CLI setup and management experience](https://github.com/talvor/AssemblyAI/issues/9#issuecomment-5979143255) (AssemblyAI#9)
- [Explore terminal conversation and Lavish decision flow](https://github.com/talvor/AssemblyAI/issues/10#issuecomment-5989237516) (AssemblyAI#10)
- [Define concurrent repository work and integration](https://github.com/talvor/AssemblyAI/issues/11#issuecomment-5990301132) (AssemblyAI#11)
- [Define v1 acceptance scenarios and evidence](https://github.com/talvor/AssemblyAI/issues/12#issuecomment-5993314453) (AssemblyAI#12)
- [Define operating limits and visibility](https://github.com/talvor/AssemblyAI/issues/14#issuecomment-5991304507) (AssemblyAI#14)
- [Choose runtime adapters and authentication](https://github.com/talvor/AssemblyAI/issues/15#issuecomment-5968867443) (AssemblyAI#15)
- [Choose skill bundles and update policy](https://github.com/talvor/AssemblyAI/issues/17#issuecomment-5992055697) (AssemblyAI#17)
- [Choose validation and delivery ownership](https://github.com/talvor/AssemblyAI/issues/18#issuecomment-5992792804) (AssemblyAI#18)
- [ADR 0002](https://github.com/talvor/AssemblyAI/blob/main/docs/adr/0002-agents-coordinate-through-asmai-cli.md) and the [glossary](https://github.com/talvor/AssemblyAI/blob/main/GLOSSARY.md): Role, Leader, Worker, Assignment, Handoff, Job, Mandate, Grant, Viable approach, Delegated decision, Escalation, Answer surface, Witnessed message.
- The review of this document: [questions](https://github.com/talvor/AssemblyAI/blob/main/.lavish/spec-doc-01-round1-questions.json) and [answers](https://github.com/talvor/AssemblyAI/blob/main/.lavish/spec-doc-01-answers.json).
