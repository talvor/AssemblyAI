# 08 Skills and agent instructions

This document specifies the working methods agents use and what they are told: the skill bundle and the operating guide, skill lists and the leaders' skill indexes, delivering skills to each provider and hiding everything else, added and repository skills, repository setup, reusing recorded decisions at skills' human steps, and what each role's instructions, the operating guide, the skill indexes and the PR section in workers' results must contain. It sets their required content; their exact wording is written during implementation and proved by the proving scenarios ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27)).

## Rules

### The skill bundle

1. **Bundled and pinned.** Each AsmAI release embeds one upstream release of Matt Pocock's skills, unchanged and with its MIT notice, plus AsmAI's own adaptations, inside the executable. Agents use only this skill bundle, never the user's personal copies ([AssemblyAI#17](https://github.com/talvor/AssemblyAI/issues/17), [ADR 0006](https://github.com/talvor/AssemblyAI/blob/main/docs/adr/0006-agents-use-only-the-pinned-skill-bundle.md), [10](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/10-release-install-and-upgrade.md)).
2. **Contents.** The bundle is upstream's own promoted set: its engineering and productivity folders, 27 skills at upstream v1.3.1. An upstream in-progress skill enters the bundle when upstream graduates it and an AsmAI release qualifies it ([AssemblyAI#17](https://github.com/talvor/AssemblyAI/issues/17)).
3. **Not shipped:** upstream's misc skills (git-guardrails-claude-code, migrate-to-shoehorn, scaffold-exercises, setup-pre-commit); its in-progress skills (claude-handoff, loop-me, setup-ts-deep-modules, writing-beats, writing-fragments, writing-shape); lavish, because the daemon owns Lavish and renders decision requests; and find-skills, because it installs skills from the internet. Any of these can be an added skill ([AssemblyAI#17](https://github.com/talvor/AssemblyAI/issues/17)). no-mistakes is not shipped either and is on no skill list, because v1 does not adopt it ([AssemblyAI#18](https://github.com/talvor/AssemblyAI/issues/18), [ADR 0007](https://github.com/talvor/AssemblyAI/blob/main/docs/adr/0007-asmai-delivers-tested-prs-with-its-own-roles.md)).
4. **Updates come with releases.** A newer upstream release reaches agents only through a newer AsmAI release, after it is qualified, because the skill text, the operating guide and the provider pins are qualified together. `asmai doctor` says when upstream has a newer release. The user's personal copies keep updating freely ([AssemblyAI#17](https://github.com/talvor/AssemblyAI/issues/17), [ADR 0006](https://github.com/talvor/AssemblyAI/blob/main/docs/adr/0006-agents-use-only-the-pinned-skill-bundle.md)).
5. **After an upgrade,** work continues on the new bundle from the next dispatch, and `asmai doctor` lists what changed. Each dispatch records the bundle version it ran with ([AssemblyAI#17](https://github.com/talvor/AssemblyAI/issues/17), [02](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/02-daemon-and-store.md)).

### The operating guide

6. **Upstream text plus one guide.** Upstream text ships unchanged. Every agent's instructions carry one operating guide that maps the skills' single-agent phrasing onto the factory ([AssemblyAI#17](https://github.com/talvor/AssemblyAI/issues/17), [ADR 0006](https://github.com/talvor/AssemblyAI/blob/main/docs/adr/0006-agents-use-only-the-pinned-skill-bundle.md)).
7. **The mappings** ([AssemblyAI#17](https://github.com/talvor/AssemblyAI/issues/17), [AssemblyAI#18](https://github.com/talvor/AssemblyAI/issues/18)):

| A skill says | In AsmAI it means |
| --- | --- |
| "Ask the user", "wait for the user" | A decision request ([01](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/01-roles-and-decisions.md)) |
| Subagents | Worker assignments, or handoffs to another role (a prototype to Engineering, research to Research) |
| Worktrees | Workspaces and assignment branches ([05](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/05-repositories-and-job-branches.md)) |
| An integration branch | The job branch, which the daemon fast-forwards |
| "Tell the human to run setup-matt-pocock-skills" | Coordination's repository setup (rules 27 to 31) |
| implement's "use /code-review" | Asking the Engineering leader for Quality's validation ([06](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/06-validation-and-delivery.md)) |
| The pr skill, in a worker | Writing the PR section into the result instead of opening a pull request |
| "Commit your work to the current branch" | The assignment branch |

8. **Only the skill list.** The guide tells agents to use only the skills on their list, which matters wherever a provider cannot hide the rest (rule 19) ([AssemblyAI#17](https://github.com/talvor/AssemblyAI/issues/17)).
9. **Grilling and Wayfinder questions** are emitted as structured decision requests (each question with an id, title, body, options and a recommendation) for the daemon to render in Lavish ([AssemblyAI#10](https://github.com/talvor/AssemblyAI/issues/10), [04](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/04-conversation-and-lavish.md)).
10. **Patches are the exception.** A skill is patched only where the guide cannot work. Each patch is listed with its reason and rechecked whenever the pinned upstream release moves ([AssemblyAI#17](https://github.com/talvor/AssemblyAI/issues/17), [ADR 0006](https://github.com/talvor/AssemblyAI/blob/main/docs/adr/0006-agents-use-only-the-pinned-skill-bundle.md)).

### Who runs skills

11. **Workers run the skills, in every role.** The leader names the skill in the assignment, the way a user tells an orchestrator "use the wayfinder skill in this repository for ticket #1" ([AssemblyAI#17](https://github.com/talvor/AssemblyAI/issues/17), [01](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/01-roles-and-decisions.md)).
12. **Leaders get an index.** Each leader gets an index of its workers' skills: each skill's name, its purpose, when it applies, and whether it starts only on request (rule 14) ([AssemblyAI#17](https://github.com/talvor/AssemblyAI/issues/17)).
13. **Narrowing.** An assignment may narrow its worker's skill list ([AssemblyAI#17](https://github.com/talvor/AssemblyAI/issues/17), [AssemblyAI#9](https://github.com/talvor/AssemblyAI/issues/9)).
14. **User-invoked skills.** A skill upstream marks as user-invoked (such as wayfinder, to-spec, to-tickets, implement, triage and retro) starts only when the user's request or the job's mandate calls for that kind of outcome. A tested-PR mandate covers to-spec, to-tickets, implement and code-review. Otherwise Coordination proposes the skill to the user as a decision ([AssemblyAI#17](https://github.com/talvor/AssemblyAI/issues/17)).
15. **Questions reach the user through the leader.** A worker's grilling and Wayfinder questions reach the user as decision requests, through its owning leader and Coordination ([AssemblyAI#17](https://github.com/talvor/AssemblyAI/issues/17)).

### Default skill lists

16. **The lists** ([AssemblyAI#17](https://github.com/talvor/AssemblyAI/issues/17), [AssemblyAI#18](https://github.com/talvor/AssemblyAI/issues/18)):

| Role | Leader | Workers |
| --- | --- | --- |
| Coordination | ask-matt (the map of flows it routes by), wait-what (for re-explaining in its own conversation), and the index | setup-matt-pocock-skills |
| Planning | The index | wayfinder, grilling, grill-with-docs, grill-me, domain-modeling, codebase-design, to-spec, to-tickets, triage, to-questionnaire, writing-for-agents |
| Research | The index | research, to-questionnaire |
| Engineering | The index, and pr for composing the pull request | implement, tdd, diagnosing-bugs, prototype, codebase-design, improve-codebase-architecture, pr, wizard, writing-for-agents |
| Quality | The index | code-review, retro, tdd |

17. **Optional skills.** handoff, teach and implement-spec ship but are on no list until the user adds them. The Engineering leader's own instructions cover working through a ticket graph, assigning each ready ticket to a worker with implement and tdd ([AssemblyAI#17](https://github.com/talvor/AssemblyAI/issues/17)).
18. **Short notes bodies.** The Planning and Research leaders write a notes pull request's short body without the pr skill ([AssemblyAI#18](https://github.com/talvor/AssemblyAI/issues/18), [06](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/06-validation-and-delivery.md)).

### Delivery and hiding

19. **Agents see only their list.** Every time AsmAI starts an agent, it hides the user's personal skills, the provider's built-in skills wherever the provider allows, and repository skills unless they are switched on (rule 25). Whatever a pinned provider version cannot hide is listed by `asmai doctor`. Hiding is qualified for each provider version ([AssemblyAI#17](https://github.com/talvor/AssemblyAI/issues/17), [ADR 0006](https://github.com/talvor/AssemblyAI/blob/main/docs/adr/0006-agents-use-only-the-pinned-skill-bundle.md)).
20. **Claude Code** receives its list as a per-session plugin (`--plugin-dir`), and the user setting source is left out ([AssemblyAI#17](https://github.com/talvor/AssemblyAI/issues/17)).
21. **Codex** has no per-session skill directory in 0.157.0, so AsmAI writes the list into `.agents/skills/asmai-<name>/` inside the workspace when it creates it, and the clone's own exclude file keeps them out of git. A leader gets the same inside its own AsmAI directory. A repository's own `.agents/skills` folders are left untouched. AsmAI switches to a native per-session option once a qualified Codex version offers one ([AssemblyAI#17](https://github.com/talvor/AssemblyAI/issues/17), [ADR 0006](https://github.com/talvor/AssemblyAI/blob/main/docs/adr/0006-agents-use-only-the-pinned-skill-bundle.md)).
22. **Names across providers.** Skill delivery must work although Claude Code names plugin skills with a namespace while upstream skills call each other by bare name; this is qualified ([AssemblyAI#17](https://github.com/talvor/AssemblyAI/issues/17), [AssemblyAI#12](https://github.com/talvor/AssemblyAI/issues/12)).

### Added and repository skills

23. **Added skills.** The configuration can add skill directories to any role's leader or worker list. An added skill with the same name as a shipped one replaces it for that role. Added skills are never qualified ([AssemblyAI#17](https://github.com/talvor/AssemblyAI/issues/17), [ADR 0006](https://github.com/talvor/AssemblyAI/blob/main/docs/adr/0006-agents-use-only-the-pinned-skill-bundle.md)).
24. **Copied at start.** Added skills are copied when an agent starts, so editing them never changes a running agent; `asmai config apply` shows which agents pick them up. `asmai doctor` and `asmai status` mark them as the user's and unqualified. Each dispatch records a fingerprint of any added skill ([AssemblyAI#17](https://github.com/talvor/AssemblyAI/issues/17)).
25. **Repository skills** (in a repository's `.claude/skills` or `.agents/skills`) are off by default and hidden. The repository's configuration can switch them on for named roles, for jobs in that repository; they are then marked as the repository's and unqualified, and each dispatch records their fingerprint ([AssemblyAI#17](https://github.com/talvor/AssemblyAI/issues/17)).
26. **No other way in.** Skills reach agents only through the bundle, added skills and switched-on repository skills ([AssemblyAI#17](https://github.com/talvor/AssemblyAI/issues/17)).

### Repository setup

27. **Where the setup lives.** A repository's skill setup lives in the repository: `docs/agents/issue-tracker.md`, `docs/agents/triage-labels.md` and `docs/agents/domain.md`, plus a block in `AGENTS.md` or `CLAUDE.md` ([AssemblyAI#17](https://github.com/talvor/AssemblyAI/issues/17)).
28. **When it runs.** When the user adds a repository with `asmai repo add` and it has no `docs/agents/issue-tracker.md`, Coordination opens a setup job straight away. With that file present, nothing happens; that file alone decides ([AssemblyAI#17](https://github.com/talvor/AssemblyAI/issues/17)).
29. **How it runs.** A Coordination worker runs setup-matt-pocock-skills, and its questions reach the user as decision requests. The files go on that job's branch and pull request ([AssemblyAI#17](https://github.com/talvor/AssemblyAI/issues/17)). Coordination's leader delivers that pull request like a notes-only job: no Quality validation unless the mandate asks for it, the push requested with `asmai push`, and a draft pull request with a short body, marked ready when CI is green ([answers](https://github.com/talvor/AssemblyAI/blob/main/.lavish/spec-doc-08-answers.json)).
30. **Answers apply at once.** The answers are recorded for that repository, so a job that starts before the setup pull request merges receives them as repository instructions ([AssemblyAI#17](https://github.com/talvor/AssemblyAI/issues/17)).
31. **CI.** The setup also asks whether the repository has CI; the declaration lives only in the configuration, and Coordination gives the user the change to make ([AssemblyAI#18](https://github.com/talvor/AssemblyAI/issues/18), [06](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/06-validation-and-delivery.md)).

### Reusing decisions at skills' human steps

32. **Which steps.** Skills' human steps include tdd's and to-spec's test seams, to-tickets' approval of the breakdown, code-review's comparison point and spec, and wizard's stages ([AssemblyAI#17](https://github.com/talvor/AssemblyAI/issues/17)).
33. **Satisfied from the records.** A step is satisfied by a recorded decision of the user's, or a grant, whose scope covers it: the job's decisions in its brief, the repository's setup, or a factory-wide grant ([AssemblyAI#17](https://github.com/talvor/AssemblyAI/issues/17), [01](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/01-roles-and-decisions.md)).
34. **Through the owning leader.** A worker never asks the user directly. It sends a decision request to its owning leader, which answers from the records or escalates through Coordination, and the worker's result names the record it relied on ([AssemblyAI#17](https://github.com/talvor/AssemblyAI/issues/17)).
35. **Uncovered steps** go to the user, and the answer is recorded for the rest of the job ([AssemblyAI#17](https://github.com/talvor/AssemblyAI/issues/17)).
36. **Grilling and Wayfinder** questions always need the user's own answer ([AssemblyAI#17](https://github.com/talvor/AssemblyAI/issues/17), [01](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/01-roles-and-decisions.md)).

### What the instructions must contain

37. **Required content, not wording.** The following lists set what each set of instructions must contain. Each item restates a rule specified elsewhere, cited there. The wording is written during implementation and proved by the proving scenarios ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27)).

**Every agent** (role instructions and the operating guide):

- Coordinate only through `asmai`; fetch the inbox with `asmai inbox` when nudged, and treat only work correlated to the current dispatch as current ([02](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/02-daemon-and-store.md)).
- Load the job's brief at every start and whenever switching jobs ([02](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/02-daemon-and-store.md)).
- Never ask the user directly; ask through a decision request, and never supply the user's side of a decision ([01](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/01-roles-and-decisions.md)).
- Bring a choice between distinct viable approaches to the user; proceed on routine choices and settled routes ([01](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/01-roles-and-decisions.md)).
- Use only the skills on the agent's list, read through the operating guide (rules 6 to 8).
- Follow the repository instructions, which never widen the mandate; escalate a conflict ([05](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/05-repositories-and-job-branches.md)).
- Record each consequential effect with `asmai effect` immediately after making it ([02](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/02-daemon-and-store.md)).
- Never run factory-changing commands; tell the user the command instead ([09](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/09-cli-and-configuration.md)).

**Every leader:**

- Do substantive work only through worker assignments; inspect, reason, converse, accept and keep records itself ([01](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/01-roles-and-decisions.md)).
- Write assignments with an outcome and acceptance criteria, naming the skill from the index, narrowing the list where useful, and declaring side-effect-free work as such ([01](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/01-roles-and-decisions.md), [02](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/02-daemon-and-store.md)).
- Answer handoffs explicitly; accept or reject results against their criteria; never accept on "done" alone ([01](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/01-roles-and-decisions.md)).
- Record delegated decisions with their mandate or grant, rationale, assumptions and reopening conditions, and pass relevant records to workers ([01](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/01-roles-and-decisions.md)).
- Answer workers' decision requests from the records, or escalate through Coordination (rules 33 to 35).
- Reconcile unknown dispatches and assignments that need it, never retrying blindly, and record what is known, what is not and the choice ([02](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/02-daemon-and-store.md)).
- Escalate an assignment that reaches its dispatch limit, with what was tried ([07](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/07-limits-holds-and-visibility.md)).

**Every worker:**

- Carry one assignment for one owning leader, and stay inside the workspace ([01](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/01-roles-and-decisions.md), [05](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/05-repositories-and-job-branches.md)).
- Submit results that link artifacts and evidence, disclose every gap, list the effects made and name the records relied on ([01](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/01-roles-and-decisions.md)).
- In a writing assignment: take in the job branch's tip before submitting; commit and push the assignment branch on a result, a blocked report or a cancellation; keep the commit trailers; put notes where the repository keeps them or under `docs/<kind>/` ([05](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/05-repositories-and-job-branches.md)).
- In a writing assignment that changes code: write tests along with the code, run the repository's checks (through `asmai turn` where the repository's switch is on), name the commands and outcomes, and include a PR section ([06](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/06-validation-and-delivery.md), [05](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/05-repositories-and-job-branches.md)).

**Coordination's leader:**

- Be the user's single counterpart: carry every exchange faithfully and return the user's answers ([01](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/01-roles-and-decisions.md)).
- Open a job from the user's witnessed message with its mandate and acceptance criteria, and link follow-ups ([01](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/01-roles-and-decisions.md)).
- Keep one focused job; tag every line about a job with its number; give one line per automated item and a flagged block for anything that needs the user; say when the focus moves and load that job's brief ([04](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/04-conversation-and-lavish.md)).
- Present each decision once, with its answer surface; record conversation answers and grants with its reading beside the user's witnessed message ([01](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/01-roles-and-decisions.md), [04](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/04-conversation-and-lavish.md)).
- Give Lavish links with the forwarding command, and confirm collected Lavish answers in one line ([04](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/04-conversation-and-lavish.md)).
- Route work by handing it to roles, never managing processes; propose a user-invoked skill the request does not call for ([02](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/02-daemon-and-store.md), rule 14).
- Own unresolved cross-role trade-offs, and never mark a failed validation as passed ([01](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/01-roles-and-decisions.md)).
- Report each delivery step, changed plans, effects that cannot be undone, and the link when a job ends ([02](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/02-daemon-and-store.md), [06](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/06-validation-and-delivery.md)).
- Pause, resume or cancel a job only on the user's word, citing it ([07](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/07-limits-holds-and-visibility.md)).
- After an interrupted automated turn, re-read the same messages and check its own recorded calls before acting again; narrate the catch-up only when asked ([04](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/04-conversation-and-lavish.md)).
- Run repository setup for a newly added repository and deliver its pull request, and give the user the commands and configuration changes only the user may make ([05](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/05-repositories-and-job-branches.md), rules 27 to 31).

**Planning's and Research's leaders:**

- Assign grilling, Wayfinder, specification and research work to workers with the right skill, and carry their questions to the user as decision requests (rules 11, 15).
- Deliver their own notes-only jobs, with a short "notes only" body ([06](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/06-validation-and-delivery.md)).
- Research's findings tie every claim to a cited source and never stand in for the user's answers ([01](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/01-roles-and-decisions.md), [AssemblyAI#12](https://github.com/talvor/AssemblyAI/issues/12)).

**Engineering's leader:**

- Work through a ticket graph, assigning each ready ticket to a worker with implement and tdd (rule 17).
- Own the delivery of a code job: decide when the job branch is ready, hand validation to Quality, receive the findings, assign fixes, ask for the push with `asmai push`, open and update the pull request with gh and record each as an effect, compose the body from the workers' PR sections, Quality's report and CI, judge the merge danger, handle red CI with at most one judged re-run, and escalate at the failed-validation limit ([06](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/06-validation-and-delivery.md)).

**Quality's leader:**

- Assign validation as a read-only assignment at the exact head commit, with the job's mandate and acceptance criteria; report findings as blocking, advisory or needs-you; reconcile disputed findings with Engineering, and take what remains to the user ([06](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/06-validation-and-delivery.md)).

38. **The PR section in a writing worker's result** contains, in the pr skill's form, what changed and the before-and-after evidence for the worker's own part. A worker that merged the base in or resolved conflicts writes a section for those changes too ([AssemblyAI#18](https://github.com/talvor/AssemblyAI/issues/18)).
39. **A leader's skill index** contains, for each of its workers' skills, the name, purpose, when it applies, and whether it starts only on request (rule 12).

## Interfaces

### Commands

| Who | Command | Purpose |
| --- | --- | --- |
| The user | `asmai doctor` | Newer upstream skill releases, what changed after an upgrade, what a provider cannot hide, and added and repository skills marked unqualified (rules 4, 5, 19, 24) |
| The user | `asmai config apply` | Shows which agents pick up added skills (rule 24) |
| The user | `asmai repo add` | Starts repository setup where it is missing (rule 28) |
| Leaders | `asmai assign` | Names the skill and may narrow the list (rules 11, 13) |

### Store records

| Record | Holds |
| --- | --- |
| Dispatch | The bundle version, and fingerprints of added and repository skills ([02](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/02-daemon-and-store.md)) |
| Repository setup answers | The user's answers for a repository, used as repository instructions until the setup pull request merges (rule 30) |

### Files

- **The bundle, the operating guide and the patch list**, embedded in the executable (rules 1, 6, 10).
- **Claude Code's per-session plugin** directory (rule 20).
- **Codex's skill folders**, `.agents/skills/asmai-<name>/` in each workspace and each leader's AsmAI directory, kept out of git by the clone's exclude file (rule 21).
- **Repository setup files**: `docs/agents/issue-tracker.md`, `triage-labels.md`, `domain.md` and the block in `AGENTS.md` or `CLAUDE.md` (rule 27).

## Settings and defaults

[09](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/09-cli-and-configuration.md) names the fields.

| Setting | Scope | Default | Rule |
| --- | --- | --- | --- |
| Skill list of each role's leader and workers | Per role | The lists in rule 16 | 16 |
| Added skill directories | Per role, for the leader or the workers | None | 23 |
| Repository skills switched on | Per repository, for named roles | None | 25 |

## Failure handling

| Failure | Handling |
| --- | --- |
| A provider version cannot hide some skills | `asmai doctor` lists them, and the guide tells agents to use only their list (rules 8, 19) |
| A skill's phrasing does not fit the factory | The operating guide maps it; a patch only where the guide cannot work (rules 7, 10) |
| A skill's human step is not covered by the records | It goes to the user, and the answer is recorded for the rest of the job (rule 35) |
| An added skill is edited while agents run | Running agents keep their copy; the next start picks it up (rule 24) |

## Qualification cases and proving scenarios

- **C33**: personal, provider built-in and repository skills are hidden, including Claude's built-in code-review next to the shipped one (rule 19).
- **C34**: per-session skill delivery works although Claude namespaces plugin skills and upstream skills call each other by bare name (rules 20, 22).
- **C35**: Codex finds the skills written into its workspace (rule 21).
- **S1** to **S9**: the proving scenarios prove the instructions' wording, the operating guide and the skill lists in real jobs; S1 and S3 exercise grilling and Wayfinder questions reaching the user in Lavish.

## Sources

- [Map Matt Pocock skills to factory roles](https://github.com/talvor/AssemblyAI/issues/3#issuecomment-5968136435) (AssemblyAI#3), research behind the lists
- [Define roles and leader-worker contracts](https://github.com/talvor/AssemblyAI/issues/5#issuecomment-5968317664) (AssemblyAI#5)
- [Explore terminal conversation and Lavish decision flow](https://github.com/talvor/AssemblyAI/issues/10#issuecomment-5989237516) (AssemblyAI#10)
- [Define v1 acceptance scenarios and evidence](https://github.com/talvor/AssemblyAI/issues/12#issuecomment-5993314453) (AssemblyAI#12)
- [Choose skill bundles and update policy](https://github.com/talvor/AssemblyAI/issues/17#issuecomment-5992055697) (AssemblyAI#17), with its [answers](https://github.com/talvor/AssemblyAI/blob/main/.lavish/skills-answers.json)
- [Choose validation and delivery ownership](https://github.com/talvor/AssemblyAI/issues/18#issuecomment-5992792804) (AssemblyAI#18)
- [Choose the specification's structure and implementation sequence](https://github.com/talvor/AssemblyAI/issues/27#issuecomment-6004852593) (AssemblyAI#27)
- [ADR 0006](https://github.com/talvor/AssemblyAI/blob/main/docs/adr/0006-agents-use-only-the-pinned-skill-bundle.md) and the [glossary](https://github.com/talvor/AssemblyAI/blob/main/GLOSSARY.md): Skill, Skill bundle, Skill list, Added skill, Repository skill.
- The review of this document: [questions](https://github.com/talvor/AssemblyAI/blob/main/.lavish/spec-doc-08-round1-questions.json) and [answers](https://github.com/talvor/AssemblyAI/blob/main/.lavish/spec-doc-08-answers.json).
