## Resolution — confirmed by Phillip in Lavish

### Where skills come from
- **Bundled and pinned.** Each AsmAI release embeds one upstream release of Matt Pocock's skills, with its MIT notice, plus AsmAI's own adaptations, inside the executable. Agents use only this **skill bundle**, never personal copies.
- **Updates.** A newer upstream release reaches agents only through a newer AsmAI release, after it is qualified. `asmai doctor` says when upstream has a newer release.
- **Contents.** The bundle is upstream's own promoted set: its engineering and productivity folders, 27 skills at v1.3.1. An upstream in-progress skill enters the bundle when upstream graduates it and an AsmAI release qualifies it.
- **Upgrades.** Each dispatch records the bundle version it ran with, plus a fingerprint of any added or repository skill. After an upgrade, work continues on the new bundle from the next dispatch, and `asmai doctor` lists what changed.

### Fitting upstream skills to the factory
- **Unchanged text plus a guide.** Upstream text ships unchanged. AsmAI's role instructions carry one operating guide that maps single-agent phrasing onto AsmAI:
  - "ask the user" or "wait for the user" means a decision request;
  - subagents mean worker assignments, or handoffs (a prototype to Engineering, research to Research);
  - worktrees mean workspaces and assignment branches;
  - an integration branch means the job branch the daemon fast-forwards;
  - "tell the human to run setup-matt-pocock-skills" means Coordination's repository setup.
- **Patches are the exception.** A skill is patched only where the guide cannot work. Each patch is listed with its reason and rechecked whenever the pinned release moves.

### Who runs skills
- **Workers run the skills, in every role.** Each leader gets an index of its workers' skills: name, purpose, when it applies, and whether it starts only on request. The leader names the skill in the assignment, the way Phillip tells Firstmate "Use the wayfinder skill in <repo> for ticket #1".
- **Coordination's own list** holds ask-matt, the map of flows it routes by, and wait-what, for re-explaining in its own conversation.
- **Narrowing.** An assignment may narrow its worker's list.
- **Questions to Phillip.** A worker's grilling and Wayfinder questions reach Phillip as decision requests, through its owning leader and Coordination.
- **User-invoked skills.** 22 of the 40 skills, including wayfinder, to-spec, to-tickets, implement, triage and retro, are marked user-invoked. One starts only when Phillip's request or the job's mandate calls for that kind of outcome; a tested-PR mandate covers to-spec, to-tickets, implement and code-review. Otherwise Coordination proposes the skill to Phillip as a decision.

### Default skill lists
| Role | Leader | Workers |
| --- | --- | --- |
| Coordination | ask-matt, wait-what, plus the index | setup-matt-pocock-skills |
| Planning | the index | wayfinder, grilling, grill-with-docs, grill-me, domain-modeling, codebase-design, to-spec, to-tickets, triage, to-questionnaire, writing-for-agents |
| Research | the index | research, to-questionnaire |
| Engineering | the index | implement, tdd, diagnosing-bugs, prototype, codebase-design, improve-codebase-architecture, pr, wizard, writing-for-agents |
| Quality | the index | code-review, retro, tdd |

- **Optional** (shipped, but on no list until added): handoff, teach and implement-spec. The Engineering leader's own instructions cover working through a ticket graph, assigning each ready ticket to a worker with implement and tdd.
- **Not shipped:**
  - upstream misc: git-guardrails-claude-code, migrate-to-shoehorn, scaffold-exercises, setup-pre-commit;
  - upstream in progress: claude-handoff, loop-me, setup-ts-deep-modules, writing-beats, writing-fragments, writing-shape;
  - lavish, because the daemon owns Lavish and renders decision requests;
  - find-skills, because it installs skills from the internet.

  Any of these can be an added skill.
