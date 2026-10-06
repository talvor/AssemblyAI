# 00 Overview

AsmAI is a personal software engineering factory: one user-facing agent, role leaders and workers, running unmodified Claude Code and Codex CLIs under a per-user daemon, delivering tested pull requests and standalone engineering work across several repositories. This document is the entry point to the v1 specification. It states the problem, the solution, the user stories, what v1 covers and leaves out, how the specification and the code are organized, the order v1 is built in, and where every decision, qualification case and proving scenario is specified.

Every rule cites the decision ticket or ADR it comes from. Words in **bold** that name a factory concept are defined in the [glossary](https://github.com/talvor/AssemblyAI/blob/main/GLOSSARY.md), which this specification cites and does not copy.

## Problem statement

The user develops software by driving coding agents (Claude Code and Codex) through working methods such as wayfinder, grilling, implement and code-review. Each agent session is tied to one terminal and one task. The user starts it, watches it, answers its questions, carries its results to the next step and, for a feature, to a pull request. While the user is away, nothing moves. A disconnect, a crash or a reboot loses track of what was running and what it already did. Work in several repositories at once means several sessions to supervise by hand, each with its own context and no shared record of decisions.

The user wants one counterpart to talk to, which takes a requested outcome and drives it to a reviewable result while other work continues. Agents should make the routine decisions themselves but bring every real choice to the user, and never act in the user's name without the user's own words. The output should be a pull request the user can trust: tested, validated by someone other than its author, with its evidence and gaps stated, and never merged without the user. It must work on the user's own subscriptions, on local and remote hosts, without handing over provider credentials or switching to API billing ([AssemblyAI#1](https://github.com/talvor/AssemblyAI/issues/1), [AssemblyAI#15](https://github.com/talvor/AssemblyAI/issues/15)).

## Solution

AsmAI is one Go executable, `asmai`, that runs a factory on the user's host ([ADR 0003](https://github.com/talvor/AssemblyAI/blob/main/docs/adr/0003-go-executable-runs-pinned-providers.md)):

- **Roles.** Five factory-wide roles: Coordination, Planning, Research, Engineering and Quality. Each has exactly one leader serving every job and repository, and workers that each carry one bounded assignment for their owning leader. Coordination is the user's single counterpart ([AssemblyAI#5](https://github.com/talvor/AssemblyAI/issues/5)).
- **The conversation.** The user talks to Coordination in its interactive terminal, with a status line from the daemon showing what is waiting on the user. Reviews and all grilling and Wayfinder questions go to Lavish pages ([AssemblyAI#10](https://github.com/talvor/AssemblyAI/issues/10), [ADR 0004](https://github.com/talvor/AssemblyAI/blob/main/docs/adr/0004-attach-client-draws-status-line.md)).
- **Authority.** A job's mandate authorizes the ordinary work its outcome needs. Whenever more than one distinct viable approach remains, the user chooses. Only the user's witnessed messages and Lavish answers count as the user's decisions ([AssemblyAI#6](https://github.com/talvor/AssemblyAI/issues/6), [AssemblyAI#10](https://github.com/talvor/AssemblyAI/issues/10)).
- **The daemon.** A per-user daemon owns every agent terminal, the input fence, hook intake, the Lavish server and the store. Agents coordinate by running `asmai` commands against it ([ADR 0001](https://github.com/talvor/AssemblyAI/blob/main/docs/adr/0001-daemon-owns-agent-terminals.md), [ADR 0002](https://github.com/talvor/AssemblyAI/blob/main/docs/adr/0002-agents-coordinate-through-asmai-cli.md)).
- **Providers.** Agents run AsmAI's own pinned, qualified copies of Claude Code, Codex and Lavish, with settings passed per session, on the user's existing subscription sign-in ([ADR 0003](https://github.com/talvor/AssemblyAI/blob/main/docs/adr/0003-go-executable-runs-pinned-providers.md), [AssemblyAI#15](https://github.com/talvor/AssemblyAI/issues/15)).
- **Repositories.** Jobs work in AsmAI's own clone of each registered repository, one workspace per assignment, and the daemon fast-forwards each job's one job branch when a leader accepts a result ([ADR 0005](https://github.com/talvor/AssemblyAI/blob/main/docs/adr/0005-jobs-work-in-an-asmai-owned-clone.md)).
- **Delivery.** Engineering tests its own work, Quality validates the finished job branch at its exact head, the daemon pushes and watches CI, the Engineering leader opens the pull request, and the user merges ([ADR 0007](https://github.com/talvor/AssemblyAI/blob/main/docs/adr/0007-asmai-delivers-tested-prs-with-its-own-roles.md)).
- **Skills.** Agents use only the skill bundle pinned in the release, with an operating guide that maps the skills onto the factory ([ADR 0006](https://github.com/talvor/AssemblyAI/blob/main/docs/adr/0006-agents-use-only-the-pinned-skill-bundle.md)).
- **Releases.** A release is the qualified commit plus its qualification record. Qualification runs the real pinned providers on real hosts, and nine proving scenarios on real repositories gate the launch ([ADR 0008](https://github.com/talvor/AssemblyAI/blob/main/docs/adr/0008-qualification-runs-real-provider-clis-on-real-hosts.md), [ADR 0009](https://github.com/talvor/AssemblyAI/blob/main/docs/adr/0009-a-release-is-the-qualified-commit-plus-its-record.md), [AssemblyAI#12](https://github.com/talvor/AssemblyAI/issues/12)).

## User stories

The stories are grouped by the component document that specifies them.

### Installing and setting up ([09](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/09-cli-and-configuration.md), [10](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/10-release-install-and-upgrade.md))

1. As the user, I want to install AsmAI with one `curl … | sh` command that fetches a release from GitHub Releases into `~/.local/bin` without root, so that I can set it up on any host I use.
2. As the user, I want the install script to check the archive's SHA-256 and, when gh is signed in, its artifact attestation, failing closed, so that I know I run the executable the release built.
3. As the user, I want the install script to refuse a platform the release does not certify and name the ones it does, so that I never install something that cannot start agents.
4. As the user, I want the install script to leave my shell files alone and print the PATH line to add, so that nothing on my host changes without me.
5. As the user, I want `asmai init` to walk me through platform certification, Node, pinned providers, sign-in, Codex hook trust, role staffing and the service, so that a new host is ready in one sitting.
6. As the user, I want `asmai init` to take flags for a non-interactive setup, so that I can set up a remote host from a script.
7. As the user, I want `asmai providers install` to fetch AsmAI's pinned Claude Code, Codex and Lavish from their official channels after I confirm, so that my personal copies keep updating without pausing the factory.
8. As the user, I want the pinned CLIs to use my existing subscription sign-in, and AsmAI never to start a login, handle my tokens or fall back to API billing, so that my accounts stay mine.
9. As the user, I want AsmAI to print the native sign-in command when a provider is not signed in or uses an API key, so that I know exactly what to run.
10. As the user, I want every agent session to start without provider API-key variables, so that a stray key cannot move an agent onto API billing.
11. As the user, I want AsmAI never to write `~/.claude` or `~/.codex`, so that my personal provider tools are unchanged.
12. As the user, I want `asmai doctor` to re-run every setup check without changing anything, so that I can diagnose a host safely.
13. As the user, I want `asmai doctor` to show the qualification record, the known limitations, what a pinned provider cannot hide from agents, and any newer release with its kind, so that I know what my factory relies on.
14. As the user, I want one TOML configuration file that commands edit and that I can also edit by hand, so that my whole factory setup is in one place.
15. As the user, I want `asmai config apply` to validate the file, show the change and the running agents it affects, and ask before applying, so that I never change a running factory by accident.
16. As the user, I want to register each repository explicitly with `asmai repo add`, so that jobs only ever target repositories I chose.
17. As the user, I want Coordination to set up a newly added repository's skill files in a setup job when it lacks them, asking me its questions as decisions, so that the skills work there without manual preparation.
18. As the user, I want to choose the provider and model of each role's leader and the default for its workers, so that I can staff roles across both subscriptions.
19. As the user, I want to keep per-repository notes in the configuration that agents treat as repository instructions, so that I can steer how work is done in a repository without editing it.
20. As the user, I want to declare per repository that it has no CI, that its checks cannot run side by side, or that its commits must not carry trailers, so that AsmAI fits each repository's conventions.
21. As the user, I want to add my own skill directories to a role's skill list, replacing a shipped skill of the same name if I choose, so that I can use my own working methods, clearly marked as mine and unqualified.
22. As the user, I want a repository's own skills to stay hidden unless I switch them on for named roles, so that a repository cannot change how agents work without my say.

### Running the factory ([02](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/02-daemon-and-store.md), [09](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/09-cli-and-configuration.md))

23. As the user, I want a bare `asmai` to open Coordination's conversation, starting a stopped factory first and saying so, so that one word gets me to work.
24. As the user, I want `asmai start` to refuse an uncertified platform, an unqualified provider combination or a store it cannot use, naming the failing step and the fix, so that the factory never runs on something untested.
25. As the user, I want `asmai service install` to register a systemd user unit (with linger) or a launchd LaunchAgent, so that my factory comes back after a reboot.
26. As the user, I want `asmai stop` to dispatch nothing new, let running turns reach a boundary for up to 10 minutes, then interrupt the rest, and `asmai stop --now` to skip the wait, so that stopping never loses work.
27. As the user, I want pending decisions, grants and queued requests to survive a stop, so that nothing I said is forgotten.
28. As the user, I want `asmai status` to show the daemon and its version, each leader, workers against each provider's cap, queued assignments, provider allowance and state, the Lavish server, paused jobs, holds and disk use, so that I can see the factory's health at a glance.
29. As the user, I want `asmai status --check` to exit non-zero when anything needs me, so that I can wire it into my own monitoring.
30. As the user, I want to run any `asmai` command against a remote host with `--host <ssh-destination>`, with the remote Lavish port forwarded for the conversation and attach, so that a remote factory feels local.
31. As the user, I want plain `ssh -t host asmai` to work too, so that I need nothing special on the machine I connect from.
32. As the user, I want to look around with `asmai jobs`, `job <n>`, `agents`, `decisions`, `lavish`, `journal` and `log`, so that I can inspect anything without attaching to an agent.
33. As the user, I want `asmai export` and `asmai backup <file>` to give me the journal and a consistent copy of the store while the factory runs, so that I can keep my own records.

### The conversation ([04](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/04-conversation-and-lavish.md))

34. As the user, I want to talk to Coordination in its interactive terminal, so that I direct the whole factory in plain language.
35. As the user, I want a status line in every attached terminal showing what is waiting on me, the focused job, the running jobs and any agent whose input I hold, so that nothing waiting on me is hidden by the conversation.
36. As the user, I want each automated item to appear as one line tagged with its job number, and anything that needs me as a flagged block, so that I can follow several jobs without noise.
37. As the user, I want my messages to apply to the focused job unless I name another (`14: …`), and "switch to 14" to move the focus, so that I can talk about several jobs without confusion.
38. As the user, I want a new request to open a job with its mandate and acceptance criteria, so that every piece of work has a clear outcome.
39. As the user, I want Coordination to keep delivering while I talk, and never to wait on whether I am present, so that work moves while I am away.
40. As the user, I want a catch-up when I return, covering what is waiting on me, jobs that finished, failed or paused, agents waiting in their own terminal, input I still hold and my saved unsent text, so that I pick up where I left off.
41. As the user, I want my unsent text saved when I leave and offered back on return, never retyped, so that leaving never loses or replays what I was writing.
42. As the user, I want a newer terminal to take over the conversation while the older one only observes, so that two terminals never type into one agent.
43. As the user, I want my keys, including Esc, always to reach the conversation, with an interrupted automated turn checked rather than repeated, so that I can always cut in safely.

### Decisions and authority ([01](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/01-roles-and-decisions.md), [04](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/04-conversation-and-lavish.md))

44. As the user, I want to be asked whenever more than one distinct viable approach remains, with the leader's recommendation, so that real choices stay mine.
45. As the user, I want leaders to make routine choices within the mandate themselves and record them as agent-made, so that I am not asked about things that do not matter.
46. As the user, I want single-choice decisions answered in the conversation and reviews, grilling, Wayfinder and multi-question requests answered in Lavish, with each decision version answerable in exactly one place, so that two answers never race.
47. As the user, I want only my witnessed messages and Lavish answers to count as my words, so that no agent can put a decision in my mouth.
48. As the user, I want a reply to an older version of a decision to be refused and the current version shown again, so that I never approve something that changed.
49. As the user, I want independent work to continue while a decision is pending, and silence never to count as approval, so that waiting on me costs as little as possible.
50. As the user, I want to grant authority at job, repository or factory scope, list grants with `asmai grants` and revoke one with `asmai grant revoke`, so that I can stop being asked the same thing.
51. As the user, I want a skill's human steps (test seams, ticket approval, review comparison points) satisfied by my recorded decisions and grants where they apply, so that each job does not re-ask what I already decided.
52. As the user, I want grilling and Wayfinder questions always to need my own answer, so that those exchanges stay genuinely mine.
53. As the user, I want Lavish pages to show structured questions with recommendations, plus whatever the agent attached, and the daemon to collect my answers word for word, so that I can answer carefully and have it recorded exactly.
54. As the user, I want Coordination to give me the Lavish URL and the SSH forwarding command, so that I can reach Lavish on a remote host.
55. As the user, I want any action that would spend money to need my grant naming the amount and scope, so that the factory never spends without me.

### Stepping into agents ([03](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/03-provider-sessions-and-terminals.md))

56. As the user, I want to attach to any agent with `asmai attach <agent>` and observe by default, so that I can watch work without disturbing it.
57. As the user, I want to take an agent's input explicitly, waiting for its turn's boundary or interrupting, with any unsent automated draft recorded and cleared, so that my typing and automation never compete.
58. As the user, I want to answer native permission prompts in the agent's terminal with the decision recorded, so that provider safety prompts stay in my hands.
59. As the user, I want release to be explicit, and detaching without releasing to keep the agent paused, so that an agent never resumes behind my back.
60. As the user, I want a Ctrl-] menu that moves this terminal between the conversation and every agent, those waiting on me first, so that I can step in without opening another terminal.
61. As the user, I want what I typed during an intervention to reach the owning leader as an intervention record, followed by a new dispatch, so that my corrections are applied by the agent that owns the work.
62. As the user, I want every agent terminal recorded per dispatch and replayable with `asmai replay`, so that I can see what an agent actually did.
63. As the user, I want any unknown input state, such as a provider modal, to hold that agent and reach me through Coordination instead of being typed over, so that automation never answers something it does not understand.

### Work in repositories ([05](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/05-repositories-and-job-branches.md), [02](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/02-daemon-and-store.md))

64. As the user, I want jobs to work in AsmAI's own clone of my repository, never my checkout, so that my local state never leaks into jobs and factory branches never appear in my working copy.
65. As the user, I want each job's accepted work on one job branch that becomes its pull request, so that each outcome has one place to review.
66. As the user, I want every writing assignment to work on its own assignment branch, pushed to origin and kept until I delete it, so that no work, including prototypes, is ever lost.
67. As the user, I want the job branch to move only when a leader accepts a result, by fast-forward, so that only accepted work reaches it.
68. As the user, I want concurrent jobs in one repository to run without locks, with conflicts resolved by a worker in whichever job meets them, so that independent work is never serialized.
69. As the user, I want commits that someone else pushed to a job branch to be merged in and reported, never force-pushed over, so that my own changes are always kept.
70. As the user, I want agents to use my git identity and credentials and to mark every commit with job, agent and dispatch trailers, so that every commit is traceable to the work that made it.
71. As the user, I want agents to follow a repository's `AGENTS.md` and `CLAUDE.md` but not load its provider configuration, so that a repository cannot change provider hooks, permissions or MCP servers for my agents.
72. As the user, I want notes that the tracker does not already hold committed to the job branch, so that research findings and diagnosis logs are kept with the work.
73. As the user, I want a follow-up to a job whose PR is still open to continue on that job branch and PR, so that review comments land where I expect.
74. As the user, I want jobs without a repository to work in scratch workspaces that are kept until I remove them, so that standalone research and diagnosis have somewhere to live.

### Delivery ([06](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/06-validation-and-delivery.md))

75. As the user, I want a job that changes code to end in a tested pull request: every writing assignment accepted, the latest base taken in, Quality's validation at that exact head, green CI on that head, and the evidence and gaps stated, so that I can trust what I review.
76. As the user, I want Engineering to test its own work and Quality to validate independently without fixing anything, so that the author never marks its own work.
77. As the user, I want Quality's findings sorted into blocking, advisory and needs-you, with needs-you findings brought to me word for word, so that only real problems block and challenges to my intent reach me.
78. As the user, I want the PR opened as a draft and marked ready only when CI is green on its head, so that "ready" always means tested.
79. As the user, I want the PR body to follow the repository's template and add an AsmAI section with the job, its mandate, the head Quality passed, the checks, CI, advisory findings and gaps, so that the evidence is where I review.
80. As the user, I want AsmAI never to merge in v1, so that every merge is my own act.
81. As the user, I want a repository with no CI to be declared as such, and otherwise AsmAI to wait up to 15 minutes for a first check and then hold and ask me, so that an empty check list is never taken as green.
82. As the user, I want a job's delivery to hold and come to me after 3 failed validations, so that a job that keeps failing does not loop forever.
83. As the user, I want Coordination to report the PR link when a job is delivered and the job to end there, so that I know when something is ready.

### Limits and visibility ([07](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/07-limits-holds-and-visibility.md))

84. As the user, I want a cap on workers in progress per provider (3 for Claude and 3 for Codex by default), with further assignments queued first come first served, so that the factory paces my subscription allowance.
85. As the user, I want each provider's allowance used and reset times in `asmai status`, so that I can see how much the factory is using.
86. As the user, I want agents to hold when a provider's allowance runs out and resume at the reset, so that the factory recovers without me.
87. As the user, I want provider errors resumed with backoff, a provider that stays down marked unavailable, and work resumed when it answers, so that outages need no action from me.
88. As the user, I want a lost or expired sign-in to hold work and show the native sign-in command, resuming once I sign in again, so that I fix access in one step.
89. As the user, I want to pause, resume and cancel a job with `asmai job pause|resume|cancel` or by telling Coordination, so that I control what runs.
90. As the user, I want an assignment that reaches 5 dispatches without acceptance to hold and come to me with what was tried, so that stuck work does not burn allowance.
91. As the user, I want no new workspace created below 5 GB of free space, and `asmai job clean` to remove kept workspaces, so that the factory never fills my disk.
92. As the user, I want the daemon's log rotated and readable with `asmai log`, and recordings deleted 14 days after their job ends, so that logs never grow without bound.
93. As the user, I want holds and events shown in the status line, the catch-up and `asmai status`, so that I see what happened without notifications.

### Recovery ([02](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/02-daemon-and-store.md))

94. As the user, I want my factory to recover with work intact from a terminal or SSH disconnect, an agent crash, a daemon crash and a host reboot, so that I can leave it running unattended.
95. As the user, I want a crashed leader restarted on the same provider, and its role held after repeated failures, so that one bad session does not stop the factory.
96. As the user, I want a crashed worker's assignment reconciled by its owning leader, never blindly retried, so that no side effect is repeated.
97. As the user, I want agent processes left by a crashed daemon terminated at the next start, so that no stale agent keeps writing.

### Upgrading ([10](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/10-release-install-and-upgrade.md))

98. As the user, I want to upgrade by stopping, rerunning the install script and starting, so that upgrades are deliberate and simple.
99. As the user, I want a running factory to keep its version until I restart it, with the status line saying a newer version is installed, so that an upgrade never changes agents mid-job.
100. As the user, I want `asmai start` after an upgrade to list the newly pinned providers and offer to install them, so that provider pins move only when I agree.
101. As the user, I want my configuration never rewritten by an upgrade, and renamed settings to keep working with a warning, so that my setup stays mine.
102. As the user, I want the store migrated forward after a checked backup, and a store AsmAI cannot use refused and explained rather than repaired or deleted, so that an upgrade can never destroy my factory's record.
103. As the user, I want `asmai restore <file>` to put a backup back while setting the current store aside, so that I can always go back.
104. As the user, I want `asmai notices` to print AsmAI's license and third-party notices, so that I know what the executable contains.

### Agents ([01](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/01-roles-and-decisions.md), [02](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/02-daemon-and-store.md), [08](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/08-skills-and-agent-instructions.md))

105. As a leader, I want a store-generated brief for each job, so that I load the same context at every start and job switch.
106. As a leader, I want to hand work to another role's leader with the context and acceptance criteria it needs, and to accept, clarify or decline handoffs, so that cross-role work has one owner at a time.
107. As a leader, I want an index of my workers' skills, so that I can name the right skill in each assignment.
108. As a worker, I want work delivered to my inbox with a one-line nudge, so that the terminal never carries the content of my work.
109. As a worker, I want to record each consequential effect with `asmai effect` as I make it, so that my leader can reconcile what happened if anything fails.
110. As a worker, I want a decision request to go to my owning leader first, who answers from the records or escalates, so that the user is asked only when the records do not cover it.

### Maintaining AsmAI ([10](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/10-release-install-and-upgrade.md), [11](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/11-qualification-and-proving.md))

111. As the maintainer, I want development tests in hosted CI on Linux and macOS for every PR, using a scripted fake provider, so that the daemon is tested on every change without a provider sign-in.
112. As the maintainer, I want a qualification harness that drives the real pinned providers on a real host under a separate OS user, injecting faults, so that a release certifies only what was actually tested.
113. As the maintainer, I want a release built from the qualified commit plus its qualification record, with the workflow checking that the record is the only change, so that the shipped code is the qualified code.
114. As the maintainer, I want releases built reproducibly in GitHub Actions without a C compiler, with checksums and an attestation for every file, so that anyone can verify them.
115. As the maintainer, I want the build to fail on a compiled-in module whose license is not on the allow-list, so that no license surprises ship.
116. As the maintainer, I want release candidates published as prereleases that the install script skips unless asked, so that the proving scenarios run on a release before it is offered.
117. As the maintainer, I want each proving scenario's evidence checklist and verdict recorded beside the releases, so that the launch decision is backed by evidence.

## Scope

v1 covers:

- **One factory per user per host**, installed without root, on local and remote hosts reached over SSH. Factories on different hosts share nothing ([AssemblyAI#7](https://github.com/talvor/AssemblyAI/issues/7)).
- **Linux and macOS**, held to one qualification bar and certified per platform. Linux x86_64 is certified first and launches v1; macOS on Apple silicon follows in a later release. Windows is supported only as Linux under WSL and is not separately targeted ([AssemblyAI#7](https://github.com/talvor/AssemblyAI/issues/7), [AssemblyAI#12](https://github.com/talvor/AssemblyAI/issues/12), [AssemblyAI#20](https://github.com/talvor/AssemblyAI/issues/20)).
- **Claude Code and Codex at launch**, with mixed staffing, on the user's own subscription sign-in only ([AssemblyAI#15](https://github.com/talvor/AssemblyAI/issues/15)).
- **Five roles**, Coordination, Planning, Research, Engineering and Quality, with one leader each ([AssemblyAI#5](https://github.com/talvor/AssemblyAI/issues/5)).
- **The kinds of job the proving scenarios name**: a feature delivered as a tested pull request, and standalone research, planning and diagnosis, each against one registered repository or none ([AssemblyAI#12](https://github.com/talvor/AssemblyAI/issues/12), [AssemblyAI#18](https://github.com/talvor/AssemblyAI/issues/18)).
- **Concurrent independent jobs** across registered repositories, including several in one repository ([AssemblyAI#11](https://github.com/talvor/AssemblyAI/issues/11), [AssemblyAI#14](https://github.com/talvor/AssemblyAI/issues/14)).
- **Recovery** with work intact from a terminal or SSH disconnect, an agent crash, a daemon crash and a host reboot ([AssemblyAI#7](https://github.com/talvor/AssemblyAI/issues/7)).
- **Releases** under Apache-2.0, installed only by the install script from GitHub Releases ([AssemblyAI#20](https://github.com/talvor/AssemblyAI/issues/20)).

## Out of scope

- **Merging.** AsmAI never merges in v1, and no grant can authorize a merge ([AssemblyAI#18](https://github.com/talvor/AssemblyAI/issues/18)).
- **Automatic production deployment** as a deliverable; the delivery target is a tested pull request ([AssemblyAI#1](https://github.com/talvor/AssemblyAI/issues/1)).
- **Coordinated features spanning several repositories**; v1 runs concurrent independent jobs, each against at most one repository ([AssemblyAI#1](https://github.com/talvor/AssemblyAI/issues/1), [AssemblyAI#8](https://github.com/talvor/AssemblyAI/issues/8)).
- **A hosted service, commercial distribution, resale of provider access, AsmAI-managed sign-in and API billing** ([AssemblyAI#15](https://github.com/talvor/AssemblyAI/issues/15)).
- **Notifications while the user is away and a browser dashboard.** Both are v2 candidates; the notification design to start from is kept in [AssemblyAI#14](https://github.com/talvor/AssemblyAI/issues/14).
- **no-mistakes as a delivery pipeline.** It is a v2 candidate, and the conflicts a v2 design must resolve are kept in [AssemblyAI#18](https://github.com/talvor/AssemblyAI/issues/18) ([ADR 0007](https://github.com/talvor/AssemblyAI/blob/main/docs/adr/0007-asmai-delivers-tested-prs-with-its-own-roles.md)).
- **Homebrew, package registries (npm, crates.io) and Apple Developer ID signing.** No package names are claimed ([AssemblyAI#20](https://github.com/talvor/AssemblyAI/issues/20)).
- **Platforms not certified:** Linux arm64 and Intel macOS are not built ([AssemblyAI#20](https://github.com/talvor/AssemblyAI/issues/20)).
- **A factory spanning hosts, a registry of hosts or a combined view across hosts** ([AssemblyAI#7](https://github.com/talvor/AssemblyAI/issues/7), [AssemblyAI#9](https://github.com/talvor/AssemblyAI/issues/9)).
- **Losing the host or migrating a factory to another host.** The user is responsible for backing up the state directory ([AssemblyAI#7](https://github.com/talvor/AssemblyAI/issues/7)).
- **Standby leaders** ([AssemblyAI#7](https://github.com/talvor/AssemblyAI/issues/7)).
- **Hot upgrades and self-update** ([AssemblyAI#7](https://github.com/talvor/AssemblyAI/issues/7), [AssemblyAI#9](https://github.com/talvor/AssemblyAI/issues/9)).
- **An MCP server for agents** ([ADR 0002](https://github.com/talvor/AssemblyAI/blob/main/docs/adr/0002-agents-coordinate-through-asmai-cli.md)).
- **tmux as the host of agent terminals**; an attach client may still run inside tmux ([ADR 0001](https://github.com/talvor/AssemblyAI/blob/main/docs/adr/0001-daemon-owns-agent-terminals.md)).
- **Compatibility with Firstmate or OpenRig** commands, configuration, agents or task history, and migration from either. Both are design references only, and copying a component from either needs its own decision ([AssemblyAI#16](https://github.com/talvor/AssemblyAI/issues/16)).
- **Exactly-once side effects and portable conversations across providers**; effects are reconciled instead ([AssemblyAI#15](https://github.com/talvor/AssemblyAI/issues/15), [AssemblyAI#19](https://github.com/talvor/AssemblyAI/issues/19)).
- **Per-job token budgets, a reserve of allowance for the user's own use, per-job disk quotas, and CPU or memory limits** ([AssemblyAI#14](https://github.com/talvor/AssemblyAI/issues/14)).
- **A security boundary against processes running as the user.** The agent command guard, witnessed messages and provider write guards prevent mistakes; they do not stop a hostile process with the user's access ([AssemblyAI#9](https://github.com/talvor/AssemblyAI/issues/9), [AssemblyAI#10](https://github.com/talvor/AssemblyAI/issues/10), [AssemblyAI#11](https://github.com/talvor/AssemblyAI/issues/11)).
- **Watching a pull request after its job ends.** Later changes are follow-up jobs the user asks for ([AssemblyAI#18](https://github.com/talvor/AssemblyAI/issues/18)).
- **An `asmai qualify` command, and qualification in hosted CI** ([AssemblyAI#12](https://github.com/talvor/AssemblyAI/issues/12)).

## Vocabulary

The [glossary](https://github.com/talvor/AssemblyAI/blob/main/GLOSSARY.md) defines the factory's language, and every document uses its terms and avoids the synonyms it lists. Its terms by area:

**The user** is whoever runs the factory, and the rules say "the user". "Phillip" appears only where a decision is about Phillip personally: as the maintainer, in building talvor/asmai, for the Mac and the fixture repository he owns, and for his verdicts in the proving scenarios. "The maintainer" is the person who qualifies and tags releases ([answers](https://github.com/talvor/AssemblyAI/blob/main/.lavish/spec-doc-00-answers.json)).

| Area | Terms |
| --- | --- |
| The product | AsmAI, Factory, Host, Release, Upgrade |
| Roles | Role, Leader, Worker, Coordination, Planning, Research, Engineering, Quality |
| Work | Job, Assignment, Handoff, Dispatch, Reconciliation, Store, Hold |
| Authority | Mandate, Grant, Viable approach, Delegated decision, Escalation |
| Conversation | Conversation, Focused job, Witnessed message, Answer surface, Catch-up, Intervention |
| Repositories | Registered repository, Repository instructions, Job branch, Assignment branch, Workspace |
| Delivery | Validation, Finding, Tested pull request |
| Limits | Allowance |
| Skills | Skill, Skill bundle, Skill list, Added skill, Repository skill |
| Qualification | Qualification, Certified platform, Qualification record, Known limitation, Proving scenario, Proving ground |

## Architecture decisions

The ADRs record the decisions that are hard to reverse. The specification cites them, and each document follows the ones in its area:

| ADR | Decision | Documents |
| --- | --- | --- |
| [0001](https://github.com/talvor/AssemblyAI/blob/main/docs/adr/0001-daemon-owns-agent-terminals.md) | A per-user AsmAI daemon owns agent terminals; tmux is not the supervisor | 02, 03 |
| [0002](https://github.com/talvor/AssemblyAI/blob/main/docs/adr/0002-agents-coordinate-through-asmai-cli.md) | Agents coordinate through the `asmai` CLI over a daemon-owned store | 02, 09 |
| [0003](https://github.com/talvor/AssemblyAI/blob/main/docs/adr/0003-go-executable-runs-pinned-providers.md) | AsmAI is one Go executable that runs its own pinned provider CLIs with per-session settings | 03, 09, 10 |
| [0004](https://github.com/talvor/AssemblyAI/blob/main/docs/adr/0004-attach-client-draws-status-line.md) | The attach client draws each agent's screen under an AsmAI status line | 03, 04 |
| [0005](https://github.com/talvor/AssemblyAI/blob/main/docs/adr/0005-jobs-work-in-an-asmai-owned-clone.md) | Jobs work in an AsmAI-owned clone, and the job branch moves only on acceptance | 05 |
| [0006](https://github.com/talvor/AssemblyAI/blob/main/docs/adr/0006-agents-use-only-the-pinned-skill-bundle.md) | Agents use only AsmAI's pinned skill bundle, passed per session | 08 |
| [0007](https://github.com/talvor/AssemblyAI/blob/main/docs/adr/0007-asmai-delivers-tested-prs-with-its-own-roles.md) | AsmAI delivers tested pull requests with its own roles; no-mistakes is not adopted in v1 | 06 |
| [0008](https://github.com/talvor/AssemblyAI/blob/main/docs/adr/0008-qualification-runs-real-provider-clis-on-real-hosts.md) | Qualification runs real provider CLIs on real hosts | 11 |
| [0009](https://github.com/talvor/AssemblyAI/blob/main/docs/adr/0009-a-release-is-the-qualified-commit-plus-its-record.md) | A release is the qualified commit plus its qualification record | 10, 11 |

## Testing decisions

Three kinds of evidence, each with its own purpose ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27), [AssemblyAI#12](https://github.com/talvor/AssemblyAI/issues/12), [ADR 0008](https://github.com/talvor/AssemblyAI/blob/main/docs/adr/0008-qualification-runs-real-provider-clis-on-real-hosts.md)):

- **Development tests** run on every PR in hosted CI, on Linux and on GitHub's hosted macOS runners. They use a scripted fake provider CLI that plays hook payloads and screens recorded from the real pinned versions. The fake never counts toward qualification and never certifies a combination.
- **Qualification** runs the 47 qualification cases in a harness that drives the real pinned providers on a real host of each platform, under a separate OS user with its own sign-in and its own factory. It is run by the maintainer, never in hosted CI. The harness lives in talvor/asmai and is built only into development builds. [11 Qualification and proving](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/11-qualification-and-proving.md) specifies it.
- **Proving scenarios** S1 to S9 run real jobs end to end on the proving ground, on a release candidate, and each passes on its evidence checklist and the user's verdict. [11 Qualification and proving](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/11-qualification-and-proving.md) specifies them.

Each component document lists the qualification cases and proving scenarios its rules serve.

## The two repositories

- **talvor/AssemblyAI** keeps the planning record: the map, the decision tickets, the ADRs, the glossary, the Lavish records and this specification. It is not renamed ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27)).
- **talvor/asmai** is created in M0 as a new repository for AsmAI's code, its implementation tickets and its releases. Releases are published at github.com/talvor/asmai/releases, so the install command is `curl -fsSL https://github.com/talvor/asmai/releases/latest/download/install.sh | sh` ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27), [AssemblyAI#20](https://github.com/talvor/AssemblyAI/issues/20)).
- **What is copied.** Nothing is brought across from talvor/AssemblyAI except a copy of `GLOSSARY.md` and ADRs 0001 to 0009 as they stand when this specification is confirmed. From then on they evolve in talvor/asmai, and new ADRs there are numbered from 0010. The copies in talvor/AssemblyAI remain the record of the planning ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27)).
- **The proving scenarios** make S1's feature (the v2 notify command) and S4's defect fix in talvor/asmai, and their record lives in talvor/asmai beside the releases it judges ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27)).

## This specification

- **Where it lives.** Markdown documents in talvor/AssemblyAI under `docs/spec/`, reviewed and merged by PR ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27)).
- **Self-contained.** It states every decision in its final form, and each rule cites the ticket or ADR it comes from. Where a later ticket changed an earlier one, only the final rule appears. Glossary terms and ADRs are cited, not copied ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27)).
- **Links.** Every link points at talvor/AssemblyAI, including links between the documents, so the tickets that to-tickets copies them into lead back here ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27)).
- **Authority.** Once confirmed, the specification is the authority for implementation until v1.0.0. A rule change found while building is made here by PR first, and the talvor/asmai ticket or PR links that change. At v1.0.0 it is frozen as the record of v1, and later changes are recorded in talvor/asmai ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27)).
- **How it was written.** The whole specification was written before implementation started, one document at a time from its tickets, ADRs and the glossary. The user reviewed each document on a Lavish board, where any contradiction between tickets reached the user as a question, and then confirmed the whole ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27)).
- **Configuration and agent instructions.** [09 CLI and configuration](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/09-cli-and-configuration.md) lists every configuration field with its name, type, default and meaning. [08 Skills and agent instructions](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/08-skills-and-agent-instructions.md) says what each role's instructions, the operating guide, the leaders' skill indexes and the PR section in workers' results must contain. Their exact wording is written during implementation and proved by the proving scenarios ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27)).

### Documents

| Document | Covers |
| --- | --- |
| [00 Overview](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/00-overview.md) | Problem, solution, user stories, scope and out of scope; vocabulary by reference to the glossary; the two repositories; the build order; traceability |
| [01 Roles and decisions](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/01-roles-and-decisions.md) | Roles, leaders and workers, handoffs, assignments and acceptance, mandates and grants, delegated decisions, escalation, versioned decision requests, answer surfaces, witnessed messages |
| [02 Daemon and store](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/02-daemon-and-store.md) | Daemon start, stop and service; the store and journal; jobs; dispatch and assignment life cycles; inbox and nudges; generations and fencing; effects; reconciliation; leaders on demand; recovery |
| [03 Provider sessions and terminals](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/03-provider-sessions-and-terminals.md) | Pinned provider copies and per-session settings; daemon-owned PTYs; hook intake; the input fence and positive submission acknowledgment; the modal allow-list; the attach client and status line; take, release and intervention records; recordings |
| [04 Conversation and Lavish](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/04-conversation-and-lavish.md) | The conversation, focused job, one-line updates, catch-up, unsent text and second attach; the Lavish server, rendering decision requests and collecting answers |
| [05 Repositories and job branches](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/05-repositories-and-job-branches.md) | The registry, AsmAI's clone, workspaces and assignment branches, the job branch and fast-forward on acceptance, keeping current, conflicts and outside commits, notes, the leaders' view, repository instructions, commit trailers, cleanup |
| [06 Validation and delivery](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/06-validation-and-delivery.md) | Engineering's tests, Quality's validation and findings, the tested pull request, push, draft PR, PR body, CI watching, the no-CI declaration, the failed-validation limit, the end of a job |
| [07 Limits, holds and visibility](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/07-limits-holds-and-visibility.md) | Worker caps and the queue, allowance, provider failures and lost sign-in, holds, work that keeps failing, job pause, resume and cancel, timeouts, `asmai status`, disk, logs |
| [08 Skills and agent instructions](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/08-skills-and-agent-instructions.md) | The skill bundle and operating guide, skill lists and leaders' indexes, per-provider delivery and hiding, added and repository skills, repository setup, reuse of decisions at skills' human steps, what each role's instructions must say |
| [09 CLI and configuration](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/09-cli-and-configuration.md) | Names, human and agent commands and the agent guard, output formats, addressing, `asmai init` and `doctor`, the configuration file and its schema, `config apply` |
| [10 Release, install and upgrade](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/10-release-install-and-upgrade.md) | License and notices, the build, the release workflow and attestations, the install script, version numbers, upgrades, provider pins, configuration across releases, store migrations and restore |
| [11 Qualification and proving](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/11-qualification-and-proving.md) | The harness, the separate OS user, fault injection and replay, the fixture repository, the 47 cases, the qualification record and doctor's self-check, the proving scenarios, their checklists and record |
| [milestones/M0](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/milestones/M0-groundwork.md) to [M8](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/milestones/M8-release-and-upgrade.md) | Which rules of which component documents each milestone delivers, its exit checks, and the cases and demo path that close it |

Each component document has the same sections: rules; interfaces (commands, store records, files); settings and defaults; failure handling; the qualification cases and proving scenarios it serves; and its sources ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27)).

## Building v1

- **Who builds it.** Firstmate crews implement the tickets with the implement and tdd skills, each ticket a PR in talvor/asmai gated by no-mistakes, which Phillip merges. AsmAI first works on its own code at the release candidate, in the proving scenarios. Phillip may try development builds on side tasks at any time ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27)).
- **Tickets.** Phillip runs to-tickets in talvor/asmai on the milestone documents, in order, one milestone at a time. Its tickets are vertical slices that link into the component documents, each blocked by tickets of its own run or by the previous milestone ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27)).
- **Order.** A walking skeleton first, then milestones that widen it toward the proving scenarios, with the qualification harness growing at each step. Between them the milestones cover all 47 cases ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27)):

| Milestone | What it adds | Cases that pass at its end | What it makes possible |
| --- | --- | --- | --- |
| [M0 Groundwork](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/milestones/M0-groundwork.md) | talvor/asmai with the copied glossary and ADRs, its tracker and no-mistakes gating; the Go module `github.com/talvor/asmai`; hosted CI on Linux and macOS with the fake provider, the license allow-list and generated notices; the fixture repository and the harness's separate OS users on this host and the Mac | None | Every later milestone |
| [M1 Walking skeleton](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/milestones/M1-walking-skeleton.md) | On Claude only: `asmai start` and `stop`, the daemon, store and journal, daemon-owned terminals with hooks, nudges and `asmai inbox`, attaching to the conversation. Coordination opens a job from the user's witnessed message and hands it to Engineering; one writing assignment in a workspace of AsmAI's clone; acceptance fast-forwards the job branch; Quality validates the head; the daemon pushes, the Engineering leader opens a draft PR, and the daemon watches CI and marks it ready; the link is reported | C3, C4, C7, C11, C19, C36, C37, C41, C42, C43, C45 | A tested PR on the fixture repository, end to end |
| [M2 Both providers and skills](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/milestones/M2-both-providers-and-skills.md) | Codex sessions and mixed staffing; `providers install`, `init` and `doctor`; the configuration file; the skill bundle, its delivery and hiding; platform certification checks; M1's cases rerun on Codex | C1, C2, C33, C34, C35 | S1's skeleton with each role on either provider |
| [M3 Decisions and planning](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/milestones/M3-decisions-and-planning.md) | Decision requests, answer surfaces and grants; the Lavish server, rendering and answer collection; Planning and Research; notes delivery; jobs without a repository; several assignments per job | None new | The full S1 path, S2, S3, S4 |
| [M4 Conversation and intervention](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/milestones/M4-conversation-and-intervention.md) | The status line, focused job, catch-up, unsent text and second attach; take, release and intervention records; the modal allow-list; recordings and replay | C6, C8, C9, C10, C12, C13, C14 | S7's decision and intervention parts |
| [M5 Concurrency and limits](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/milestones/M5-concurrency-and-limits.md) | Worker caps and the queue; concurrent jobs and repositories; conflicts and outside commits; leaders on demand; allowance, provider failures, lost sign-in and holds; job pause, resume and cancel; the no-CI declaration and the 15-minute wait; the failed-validation limit; the disk floor | C26 to C32, C38, C39, C44 | S5, S6, S7 |
| [M6 Recovery](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/milestones/M6-recovery.md) | Full reconciliation; generations and fencing; orphan termination; agent crash, daemon crash and reboot with the service; `asmai stop` draining; terminal disconnect; a crash during a push or between the push and the PR | C15 to C18, C20 to C25, C40, C46 | S8 |
| [M7 Remote hosts](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/milestones/M7-remote-hosts.md) | `--host`, Lavish through port forwarding, plain `ssh -t host asmai` | C47 | S9, on the virtual machine Phillip sets up then |
| [M8 Release and upgrade](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/milestones/M8-release-and-upgrade.md) | The release workflow and attestations; the install script; the running factory keeping its version; new provider pins at start; store migrations, backups and `asmai restore`; `asmai notices`; the qualification record that `start` enforces | C5, then all 47 together on the candidate commit | The first release candidate |
| Proving and launch | S1 to S9 on the release candidate, with Phillip's verdicts; AsmAI builds the v2 notify command (S1) and fixes a real defect (S4) in talvor/asmai | All 47 on Linux x86_64 | v1.0.0 on Linux; macOS certified by a later release |

- **Two corrections to the table in [AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27)**, made in review of this document ([answers](https://github.com/talvor/AssemblyAI/blob/main/.lavish/spec-doc-00-answers.json)): S7 needs job pause, resume and cancel, which M5 adds, so the whole of S7 is first possible at M5's end; and in M1, as everywhere, the Engineering leader opens the PR, as [AssemblyAI#18](https://github.com/talvor/AssemblyAI/issues/18) and [ADR 0007](https://github.com/talvor/AssemblyAI/blob/main/docs/adr/0007-asmai-delivers-tested-prs-with-its-own-roles.md) decided.
- **The end of a milestone.** A milestone ends when its tickets are closed, the development tests are green on both platforms, its qualification cases pass in the harness on Linux and have run on the Mac, and its demo path has run once on the fixture repository, with the terminal recording kept for Phillip to watch. A macOS failure becomes a ticket in the next milestone and never holds up the Linux release candidate ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27)).
- **The Mac** is one Phillip already has. M0 sets it up with the harness's separate OS user ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27)).
- **Launch.** v1 launches when Linux is certified and every proving scenario has passed. macOS follows when it is certified. Nothing a burn-in period would find holds up the launch; it becomes a fix in a later release ([AssemblyAI#12](https://github.com/talvor/AssemblyAI/issues/12)).

## Traceability

### Decision tickets to documents

| Ticket | Specified in |
| --- | --- |
| [AssemblyAI#2 Research Firstmate and Openrig coordination patterns](https://github.com/talvor/AssemblyAI/issues/2) | Research only: background, no rules. Its ideas reach the specification through [AssemblyAI#16](https://github.com/talvor/AssemblyAI/issues/16) |
| [AssemblyAI#3 Map Matt Pocock skills to factory roles](https://github.com/talvor/AssemblyAI/issues/3) | Research only: the skill inventory behind 08 |
| [AssemblyAI#4 Research agent runtimes and persistent sessions](https://github.com/talvor/AssemblyAI/issues/4) | Research only: background for 02 and 03 |
| [AssemblyAI#5 Define roles and leader-worker contracts](https://github.com/talvor/AssemblyAI/issues/5) | 01; 08 (skill homes) |
| [AssemblyAI#6 Define delegated authority and human escalation](https://github.com/talvor/AssemblyAI/issues/6) | 01 |
| [AssemblyAI#7 Choose factory hosting and lifecycle](https://github.com/talvor/AssemblyAI/issues/7) | 02, 03, 09; 00 (platforms) |
| [AssemblyAI#8 Define work state and coordination contracts](https://github.com/talvor/AssemblyAI/issues/8) | 02; 01 (decision records); 09 (agent commands) |
| [AssemblyAI#9 Define CLI setup and management experience](https://github.com/talvor/AssemblyAI/issues/9) | 09; 03 (pinned copies and per-session settings); 10 (installation) |
| [AssemblyAI#10 Explore terminal conversation and Lavish decision flow](https://github.com/talvor/AssemblyAI/issues/10) | 04; 01 (answer surfaces, witnessed messages); 03 (status line, take and release) |
| [AssemblyAI#11 Define concurrent repository work and integration](https://github.com/talvor/AssemblyAI/issues/11) | 05; 09 (repository settings) |
| [AssemblyAI#12 Define v1 acceptance scenarios and evidence](https://github.com/talvor/AssemblyAI/issues/12) | 11; 00 (launch); every component document (its cases) |
| [AssemblyAI#13 Choose the AsmAI product name](https://github.com/talvor/AssemblyAI/issues/13) | 00; 09 (names) |
| [AssemblyAI#14 Define operating limits and visibility](https://github.com/talvor/AssemblyAI/issues/14) | 07; 02 (leaders on demand); 09 (settings) |
| [AssemblyAI#15 Choose runtime adapters and authentication](https://github.com/talvor/AssemblyAI/issues/15) | 03, 07; 01 (provider replacement as a decision); 00 (scope) |
| [AssemblyAI#16 Choose inspiration versus reuse of reference systems](https://github.com/talvor/AssemblyAI/issues/16) | 00 (independent core); 10 (copying a component needs a decision) |
| [AssemblyAI#17 Choose skill bundles and update policy](https://github.com/talvor/AssemblyAI/issues/17) | 08; 09 (skill settings) |
| [AssemblyAI#18 Choose validation and delivery ownership](https://github.com/talvor/AssemblyAI/issues/18) | 06; 08 (operating-guide mappings, PR section); 01 (findings that need the user) |
| [AssemblyAI#19 Validate interactive CLI coordination and intervention](https://github.com/talvor/AssemblyAI/issues/19) | 03, 02 |
| [AssemblyAI#20 Choose license, release packaging and upgrade migration](https://github.com/talvor/AssemblyAI/issues/20) | 10 |
| [AssemblyAI#27 Choose the specification's structure and implementation sequence](https://github.com/talvor/AssemblyAI/issues/27) | 00; 11 (development tests, the harness); M0 to M8 |

### Qualification cases to documents and milestones

Each case is listed under the document whose rules it qualifies; other documents that rely on it also list it among the cases they serve. The case wording is from [AssemblyAI#12](https://github.com/talvor/AssemblyAI/issues/12), and [11 Qualification and proving](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/11-qualification-and-proving.md) holds the full list.

| Case | What it qualifies | Document | Milestone |
| --- | --- | --- | --- |
| C1 | Platform certification on Linux and macOS; an uncertified platform refuses to start agents | 09 | M2 |
| C2 | An unqualified provider version is refused before any dispatch; a self-upgraded provider CLI holds its agent at the next restart | 03 | M2 |
| C3 | The pinned provider copies reuse the user's existing sign-in | 03 | M1 |
| C4 | Every agent session starts without provider API-key variables | 03 | M1 |
| C5 | Codex hook trust survives an AsmAI upgrade | 10 | M8 |
| C6 | Native modals: any input state not on the allow-list holds the agent | 03 | M4 |
| C7 | Positive acknowledgment of each automated submission | 03 | M1 |
| C8 | Taking an agent mid-turn and with an unsent automated draft | 03 | M4 |
| C9 | The attach client's rendering under the status line, at reduced height | 03 | M4 |
| C10 | Detecting unsent text in the conversation and clearing the input box | 04 | M4 |
| C11 | Capturing witnessed messages and telling them apart from nudges | 03 | M1 |
| C12 | Recognising an interrupted Claude turn | 03 | M4 |
| C13 | A second attach takes over; the older terminal only observes | 04 | M4 |
| C14 | Terminal recording per dispatch, and replay | 03 | M4 |
| C15 | Lost, duplicate, reordered and late hooks and observations | 02 | M6 |
| C16 | A superseded leader or worker generation is rejected | 02 | M6 |
| C17 | Agent processes left by a previous daemon are terminated at start | 02 | M6 |
| C18 | A crash during an effect is recovered through reconciliation | 02 | M6 |
| C19 | Dispatches and results stay correlated and reconcilable across restarts | 02 | M1 |
| C20 | A working dispatch with no observation for 30 minutes becomes unknown | 02 | M6 |
| C21 | Agent crash: a leader restarts within its bound; a worker's assignment needs reconciliation | 02 | M6 |
| C22 | Daemon crash | 02 | M6 |
| C23 | Host reboot with the service installed | 02 | M6 |
| C24 | Terminal and SSH disconnect | 03 | M6 |
| C25 | `asmai stop` drains; `asmai stop --now` interrupts | 02 | M6 |
| C26 | Expired or revoked sign-in holds work and resumes when sign-in is back | 07 | M5 |
| C27 | Allowance used and reset times, for each provider | 07 | M5 |
| C28 | Allowance used up: agents hold, then resume at the reset | 07 | M5 |
| C29 | A reported provider error resumes with backoff; past the bound the provider is unavailable | 07 | M5 |
| C30 | Fallback to the other provider only before first dispatch, including a leader's on-demand start | 07 | M5 |
| C31 | Leaders start when a message for their role arrives and stop after the idle grace | 02 | M5 |
| C32 | Below the free-space floor no new workspace is created | 07 | M5 |
| C33 | Personal, provider built-in and repository skills are hidden | 08 | M2 |
| C34 | Per-session skill delivery works with Claude's namespaced plugin skills | 08 | M2 |
| C35 | Codex finds the skills written into its workspace | 08 | M2 |
| C36 | Instruction files load without the repository's provider configuration | 05 | M1 |
| C37 | Provider write guards are switched on | 05 | M1 |
| C38 | Concurrent jobs in one repository | 05 | M5 |
| C39 | Outside commits are merged in and never force-pushed over | 05 | M5 |
| C40 | A crash during a push | 06 | M6 |
| C41 | The daemon's push, and its refusal when origin holds outside commits | 06 | M1 |
| C42 | A draft PR, and the "[not ready]" fallback | 06 | M1 |
| C43 | CI watched through gh: green; red with one judged re-run; a newer push replacing the wait | 06 | M1 |
| C44 | The 15-minute wait for a first check, and the hold for a repository with no declared CI | 06 | M5 |
| C45 | Marking the PR ready when CI is green | 06 | M1 |
| C46 | A leader-opened PR reconciled as an effect, including a crash between the push and the PR | 06 | M6 |
| C47 | Remote use over SSH: `--host`, Lavish through port forwarding, and plain `ssh -t host asmai` | 09 | M7 |

All 47 run together on the candidate commit in M8, and again on Linux x86_64 for the launch ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27)).

### Proving scenarios to milestones

Every scenario runs for the record on the release candidate, after M8. The milestone named here is the one whose end first makes the whole scenario possible ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27), [AssemblyAI#12](https://github.com/talvor/AssemblyAI/issues/12)):

| Scenario | First possible at the end of |
| --- | --- |
| S1 Feature to tested PR | M3 (its skeleton at M2) |
| S2 Research | M3 |
| S3 Planning | M3 |
| S4 Diagnosis | M3 |
| S5 Concurrent repositories | M5 |
| S6 No CI | M5 |
| S7 Human decisions | M5 (its decision parts at M3, its intervention at M4) |
| S8 Local continuity | M6 |
| S9 Remote continuity | M7 |

## Sources

- [Chart AsmAI](https://github.com/talvor/AssemblyAI/issues/1): the map's destination, notes and out-of-scope list.
- [AssemblyAI#5](https://github.com/talvor/AssemblyAI/issues/5#issuecomment-5968317664), [#6](https://github.com/talvor/AssemblyAI/issues/6#issuecomment-5968467874), [#7](https://github.com/talvor/AssemblyAI/issues/7#issuecomment-5976506834), [#8](https://github.com/talvor/AssemblyAI/issues/8#issuecomment-5976668034), [#9](https://github.com/talvor/AssemblyAI/issues/9#issuecomment-5979143255), [#10](https://github.com/talvor/AssemblyAI/issues/10#issuecomment-5989237516), [#11](https://github.com/talvor/AssemblyAI/issues/11#issuecomment-5990301132), [#12](https://github.com/talvor/AssemblyAI/issues/12#issuecomment-5993314453), [#13](https://github.com/talvor/AssemblyAI/issues/13#issuecomment-5968140448), [#14](https://github.com/talvor/AssemblyAI/issues/14#issuecomment-5991304507), [#15](https://github.com/talvor/AssemblyAI/issues/15#issuecomment-5968867443), [#16](https://github.com/talvor/AssemblyAI/issues/16#issuecomment-5974485663), [#17](https://github.com/talvor/AssemblyAI/issues/17#issuecomment-5992055697), [#18](https://github.com/talvor/AssemblyAI/issues/18#issuecomment-5992792804), [#19](https://github.com/talvor/AssemblyAI/issues/19#issuecomment-5976021294), [#20](https://github.com/talvor/AssemblyAI/issues/20#issuecomment-6004145724) and [#27](https://github.com/talvor/AssemblyAI/issues/27#issuecomment-6004852593): the resolution comments.
- Research tickets [AssemblyAI#2](https://github.com/talvor/AssemblyAI/issues/2#issuecomment-5968135182), [#3](https://github.com/talvor/AssemblyAI/issues/3#issuecomment-5968136435) and [#4](https://github.com/talvor/AssemblyAI/issues/4#issuecomment-5968137383): background, not decisions.
- [ADRs 0001 to 0009](https://github.com/talvor/AssemblyAI/tree/main/docs/adr) and the [glossary](https://github.com/talvor/AssemblyAI/blob/main/GLOSSARY.md).
- The original scope answers: [wayfinder-answers.json](https://github.com/talvor/AssemblyAI/blob/main/.lavish/wayfinder-answers.json).
- The review of this document: [questions](https://github.com/talvor/AssemblyAI/blob/main/.lavish/spec-doc-00-round1-questions.json) and [answers](https://github.com/talvor/AssemblyAI/blob/main/.lavish/spec-doc-00-answers.json).
