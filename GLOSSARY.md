# AsmAI

A personal software engineering factory that can serve multiple repositories.

## Language

**AsmAI**:
The product name of the personal software factory, meaning AssemblyAI.

**Factory**:
The coordinated group of agents that carries out software engineering work for the user across repositories.
_Avoid_: Repository (a factory is not tied to one repository)

**Host**:
The machine on which a factory and all of its agents run. Each user runs at most one factory per host; factories on different hosts are independent.
_Avoid_: Server, machine (when meaning the factory's execution host)

**Job**:
One outcome the user requested through Coordination, with its mandate and acceptance criteria, against at most one repository or none. A job owns its handoffs, assignments, decisions, and grants; later follow-up work is a new job linked to it.
_Avoid_: Task, request, work item

**Role**:
A defined area of factory responsibility, such as orchestration, planning, implementation, research, or testing, with one leader and workers as needed.
_Avoid_: Responsibility (use role as the canonical name)

**Leader**:
The agent accountable for decisions and coordination within a role across the whole factory. Each role has exactly one leader serving all jobs and repositories; leaders communicate with other leaders and delegate execution to workers.
_Avoid_: Worker (leaders and workers have different responsibilities)

**Worker**:
An agent spawned to carry out one bounded assignment at a time under one owning leader. Changes to its assignment are controlled by that leader.

**Assignment**:
A bounded piece of work entrusted to one worker by its owning leader, with an outcome and acceptance criteria.

**Dispatch**:
One identified delivery of work to a specific agent session. Only evidence tied to the current dispatch counts; a retry, correction, or resumption is always a new dispatch.
_Avoid_: Attempt, run

**Reconciliation**:
The owning leader's determination of what actually happened when a dispatch's outcome is unknown, recorded with what is known, what is not, and the chosen way forward.
_Avoid_: Retry (reconciliation decides whether anything is retried)

**Handoff**:
A request for another leader to take responsibility for a defined outcome, carrying the context and acceptance criteria needed to accept, clarify, or decline it.

**Mandate**:
The authority to pursue a requested outcome within its agreed scope, constraints, and acceptance criteria.

**Grant**:
An explicit authorization for a decision or action within a recorded scope and set of conditions, reusable while those conditions hold.

**Viable approach**:
A way of achieving an outcome that satisfies the agreed constraints and differs from alternatives in behavior, dependencies, interfaces, cost, maintenance, or operational consequences. Equivalent expression styles are not distinct approaches.

**Delegated decision**:
A choice made by an accountable leader within its mandate or an applicable grant, recorded as agent-made rather than attributed to the user.

**Escalation**:
A decision request carried to the user through Coordination when work requires the user's choice or authority.

**Registered repository**:
A repository the user has explicitly added to a factory. Jobs can target only registered repositories.

**Repository instructions**:
The instructions a registered repository gives agents, plus the user's own notes for it in the factory's configuration. They govern how work is done in that repository but never widen a mandate.
_Avoid_: Repository rules, project settings

**Job branch**:
The one branch that carries a repository job's accepted work and becomes its pull request.
_Avoid_: Integration branch, feature branch

**Assignment branch**:
The branch a writing assignment works on in its workspace, made from its job branch and kept on origin.
_Avoid_: Worker branch

**Workspace**:
The directory set aside for one assignment, where its worker works: the factory's own checkout of the job's repository, or an empty scratch directory for a job without one. A writing assignment's workspace has its own branch; a read-only one is fixed at the commit it examines. Writes outside it are effects.
_Avoid_: Worktree, sandbox, checkout (when meaning an assignment's working copy)

**Conversation**:
The user's ongoing exchange with Coordination in its interactive terminal. Unlike an intervention, leaving it never pauses automated delivery.
_Avoid_: Chat, session

**Focused job**:
The job the conversation is currently about. The user's messages apply to it unless they name another job.
_Avoid_: Current job, active job

**Witnessed message**:
A message the factory observed the user submit from their own keyboard in an agent's terminal. It is the only conversation evidence that a decision, grant or mandate came from the user.
_Avoid_: Turn, prompt (when meaning the user's attributable words)

**Answer surface**:
The one place where a given version of a decision request can be answered: the conversation or Lavish.

**Catch-up**:
The factory's account of what changed since the user last left the conversation, shown when they return.
_Avoid_: Digest, recap, summary

**Coordination**:
The role responsible for the user's conversation with the factory and overall delivery progress.

**Planning**:
The role responsible for requirements, decision maps, and specifications.

**Research**:
The role responsible for gathering evidence that informs the factory's work.

**Engineering**:
The role responsible for implementation and technical diagnosis.

**Quality**:
The role responsible for independent review and validation.

**Skill**:
A reusable working method an agent applies while fulfilling a role; a role may use several skills.
_Avoid_: Agent (a skill is not itself an agent)

**Intervention**:
An explicit period of direct human interaction with an agent outside the normal Coordination conversation, with automated input paused and resulting decisions or changes recorded for its owner.
