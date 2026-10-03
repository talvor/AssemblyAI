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
The agent accountable for decisions and coordination within a role. Each role has exactly one leader; leaders communicate with other leaders and delegate execution to workers.
_Avoid_: Worker (leaders and workers have different responsibilities)

**Worker**:
An agent spawned by a role's leader to carry out delegated work.

**Skill**:
A reusable working method an agent applies while fulfilling a role; a role may use several skills.
_Avoid_: Agent (a skill is not itself an agent)