- **no-mistakes** is placed by [Choose validation and delivery ownership](https://github.com/talvor/AssemblyAI/issues/18).

### Visibility and delivery
- **Agents see only their skill list.** Every time AsmAI starts an agent, it hides the user's personal skills, provider built-in skills wherever the provider allows, and repository skills unless they are switched on.
- **What cannot be hidden.** Whatever a pinned provider version cannot hide is listed by `asmai doctor`, and the operating guide tells agents to use only their list. Qualification proves the hiding for each provider version.
- **Claude** receives a per-session plugin (`--plugin-dir`), and the user setting source is left out.
- **Codex** has no per-session skill directory in 0.157.0, so AsmAI writes the skills into `.agents/skills/asmai-<name>/` inside the workspace when it creates it. The clone's own exclude file hides them from git. A leader gets the same inside its own AsmAI directory, and a repository's own `.agents/skills` folders are left untouched. AsmAI switches to a native per-session option once a qualified Codex version offers one.

### Added and repository skills
- **Added skills.** The configuration can add skill directories to any role's leader or worker list. One with the same name as a shipped skill replaces it for that role.
  - They are copied when an agent starts, so editing them never changes a running agent; `asmai config apply` shows which agents pick them up.
  - `asmai doctor` and `asmai status` mark them as the user's and unqualified.
- **Repository skills** (in `.claude/skills` or `.agents/skills`) are off by default and hidden. Per-repository configuration can switch them on for named roles, for jobs in that repository. They are then marked as the repository's and unqualified.

### Repository setup and reuse of decisions
- **Where the setup lives.** A repository's skill setup lives in the repository: `docs/agents/issue-tracker.md`, `triage-labels.md` and `domain.md`, plus a block in AGENTS.md or CLAUDE.md.
- **When it runs.** When Phillip adds a repository with `asmai repo add` and it has no `docs/agents/issue-tracker.md`, Coordination opens a setup job straight away. With that file present, nothing happens.
  - A Coordination worker runs setup-matt-pocock-skills, and its questions reach Phillip as decision requests.
  - The files go on that job's branch and PR.
  - The answers are recorded for that repository, so a job that starts before the PR merges receives them as repository instructions.
- **Reusing decisions at a skill's human steps.** These include tdd and to-spec test seams, to-tickets approval, code-review's comparison point and spec, and wizard stages.
  - A step is satisfied by a recorded decision of Phillip's, or a grant, whose scope covers it: the job's decisions in its brief, the repository's setup, or a factory-wide grant.
  - A worker never asks Phillip directly. It sends a decision request to its owning leader, who answers from the records or escalates through Coordination, and the worker's result names the record it relied on.
  - A step the records do not cover goes to Phillip, and his answer is recorded for the rest of the job.
  - Grilling and Wayfinder questions still need Phillip's own answer.

### Glossary and ADR
- [GLOSSARY.md](https://github.com/talvor/AssemblyAI/blob/main/GLOSSARY.md) gains **Skill bundle**, **Skill list**, **Added skill** and **Repository skill** (pending archive).
- [ADR 0006](https://github.com/talvor/AssemblyAI/blob/main/docs/adr/0006-agents-use-only-the-pinned-skill-bundle.md) records that agents use only AsmAI's pinned skill bundle, passed per session (pending archive).

### Deferred to existing tickets
- [Choose validation and delivery ownership](https://github.com/talvor/AssemblyAI/issues/18): whether no-mistakes is adopted and on which list, and who opens the PR that the pr skill shapes.
- [Define v1 acceptance scenarios and evidence](https://github.com/talvor/AssemblyAI/issues/12): qualify, per provider version:
  - hiding personal, built-in and repository skills, including Claude's built-in code-review alongside the shipped one;
  - per-session skill delivery, since Claude names plugin skills like `asmai-planning:grilling` while upstream skills call each other by bare name;
  - Codex finding skills in the workspace.
- [Choose license, release packaging and upgrade migration](https://github.com/talvor/AssemblyAI/issues/20): releases carry the upstream MIT notice for the bundled skills.

### Map follow-through
- **No new ticket.**
- **Configuration and prompts fog.** The configuration schema fog now also covers skill-list fields, added skills and repository-skill switches. The agent prompts it covers include the operating guide and the leaders' skill indexes.
- **Workflow-variation fog.** Narrowed: the skill lists for each role, and when a leader assigns a skill, are settled here.
- **No implementation.** This is a planning resolution; it authorizes no implementation.

### Evidence
Three live Lavish rounds on 2026-10-05 (18 questions with recommendations), then confirmation. The answers are recorded verbatim here:
- **Round 1:**
  - Q1 A (bundled in each AsmAI release; updates arrive with AsmAI releases)
  - Q2 **B, with notes:** "setup-matt-pocock-skills should move to coordinator and is used when a new repository is added or introduced to the factory. For the "planning" skills, the actual work should be done by the workers, so skills like "wayfinder", "grillme" should be actually run by the worker. So the leader needs to know when to forward the job to the worker to initiate the skill. E.g. When I am using "firstmate" I will say to firstmate something like "Use the wayfinder skill in <repo> for ticket #1""
  - Q3 A (upstream text unchanged plus an operating guide)
  - Q4 A (the request or mandate invokes it; otherwise Coordination proposes it)
  - Q5 A (add or replace per role; copied at agent start; marked as mine and unqualified)
  - Q6 A (only their list; hide what can be hidden; doctor lists the rest)
  - Q7 A (Codex: the workspace's .agents/skills, excluded from git)
  - Q8 A (repository skills off unless switched on per repository and role)
  - Q9 A (in the repository; its timing is superseded by the Q2 note)
  - Q10 A (satisfied from recorded decisions and grants)
- **Round 2:**
  - R2-Q1 A (every role: workers run skills; leaders get an index)
  - R2-Q2 not answered, so asked again in round 3
  - R2-Q3 A (a setup job when the repository is added; recorded answers usable before the PR merges), note: "Only required if the repo does not have the "docs/agent/issue-tracker.md" file"
  - R2-Q4 A (record the bundle version per dispatch; continue on the new bundle)
  - R2-Q5 A (the four glossary terms)
  - R2-Q6 A (ADR 0006 as drafted)
- **Round 3:**
  - R3-Q1 A (implement-spec optional, on no list)
  - R3-Q2 A (docs/agents/issue-tracker.md alone decides)
- **Confirmation:** CONFIRM "Confirm and record", on a page holding this resolution.

Facts checked on 2026-10-05, used as evidence and not as qualification:
- Upstream is MIT-licensed and tagged, at v1.3.1.
- The copies installed on the host match upstream as of 2026-10-03.
- Claude Code 2.1.283 probe: leaving out the user setting source hid personal skills, and `--plugin-dir` added namespaced plugin skills.
- Codex 0.157.0 probe: `-c skills.config=[{path=…,enabled=false}]` hid a named personal skill, a workspace `.agents/skills` folder was discovered, and `skills.extra_roots` is not accepted.

The board, the round-by-round questions and answers, ADR 0006 and the glossary terms were produced in a disposable worktree and are being archived separately.
