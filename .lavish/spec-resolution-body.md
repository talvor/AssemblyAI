## Resolution — confirmed by Phillip in Lavish

### Scope
This ticket settles how AsmAI's v1 specification is organized and kept, and the order in which v1 is built to reach the qualification harness and the proving scenarios settled in [Define v1 acceptance scenarios and evidence](https://github.com/talvor/AssemblyAI/issues/12). It also settles the map's last fog item, the configuration schema and agent instructions. Writing the specification is the next step, after this ticket; this ticket does not write it.

### Two repositories
- **No rename.** talvor/AssemblyAI stays as it is. It keeps the map, the decision tickets, the ADRs, the glossary, the Lavish records and the specification.
- **A new repository for the code.** M0 creates talvor/asmai as a new repository for AsmAI's code, its implementation tickets and its releases. Releases are still published at github.com/talvor/asmai/releases, so the install command is unchanged. Nothing is brought across from talvor/AssemblyAI, with one exception: talvor/asmai starts with a copy of `GLOSSARY.md` and ADRs 0001 to 0009 as they stand when the specification is confirmed. From then on they evolve in talvor/asmai, and new ADRs are numbered from 0010. The copies in talvor/AssemblyAI remain the record of the planning.
- **Links.** Every link in the specification points at talvor/AssemblyAI, so the tickets that to-tickets copies them into lead back to it.
- **The proving scenarios.** S1's feature (the v2 notify command) and S4's defect fix are made in talvor/asmai, where AsmAI's code lives. The record of the proving scenarios lives in talvor/asmai, beside the releases it judges.

### The specification
- **Where it lives.** Markdown documents in talvor/AssemblyAI under `docs/spec/`, reviewed and merged by PR. An issue cannot hold it: an issue body is limited to 65,536 characters, and the decisions alone come to about 110,000.
- **Self-contained.** It states every decision in its final form, and each rule cites the ticket or ADR it comes from. Where a later ticket changed an earlier one, only the final rule appears. Glossary terms and ADRs are cited, not copied.
- **Authority.** Once confirmed, the specification is the authority for implementation until v1.0.0. A rule change found while building is made in it by PR first, and the talvor/asmai ticket or PR links that change. At v1.0.0 it is frozen as the record of v1, and later changes are recorded in talvor/asmai.
- **Organized by component.** An overview in to-spec's form (problem, solution, user stories, out of scope), eleven component documents, and one milestone document per milestone:

| Document | Covers |
| --- | --- |
| 00 Overview | Problem, solution, user stories, scope and out of scope; vocabulary by reference to the glossary; the two repositories; traceability: each resolved ticket to its documents, each qualification case to its document and milestone, each proving scenario to its milestone |
| 01 Roles and decisions | Roles, leaders and workers, handoffs, assignments and acceptance, mandates and grants, delegated decisions, escalation, versioned decision requests, answer surfaces, witnessed messages |
| 02 Daemon and store | Daemon start, stop and service; the store and journal; jobs; dispatch and assignment life cycles; inbox and nudges; generations and fencing; effects; reconciliation; leaders on demand; recovery |
| 03 Provider sessions and terminals | Pinned provider copies and per-session settings; daemon-owned PTYs; hook intake; the input fence and positive submission acknowledgment; the modal allow-list; the attach client and status line; take, release and intervention records; recordings |
| 04 Conversation and Lavish | The conversation, focused job, one-line updates, catch-up, unsent text and second attach; the Lavish server, rendering decision requests and collecting answers |
| 05 Repositories and job branches | The registry, AsmAI's clone, workspaces and assignment branches, the job branch and fast-forward on acceptance, keeping current, conflicts and outside commits, notes, the leaders' view, repository instructions, commit trailers, cleanup |
| 06 Validation and delivery | Engineering's tests, Quality's validation and findings, the tested pull request, push, draft PR, PR body, CI watching, the no-CI declaration, the failed-validation limit, the end of a job |
| 07 Limits, holds and visibility | Worker caps and the queue, allowance, provider failures and lost sign-in, holds, work that keeps failing, job pause, resume and cancel, timeouts, `asmai status`, disk, logs |
| 08 Skills and agent instructions | The skill bundle and operating guide, skill lists and leaders' indexes, per-provider delivery and hiding, added and repository skills, repository setup, reuse of decisions at skills' human steps, what each role's instructions must say |
| 09 CLI and configuration | Names, human and agent commands and the agent guard, output formats, addressing, `asmai init` and `doctor`, the configuration file and its schema, `config apply` |
| 10 Release, install and upgrade | License and notices, the build, the release workflow and attestations, the install script, version numbers, upgrades, provider pins, configuration across releases, store migrations and restore |
| 11 Qualification and proving | The harness, the separate OS user, fault injection and replay, the fixture repository, the 47 cases, the qualification record and doctor's self-check, the proving scenarios, their checklists and record |
| milestones/M0 to M8 | Which rules of which component documents each milestone delivers, its exit checks, and the cases and demo path that close it |

