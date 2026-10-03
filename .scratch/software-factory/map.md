# Chart AsmAI

Label: wayfinder:map

## Destination

An implementation-ready v1 specification for AsmAI, a CLI-managed, repository-independent personal software factory: one user-facing agent, role leaders and workers, and delivery of tested pull requests plus standalone engineering work. Settle enough workflow and architecture decisions that implementation can begin without unresolved foundational choices.

## Notes

- Planning only. Charting is complete; subsequent sessions resolve decision tickets. No factory implementation is authorized by the map itself.
- Consult wayfinder, grilling, and domain-modeling. Present all questions in Lavish. Consult research or prototype for those ticket types.
- First customer: Phillip. Browser interaction is primary; terminal conversation is desirable and its v1 scope remains to be decided.
- The factory is independent of a repository and must support concurrent independent work across repositories.
- Both local and remote hosts are in v1 scope. Investigate persistent sessions, tmux, and supervision; none is selected yet.
- Canonical vocabulary: role, leader, worker, skill; see ../../GLOSSARY.md. Each role has exactly one leader; leaders coordinate and make decisions within their roles, spawning workers for execution.
- One agent is the user's conversational counterpart and drives delivery, making reasonable decisions and involving the user when the path is unclear. The precise assignment to a role remains to be specified.
- Preserve human grilling and wayfinder participation; define separate delegated decision steps for autonomous leaders.
- Account for Matt Pocock skills across roles, particularly wayfinder and grilling. Roles use multiple skills.
- Leave Claude-versus-Codex selection open. Mixed staffing and runtime configurability need investigation, not an assumed provider choice.
- Firstmate and mvschwarz/openrig (confirmed by Phillip in Lavish) are an ideas pool, not selected dependencies.
- Tracker: local Markdown fallback, per /home/phillip/.agents/skills/setup-matt-pocock-skills/issue-tracker-local.md. Open tickets have no Status line; claimed/resolved statuses follow that document. Query child files numerically for the unblocked, unclaimed frontier.
- The workspace has no usable Git repository and its .git is read-only. Research agents use isolated temporary research branches and link their checked-in findings here; implementation must resolve repository setup separately when needed.
- Map scope confirmed by Phillip in Lavish after charting.
- Source of scope: live Lavish rounds, retained in ../../.lavish/wayfinder-answers.json. Research findings are facts and recommendations, not user decisions.

## Decisions so far

<!-- Resolution index only. Scope preferences from charting live in Notes. -->

- [Research agent runtimes and persistent sessions](issues/03-runtime-and-hosting.md): Structured integration is available; conversation, process, and task persistence need separate contracts, and tmux alone does not establish leader ownership.

- [Research Firstmate and Openrig coordination patterns](issues/01-reference-systems.md): Durable ownership and retryable notifications inform the design; the user confirmed mvschwarz/openrig as the intended reference.

- [Map Matt Pocock skills to factory roles](issues/02-skills-inventory.md): 37 verified upstream skills plus three integrations; proposed role groupings preserve human decision gates and worker ownership boundaries.

- [Choose the AsmAI product name](issues/12-product-name.md): AsmAI, meaning AssemblyAI, selected explicitly by Phillip.

## Not yet specified

- Concrete configuration schemas, agent prompts, provider adapters, and message/storage design depend on role and lifecycle choices.
- How much workflow variation is needed for different engineering tasks, repository conventions, and skill combinations.
- Browser presentation details and how durable agent context should appear to the user after long absences.
- Product distribution and migration details after the installation model is chosen.
- The final specification's structure and implementation sequencing once the foundational route is clear.

## Out of scope

- Building or deploying the factory in this wayfinding effort; the destination is the v1 specification.
- Coordinated features spanning multiple repositories in v1; the chosen scope is concurrent independent jobs.
- Automatic production deployment as the default deliverable; the agreed delivery target is a tested pull request.
