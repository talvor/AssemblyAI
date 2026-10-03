# Research agent runtimes and persistent sessions

Status: resolved
Assignee: Phillip
Researcher: research_runtime
Type: research
Label: wayfinder:research
Parent: ../map.md

## Question

What supported integration mechanisms can run Codex and Claude agents on local and remote hosts, preserve sessions, spawn workers, and report completion? Examine tmux, process supervision, restart recovery, and browser/terminal disconnection separately. Clarify authentication/subscription constraints from primary sources without choosing a runtime. Evaluate one active leader per role as an invariant, not a particular implementation.

## Answer

[Runtime and hosting findings](../research/runtime-and-hosting.md) establish structured integration surfaces, separate conversation/process/task persistence, and define leadership as an authority invariant. Runtime, recovery guarantees, and billing remain product decisions.

## Research context

Isolated repository: `/tmp/wayfinder-runtime-qpj5aijf`

Branch: `research/runtime-and-hosting`

Commit: `294d4862a89217cc50b429fac1ff63e08a762c5a` (unsigned research snapshot).

The workspace Git metadata is unavailable/read-only, so research was committed in an isolated temporary repository.