- **Sections.** Each component document has the same sections: rules; interfaces (commands, store records, files); settings and defaults; failure handling; the qualification cases and proving scenarios it serves; and its sources.
- **Configuration and agent instructions.** The specification settles them, which clears the map's last fog item. 09 lists every configuration field with its name, type, default and meaning, drawn from the settled decisions, including the per-repository fields (notes, one-at-a-time checks, the no-CI declaration, repository-skill switches), skill lists and added skills. 08 says what each role's instructions, the operating guide, the leaders' skill indexes and the PR section in workers' results must contain. Their exact wording is written during implementation and proved by the proving scenarios.
- **Writing and confirming.** The whole specification is written before implementation starts. Planning sessions draft it one document at a time from its tickets, ADRs and the glossary. Phillip reviews each document on a Lavish board, where any contradiction between tickets reaches him as a question, and then confirms the whole before it merges. Implementation starts once it is confirmed.

### Building v1
- **Who builds it.** Firstmate crews implement the tickets with the implement and tdd skills, each ticket a PR in talvor/asmai gated by no-mistakes, which Phillip merges. AsmAI first works on its own code at the release candidate, in the proving scenarios. Phillip may try development builds on side tasks at any time.
- **Tickets.** Phillip runs to-tickets in talvor/asmai on the milestone documents, in order, one milestone at a time. Its tickets are vertical slices that link into the component documents, each blocked by tickets of its own run or by the previous milestone.
- **Order.** A walking skeleton first, then milestones that widen it toward the proving scenarios, with the qualification harness growing at each step. Between them the milestones cover all 47 cases:

| Milestone | What it adds | Cases that pass at its end | What it makes possible |
| --- | --- | --- | --- |
| M0 Groundwork | talvor/asmai created, with the copied glossary and ADRs; its tracker set up for the skills and no-mistakes gating its PRs; the Go module `github.com/talvor/asmai`; hosted CI on Linux and macOS with the fake provider, the license allow-list and generated notices; the fixture repository and the harness's separate OS users on this host and the Mac | None | Every later milestone |
| M1 Walking skeleton | On Claude only: `asmai start` and `stop`, the daemon, store and journal, daemon-owned terminals with hooks, nudges and `asmai inbox`, attaching to the conversation. Coordination opens a job from Phillip's witnessed message and hands it to Engineering; one writing assignment in a workspace of AsmAI's clone; acceptance fast-forwards the job branch; Quality validates the head; the daemon pushes, opens a draft PR, watches CI and marks it ready; the link is reported | C3, C4, C7, C11, C19, C36, C37, C41, C42, C43, C45 | A tested PR on the fixture repository, end to end |
| M2 Both providers and skills | Codex sessions and mixed staffing; `asmai providers install`, `init` and `doctor`; the configuration file; the skill bundle, its per-session delivery and hiding; platform certification checks; M1's cases rerun on Codex | C1, C2, C33, C34, C35 | S1's skeleton with each role on either provider |
| M3 Decisions and planning | Decision requests, answer surfaces and grants; the Lavish server, rendering and answer collection; Planning and Research roles; notes delivery; jobs without a repository; several assignments per job | None new (S3 and S7 prove these) | The full S1 path, S2, S3, S4 |
| M4 Conversation and intervention | The status line, focused job, catch-up, unsent text and second attach; take, release and intervention records; the modal allow-list; recordings and replay | C6, C8, C9, C10, C12, C13, C14 | S7 |
| M5 Concurrency and limits | Worker caps and the queue; concurrent jobs and repositories; conflicts and outside commits; leaders on demand; allowance, provider failures, lost sign-in and holds; job pause, resume and cancel; the no-CI declaration and the 15-minute wait; the failed-validation limit; the disk floor | C26 to C32, C38, C39, C44 | S5, S6 |
| M6 Recovery | Full reconciliation; generations and fencing; orphan termination; agent crash, daemon crash and reboot with the service installed (systemd and launchd); `asmai stop` draining; terminal disconnect; a crash during a push or between the push and the PR | C15 to C18, C20 to C25, C40, C46 | S8 |
| M7 Remote hosts | `--host`, Lavish through port forwarding, plain `ssh -t host asmai` | C47 | S9, on the virtual machine Phillip sets up then |
| M8 Release and upgrade | The release workflow and attestations; the install script; the running factory keeping its version; new provider pins at start; store migrations, backups and `asmai restore`; `asmai notices`; the qualification record that `start` enforces | C5, then all 47 together on the candidate commit | The first release candidate |
| Proving and launch | S1 to S9 on the release candidate, with Phillip's verdicts; AsmAI builds the v2 notify command (S1) and fixes a real defect (S4) in talvor/asmai | All 47 on Linux x86_64 | v1.0.0 on Linux; macOS certified by a later release |

