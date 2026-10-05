
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
- **Confirmation:** CONFIRMATION_PLACEHOLDER

Facts checked on 2026-10-05, used as evidence and not as qualification:
- otman: Go, CI (`go vet`, `go test`, a cross-platform build) green on 2026-10-05, 52 PRs; its own otman tracker holds only four test items.
- dev-setup: Shell and Nix, one test script, no CI workflow.
- This host: Linux x86_64 (Pop!_OS), Ghostty, no tmux, QEMU with KVM; Claude Code 2.1.283, Codex 0.157.0, Lavish 0.1.79.

The board, the round-by-round questions and answers, the gathered case list, ADR 0008 and the glossary terms were produced in a disposable worktree and are being archived separately.
