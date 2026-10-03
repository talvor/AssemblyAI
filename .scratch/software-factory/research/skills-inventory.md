# Skills inventory for the software factory

Research date: 2026-10-03. This answers [Map Matt Pocock skills to factory roles](../issues/02-skills-inventory.md). Proposed responsibilities below are options for the later role-design decision, not an approved roster.

## Findings

Skills fit responsibilities; they do not each require a permanent agent. The installed collection already combines several skills in a workflow and delegates bounded execution to subagents. A leader can own a responsibility, communicate with other leaders, and dispatch workers with the relevant subset of skills. Preserve a separate human-decision step wherever a skill requires one: a leader consulting another leader is not human grilling.

There are **37 Matt Pocock skill entry points installed**, plus **three other direct skill folders**. All 37 entry files and all 101 installed files beneath those 37 directories exactly match the Git blob hashes in the current upstream tree. No differences or extra local files were found inside those directories. This verifies content identity at inspection time, not installation history, authorship of every contribution, or future compatibility.

## Sources and provenance

The primary workflow sources are the actual installed files linked in each inventory row. Source discovery used `rg --files /home/phillip/.agents/skills -g SKILL.md`; this inventory covers immediate skill directories only. The separate `synced/` collection contains unrelated assistant/application skills and is deliberately excluded.

