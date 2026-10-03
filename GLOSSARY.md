# AsmAI

A personal software engineering factory that can serve multiple repositories.

## Language

**AsmAI**:
The product name of the personal software factory, meaning AssemblyAI.

**Factory**:
The coordinated group of agents that carries out software engineering work for the user across repositories.
_Avoid_: Repository (a factory is not tied to one repository)

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

**Handoff**:
A request for another leader to take responsibility for a defined outcome, carrying the context and acceptance criteria needed to accept, clarify, or decline it.

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