- **The end of a milestone.** A milestone ends when its tickets are closed, the development tests are green on both platforms, its qualification cases pass in the harness on Linux and have run on the Mac (a macOS failure becomes a ticket in the next milestone), and its demo path has run once on the fixture repository, with the terminal recording kept for Phillip to watch.
- **Development tests.** Every PR runs development tests in hosted CI, using a scripted fake provider CLI that plays hook payloads and screens recorded from the real pinned versions. The fake never counts toward qualification; only the harness, with the real providers on a real host, qualifies (ADR 0008, which gains a dated line saying so).
- **The harness.** It lives in talvor/asmai, in its own directory, and is built only into development builds, never into a release executable, so it and the code it qualifies always share a commit. The fixture repository is a separate small repository Phillip owns, for example talvor/asmai-fixture.
- **macOS alongside.** Every PR builds for both platforms and runs the development tests on Linux and on GitHub's hosted macOS runners. At the end of each milestone its cases also run in the harness on a Mac. A macOS failure becomes a ticket in the next milestone and never holds up the Linux release candidate. macOS is certified by a release after Linux, as already decided.
- **The Mac.** MAC_LINE
- **Store migrations.** Kept from the first release candidate. Development builds may reset their store, but from v1.0.0-rc.1 every schema change is a kept forward-only migration, so a proving-scenario factory survives an upgrade to the next release candidate.

### Changes to earlier decisions
- [Choose license, release packaging and upgrade migration](https://github.com/talvor/AssemblyAI/issues/20) decided to rename talvor/AssemblyAI to talvor/asmai, with the map's issues and history moving with it. Instead, talvor/asmai is a new repository created in M0, and talvor/AssemblyAI keeps the planning record. Everything else in that resolution, including the release location and the install command, stands.
- [Define v1 acceptance scenarios and evidence](https://github.com/talvor/AssemblyAI/issues/12) put S1's feature on "AssemblyAI" and the record of the proving scenarios "in the AssemblyAI repository", both written when this repository was to become the code's home. Both now mean talvor/asmai.

### Glossary and ADR
- No glossary change: this ticket is about how AsmAI is built, not the factory's own language.
- [ADR 0008](https://github.com/talvor/AssemblyAI/blob/main/docs/adr/0008-qualification-runs-real-provider-clis-on-real-hosts.md) gains a dated line: development tests may use a scripted fake provider built from recorded payloads, and it never counts toward qualification (pending archive).
- No new ADR: the repository split is explained here, in the specification's overview and in talvor/asmai's README.

### Map follow-through
- **Decisions so far** gains this ticket's line, and **Notes** gain a pointer: the specification's structure and the implementation order are settled here.
- **Fog.** The configuration-schema and agent-instructions item is removed: the specification settles it.
- **No new ticket.** The map has no open tickets and no fog left: the way to the destination is clear. Writing the specification is the next step, outside the map.
- **No implementation.** This is a planning resolution; it authorizes no implementation.