Upstream verification used the [Matt Pocock skills Git tree API](https://api.github.com/repos/mattpocock/skills/git/trees/d81f3a183412e71a5b1e84ca21bc1a35eea03a60?recursive=1), fetched with `gh api repos/mattpocock/skills/git/trees/main --method GET -f recursive=1`. Snapshot tree SHA: `d81f3a183412e71a5b1e84ca21bc1a35eea03a60`. Each local file was hashed as a Git blob (`sha1("blob " + byte_length + NUL + bytes)`) and compared with its upstream path. The immutable tree identifies the snapshot; it is not asserted to be a commit SHA. The [upstream collection](https://github.com/mattpocock/skills) is the source repository, not an endorsement of every optional workflow for this factory.

`lavish`, `no-mistakes`, and `find-skills` do not appear in that upstream tree. Lavish's local metadata credits Kun Chen. The no-mistakes local file links its separate product documentation. The find-skills installation's origin was not established. Do not describe these as Matt Pocock skills. The `pr` skill belongs to the verified upstream collection but explicitly credits the Humanlayer `show-me` skill by Dex Horthy.

Upstream categorizes six entries as `in-progress`: `claude-handoff`, `loop-me`, `setup-ts-deep-modules`, `writing-beats`, `writing-fragments`, and `writing-shape`. That is a provenance/category fact, not proof they are unsuitable.

## Complete inventory

“Human” indicates the human interaction encoded in the skill, not an additional blanket approval requirement. Existing user decisions and standing authorization should be carried into a worker brief rather than repeatedly requested. The responsibility column is proposed placement.

| Skill and primary source | Proposed responsibility/use | Human gate or sequencing constraint |
| --- | --- | --- |
| [ask-matt](/home/phillip/.agents/skills/ask-matt/SKILL.md) | Coordinator: route requests into appropriate skill flows. | User-invoked router; main flow runs discovery → spec → tickets → implementation → retrospective. Wayfinder hands off to synthesis rather than immediately building. |
| [wayfinder](/home/phillip/.agents/skills/wayfinder/SKILL.md) | Planning: maintain a decision map for work larger than one session. | Name destination with human first; chart without hand-resolving tickets; claim before work; one non-research ticket per session. Grilling/prototype tickets need live human exchange; research can resolve concurrently. |
| [grilling](/home/phillip/.agents/skills/grilling/SKILL.md) | Coordinator-facing decision work, informed by specialist leaders. | Ask only the settled-prerequisite frontier, with recommendations; wait for user answers; facts delegated to exploration. Human confirms shared understanding before acting. Another agent must not impersonate the user. |
| [domain-modeling](/home/phillip/.agents/skills/domain-modeling/SKILL.md) | Planning/design and documentation: canonical terms and selective ADRs. | Challenge fuzzy terms with concrete scenarios; update glossary when resolved, not as speculation. ADRs only for hard-to-reverse, surprising, genuine trade-offs. Glossary excludes implementation details. |
| [grill-with-docs](/home/phillip/.agents/skills/grill-with-docs/SKILL.md) | Planning: stateful discovery in a repository. | Wrapper invokes both grilling and domain-modeling; inherits the real human decision loop. |
| [grill-me](/home/phillip/.agents/skills/grill-me/SKILL.md) | Coordinator: stateless interview without repository artifacts. | Wrapper invokes grilling; choose when no persistent repo discussion is needed. |
| [research](/home/phillip/.agents/skills/research/SKILL.md) | Research: background reading workers. | Agent does the legwork; primary sources, cited single Markdown result. It supplies facts for decisions, not authority to decide product behavior. |
| [prototype](/home/phillip/.agents/skills/prototype/SKILL.md) | Design/prototyping: workers produce concrete experiments. | Choose logic/state versus UI question. Review verdict with human in wayfinder. Capture throwaway artifact on a separate branch with a pointer; no production polish/tests by default. |
| [to-spec](/home/phillip/.agents/skills/to-spec/SKILL.md) | Planning: synthesize resolved decisions into a buildable spec. | No new interview as substitute for synthesis; explicitly check testing seams with user, then publish to configured tracker. Unresolved decisions should remain visible. |
| [to-tickets](/home/phillip/.agents/skills/to-tickets/SKILL.md) | Planning: implementation task graph. | Human approves granularity, edges, and split/merge choices before publishing. Vertical tracer bullets; wide refactors can use expand–contract. These are implementation tickets, distinct from decision tickets. |
| [implement](/home/phillip/.agents/skills/implement/SKILL.md) | Implementation worker: one specified item. | TDD where possible at pre-agreed seams, regular focused checks, final suite and code-review, commit current branch. Supply isolated correct branch/worktree in brief. |
| [implement-spec](/home/phillip/.agents/skills/implement-spec/SKILL.md) | Delivery coordination: dispatch ready implementation workers. | Workers use separate worktrees/branches based on integration branch; merger subagent integrates; run integration code-review after all work. Draft PR after first merge, ready after review. Requires spec and task graph first. |
| [tdd](/home/phillip/.agents/skills/tdd/SKILL.md) | Implementation/testing: executable behavioral slices. | Test seams must be recorded and confirmed by user before tests. One failing behavioral test then minimal implementation at a time. Review handles refactoring; do not replace this with all tests first. |
| [code-review](/home/phillip/.agents/skills/code-review/SKILL.md) | Quality: independent Standards and Spec reviewers. | Pin valid non-empty comparison and spec source; ask if missing. Run two parallel reviewers, report axes separately; repo standards override heuristic smells. |
| [diagnosing-bugs](/home/phillip/.agents/skills/diagnosing-bugs/SKILL.md) | Diagnosis: reproduce and minimize before repair. | No hypothesis phase without tight red-capable command; ask for missing environment/artifacts if necessary. Show ranked hypotheses but can proceed AFK. Correct regression seam or document absence; redact secrets. |
| [triage](/home/phillip/.agents/skills/triage/SKILL.md) | Intake: raw external requests and configured external PRs. | Recommend category/state and wait for maintainer direction, verify claim, grill if needed. Explicit state override authorizes direct transition. Do not retriage agent-ready generated tickets. |
| [codebase-design](/home/phillip/.agents/skills/codebase-design/SKILL.md) | Design: shared deep-module and seam vocabulary. | Reference layer, not another persistent agent. Alternative-interface exploration can delegate parallel proposals; user-facing choices remain choices. |
| [improve-codebase-architecture](/home/phillip/.agents/skills/improve-codebase-architecture/SKILL.md) | Architecture: survey hot spots and deepening opportunities. | Exploration worker → visual candidates → human selects → grilling. Do not jump from survey to implementation or choose interfaces before discussion. |
| [retro](/home/phillip/.agents/skills/retro/SKILL.md) | Quality/process improvement: learn from session evidence. | Present improvement candidates; deterministic checks for mechanical failures, standards for judgment. Produces suggestions rather than silent process-policy changes. |
| [pr](/home/phillip/.agents/skills/pr/SKILL.md) | Delivery: explain changes with evidence and merge risk. | Shapes PR body; does not itself grant merge authority. Before/after evidence, concise visual summary, reversibility and blast radius. |
| [setup-matt-pocock-skills](/home/phillip/.agents/skills/setup-matt-pocock-skills/SKILL.md) | Factory setup: tracker, triage vocabulary, domain-document pointers. | Explore then present/confirm choices and file drafts. Single-context defaults unless evidence says otherwise. If neither agent instruction file exists, user chooses which to create. |
| [wizard](/home/phillip/.agents/skills/wizard/SKILL.md) | Setup/operations: prepare genuinely human-only steps. | Confirm stages and destinations, generate script, static-check and hand off. Human executes; confirm irreversible actions. Do agent-runnable tasks directly instead. |
| [handoff](/home/phillip/.agents/skills/handoff/SKILL.md) | All leaders: portable context across harnesses/directories. | Temp Markdown pointer document, suggested skills, secrets redacted. Does not itself schedule execution. |
| [claude-handoff](/home/phillip/.agents/skills/claude-handoff/SKILL.md) | Optional harness adapter for fresh background session. | Uses Claude-specific `claude --bg --name`; adapt capability at runtime rather than assume cross-provider support. In-progress upstream. |
| [writing-for-agents](/home/phillip/.agents/skills/writing-for-agents/SKILL.md) | Setup/process/documentation: durable worker instructions. | Shared reference for skill/steering-file design: pointers, progressive disclosure, explicit completion criteria. Not an autonomous runtime or its own roster member. |
| [wait-what](/home/phillip/.agents/skills/wait-what/SKILL.md) | Coordinator: repair an explanation that did not land. | Explicit user-triggered re-explanation using glossary and plain technical English. |
| [to-questionnaire](/home/phillip/.agents/skills/to-questionnaire/SKILL.md) | Research/product: gather facts held by another human. | Ask user who receives it and what is needed; create questionnaire. Writing it does not send it or answer it on recipient's behalf. |
| [loop-me](/home/phillip/.agents/skills/loop-me/SKILL.md) | Optional workflow design for recurring factory operations. | Stateful grilling; spec done only when no implementer questions remain. Does not mandate AI, checkpoint, or schedule. In-progress. |
| [setup-pre-commit](/home/phillip/.agents/skills/setup-pre-commit/SKILL.md) | Setup/quality: JavaScript repo guardrails. | Installs Husky/lint-staged/Prettier, adapts package manager and scripts, verifies/commits. Language-specific optional integration, not universal scaffold. |
| [setup-ts-deep-modules](/home/phillip/.agents/skills/setup-ts-deep-modules/SKILL.md) | Setup/architecture: enforce TypeScript module entry points. | Confirm conflicting existing layout; merge config; prove pass/fail/pass behavior. In-progress and TypeScript-specific. |
| [git-guardrails-claude-code](/home/phillip/.agents/skills/git-guardrails-claude-code/SKILL.md) | Setup/security: Claude tool-hook restrictions. | Ask project/global scope and customization. Blocks push and destructive Git commands; reconcile with authorized delivery workflow rather than silently bypass. Claude-specific. |
| [migrate-to-shoehorn](/home/phillip/.agents/skills/migrate-to-shoehorn/SKILL.md) | Optional implementation/test maintenance for TypeScript. | Establish target test data; tests only, never production. Install library, migrate assertions, typecheck. Not a core factory responsibility. |
| [scaffold-exercises](/home/phillip/.agents/skills/scaffold-exercises/SKILL.md) | Optional educational-content implementation. | Requires the AI Hero course layout/linter; create from plan, lint, commit. Not generic project scaffolding. |
| [teach](/home/phillip/.agents/skills/teach/SKILL.md) | Optional onboarding/learning assistant. | Human learning mission, primary sources, interactive lessons and learning records; confirm mission changes. Separate from software delivery. |
| [writing-fragments](/home/phillip/.agents/skills/writing-fragments/SKILL.md) | Optional product writing/name exploration notes. | Interview human, append raw fragments without imposing structure; ask destination if unknown. In-progress. |
| [writing-shape](/home/phillip/.agents/skills/writing-shape/SKILL.md) | Optional longer product documentation. | Human picks opening and agrees each block; raw material immutable, user decides done. In-progress. |
| [writing-beats](/home/phillip/.agents/skills/writing-beats/SKILL.md) | Optional guided narrative writing. | User chooses each next beat; write only chosen beat, reread edits. In-progress; alternative to writing-shape, not mandatory extra stage. |
| [lavish](/home/phillip/.agents/skills/lavish/SKILL.md) | Coordinator presentation: visual questions and feedback. | Separate integration. CLI owns current workflow. User has requested this channel for questions; preserve real review/answer event and working feedback loop. |
| [no-mistakes](/home/phillip/.agents/skills/no-mistakes/SKILL.md) | Delivery/quality integration: validation pipeline and PR readiness. | Separate product, not Matt skill. Outer driver owns pipeline; phase workers do assigned phase only. Detailed ownership and gate restrictions below. |
| [find-skills](/home/phillip/.agents/skills/find-skills/SKILL.md) | Optional setup discovery of additional capabilities. | Not in verified Matt tree; provenance unresolved. Search/verify then offer installation; not authority to install arbitrary extensions or expand scope. |

## Applying the workflow to leader and worker agents

These are architectural implications inferred from the skill contracts, not settled product decisions.

1. **Give each selected responsibility one leader, with several skills available.** Planning may combine wayfinder, grilling, domain-modeling, to-spec, and to-tickets. Research workers use research; implementers use implement/tdd; reviewers use code-review. A skill is a procedure or reference, a role is responsibility, and a worker is a bounded execution instance. This supports the stated one-leader-per-role direction without deciding the number or names of roles.
2. **Keep one human-facing coordinator.** Specialist leaders can prepare evidence and recommendations and communicate with each other. Genuine grilling questions reach the human through that coordinator's Lavish surface. Record which human answer or standing authorization settles a decision. A delegated technical decision should be explicitly marked as delegated, with constraints, decision owner, result and rationale; it must not masquerade as a completed HITL ticket.
3. **Separate decision work from build work.** Wayfinder maps uncertain decisions. Once clear, to-spec synthesizes; to-tickets produces the implementation graph. A decision ticket being closed does not mean code was built. Research completion may unblock a human choice rather than close that choice.
4. **Pass durable pointers and authority with work.** A worker brief should carry the task/spec, accepted decisions, permitted changes, approved test seams, relevant glossary/ADRs, isolated worktree/branch, completion evidence, and escalation route. Include skill invocation intent where a skill is user-invoked; do not infer unlimited permission from its presence on disk.
5. **Retain ownership boundaries.** Workers may gather facts while human decisions wait; dependent implementation must wait for required decisions. Integration, review, publication, and user acceptance remain distinct states. The skills do not specify a general leader messaging bus, worker persistence, crash recovery, budgets, or provider protocol; those remain product decisions.
6. **Share the TDD seam approval once.** to-spec and tdd both mention it. Carry the approved seam artifact forward so the factory does not repeatedly ask the same question. Changed interfaces or new seams require surfacing the new decision.

The installed [ask-matt flow](/home/phillip/.agents/skills/ask-matt/SKILL.md) supports this sequence: repository setup → discovery (wayfinder for large foggy work, grill-with-docs for smaller work) → to-spec → to-tickets → implement/implement-spec → review/PR → retro. Prototype/research are evidence-producing detours. Raw incoming reports enter via triage, while bugs needing diagnosis enter via diagnosing-bugs. The [phase-boundary reference](/home/phillip/.agents/skills/ask-matt/PHASE-BOUNDARIES.md) is the place to consult for context-window transitions, rather than turn every skill boundary into a new agent.

## no-mistakes integration requires explicit custody

The following describes the installed [no-mistakes instructions](/home/phillip/.agents/skills/no-mistakes/SKILL.md), not an independently tested runtime integration:

- Input is committed feature-branch history, initialized repo configuration and a runnable pipeline agent. Preserve the user's full intent including decisions, constraints and acceptance criteria.
- The outer AXI driver starts/reattaches and responds to pipeline gates. An agent already executing a validation step only inspects, fixes and returns its assigned phase; it must not start a nested pipeline, push directly, or take over other phases.
- During an active run the pipeline owns findings and fixes. Other factory agents must not edit the same branch to fix findings or abort/restart to circumvent a gate. Return a fix instruction to the outer executor; recover/synchronize custody only by the reported structured action.
- Ordinary `ask-user` findings require human response, with exact finding details relayed. Explicit consent to drive the whole run unattended permits `--yes` for eligible gates; it is not the default.
- Even under `--yes`, protected-path refusals require explicit operator handling. Unvalidated work left by a timed-out Test agent requires another validation budget or abort; it must not be approved or skipped into publication.
- `checks-passed` means ready for human PR review/merge, not merged. Overrides, missing verification and skipped steps must be reported accurately. `passed` alone is not evidence of merge.

This fits a tested-PR destination, but adopting the tool, deciding which leader drives it, and allocating review/test responsibilities between factory workers and its phase agents are still choices. Avoid two competing orchestrators owning the same Git work simultaneously.

## Remaining decisions this research does not settle

- Final leader roster, names, persistence and communication rules.
- Which decisions can be delegated and which always return to the human.
- Required versus optional skill bundle and treatment of upstream `in-progress` entries.
- Pinning/updating skill versions, local overrides and licensing/distribution details.
- Runtime/provider compatibility, isolated worker lifecycle and recovery.
- Whether no-mistakes is the default delivery integration and how its custody is represented.
- Product name: none of the reviewed skills selects it or establishes availability.

No skills were installed or edited. No product role roster or human decision ticket was resolved by this research.
