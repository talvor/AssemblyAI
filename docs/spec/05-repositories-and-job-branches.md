# 05 Repositories and job branches

This document specifies how jobs work in repositories: the registry, AsmAI's own clone, workspaces and assignment branches, the job branch and its fast-forward on acceptance, keeping it current, conflicts and outside commits, notes, the leaders' view, repository instructions, commit trailers and cleanup. [06 Validation and delivery](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/06-validation-and-delivery.md) specifies how the finished job branch is validated, pushed and opened as a pull request.

## Rules

### The registry

1. **Registered repositories only.** Jobs can target only repositories the user has registered. The user registers them with `asmai repo add <path-or-url>`; Coordination tells the user the command and never registers one itself ([AssemblyAI#9](https://github.com/talvor/AssemblyAI/issues/9)).
2. **What registration records:** a name, the repository's location on the host, its origin remote and its default branch ([AssemblyAI#9](https://github.com/talvor/AssemblyAI/issues/9)).
3. **Listing and removing.** `asmai repo list|show|remove` list, show and remove registered repositories. Removing a repository with open jobs is refused ([AssemblyAI#9](https://github.com/talvor/AssemblyAI/issues/9)).
4. **Setup on registration.** Registering a repository without `docs/agents/issue-tracker.md` makes Coordination open a setup job ([AssemblyAI#17](https://github.com/talvor/AssemblyAI/issues/17), [08](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/08-skills-and-agent-instructions.md)).

### AsmAI's clone

5. **Never the user's checkout.** Each registered repository has an AsmAI-owned clone in the state directory, fetched from origin, and every workspace is made from it. The user's own checkout is never used, although the registry records where it is ([AssemblyAI#11](https://github.com/talvor/AssemblyAI/issues/11), [ADR 0005](https://github.com/talvor/AssemblyAI/blob/main/docs/adr/0005-jobs-work-in-an-asmai-owned-clone.md)).

### Workspaces

6. **The daemon owns them.** The daemon creates each workspace when it dispatches the assignment, starts the worker inside it, and is the only party that creates or removes workspaces ([AssemblyAI#11](https://github.com/talvor/AssemblyAI/issues/11)).
7. **Writing and read-only.** A writing assignment works on its own assignment branch, made from the job branch's tip. A read-only assignment's workspace is fixed at the commit it examines, and its evidence names that commit ([AssemblyAI#11](https://github.com/talvor/AssemblyAI/issues/11)).
8. **No repository.** In a job without a repository, each assignment gets an empty scratch workspace ([AssemblyAI#11](https://github.com/talvor/AssemblyAI/issues/11)).
9. **Staying inside.** Staying inside the workspace is part of every worker's instructions, and any write outside it is an effect to record. The providers' qualified write guards are switched on as a guard against mistakes, not as a security boundary ([AssemblyAI#11](https://github.com/talvor/AssemblyAI/issues/11), [03](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/03-provider-sessions-and-terminals.md)).
10. **Slots.** Every workspace gets a slot number and its own temporary directory, given to the worker as `ASMAI_SLOT` and `TMPDIR` ([AssemblyAI#11](https://github.com/talvor/AssemblyAI/issues/11)).
11. **Checks that cannot run side by side.** A repository whose checks cannot run side by side says so, and agents run those checks through an `asmai` command that takes turns per repository ([AssemblyAI#11](https://github.com/talvor/AssemblyAI/issues/11)). The declaration is one per-repository switch. When it is on, agents run the repository's checks through `asmai turn -- <command>`, which waits until no other workspace of that repository is running one, then runs the command and passes its exit status through ([answers](https://github.com/talvor/AssemblyAI/blob/main/.lavish/spec-doc-05-answers.json)).
12. **Disk.** Below the free-space floor on the state directory's volume, the daemon creates no new workspace, and the assignments waiting for one hold ([AssemblyAI#14](https://github.com/talvor/AssemblyAI/issues/14), [07](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/07-limits-holds-and-visibility.md)).

### The job branch

13. **One per repository job.** Each repository job has one job branch, which becomes its pull request. It starts from the default branch as fetched from origin, or from another origin branch the user names, and the job records the commit it started from ([AssemblyAI#11](https://github.com/talvor/AssemblyAI/issues/11)).
14. **Branch names.** The job branch is named `asmai/job-<n>-<slug>`, with the slug taken from the job's title, and each assignment branch `asmai/job-<n>/<assignment>`. The daemon names them when it makes them, and a follow-up that continues an open pull request keeps its job branch (rule 16) ([answers](https://github.com/talvor/AssemblyAI/blob/main/.lavish/spec-doc-05-answers.json)).
15. **One writer per branch.** Only one party writes a branch at any time ([AssemblyAI#11](https://github.com/talvor/AssemblyAI/issues/11)). The daemon is the only party that ever moves the job branch, locally or on origin ([AssemblyAI#18](https://github.com/talvor/AssemblyAI/issues/18)).
16. **One open job per job branch.** A job branch belongs to one open job at a time. A follow-up to a job whose pull request is still open continues on that job branch and pull request, starting from origin's copy. Once the pull request is merged or closed, a follow-up starts from the base with a new job branch and pull request ([AssemblyAI#11](https://github.com/talvor/AssemblyAI/issues/11)).

### Accepted work

17. **Workers take in the tip.** A worker takes in the job branch's tip before submitting a result ([AssemblyAI#11](https://github.com/talvor/AssemblyAI/issues/11)).
18. **Fast-forward on acceptance.** When the owning leader accepts a result with `asmai accept`, the daemon fast-forwards the job branch to the accepted commit as part of recording the acceptance ([AssemblyAI#11](https://github.com/talvor/AssemblyAI/issues/11), [ADR 0005](https://github.com/talvor/AssemblyAI/blob/main/docs/adr/0005-jobs-work-in-an-asmai-owned-clone.md)).
19. **A moved tip.** If the job branch moved after the result was submitted, the work returns to the same worker to take in the new tip and submit again. This is not a rejection ([AssemblyAI#11](https://github.com/talvor/AssemblyAI/issues/11)).
20. **Workers resolve conflicts.** Conflicts are always resolved by a worker inside an assignment, never by a leader or the daemon ([AssemblyAI#11](https://github.com/talvor/AssemblyAI/issues/11), [ADR 0005](https://github.com/talvor/AssemblyAI/blob/main/docs/adr/0005-jobs-work-in-an-asmai-owned-clone.md)).

### Keeping current and conflicts

21. **Taking in the base.** The job branch takes in the latest base before it is offered for review and before each later push ([AssemblyAI#11](https://github.com/talvor/AssemblyAI/issues/11)).
22. **Merge or rebase.** The base is merged in ([AssemblyAI#11](https://github.com/talvor/AssemblyAI/issues/11)). A repository whose instructions ask for a rebase has its job branch rebased, by a worker, until the job branch is first pushed; after that the base is merged in, because the job branch is never force-pushed, and the PR body states the exception ([AssemblyAI#18](https://github.com/talvor/AssemblyAI/issues/18), [ADR 0007](https://github.com/talvor/AssemblyAI/blob/main/docs/adr/0007-asmai-delivers-tested-prs-with-its-own-roles.md), [answers](https://github.com/talvor/AssemblyAI/blob/main/.lavish/spec-doc-05-answers.json)). This replaces the force-with-lease rewrite that AssemblyAI#11 allowed.
23. **Conflicts are ordinary work.** Resolving a conflict is ordinary writing work, and a choice between distinct viable approaches in it goes to the user ([AssemblyAI#11](https://github.com/talvor/AssemblyAI/issues/11), [01](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/01-roles-and-decisions.md)).
24. **Concurrent jobs in one repository** run with no locks and no overlap report. A conflict is resolved in whichever job meets it when its branch is brought up to date ([AssemblyAI#11](https://github.com/talvor/AssemblyAI/issues/11)).
25. **Outside commits.** Before every push, the job's branch is fetched from origin. Commits AsmAI did not make are kept and merged in by a worker, recorded as an outside change and reported in one line; they are never force-pushed over ([AssemblyAI#11](https://github.com/talvor/AssemblyAI/issues/11), [AssemblyAI#18](https://github.com/talvor/AssemblyAI/issues/18)). After a restore, commits pushed since the backup count as outside changes ([AssemblyAI#20](https://github.com/talvor/AssemblyAI/issues/20)).

### Branches on origin

26. **Assignment branches are pushed.** A worker commits and pushes its assignment branch whenever it submits a result, reports that it is blocked, or is cancelled, committing any uncommitted changes first. Each push is an effect ([AssemblyAI#11](https://github.com/talvor/AssemblyAI/issues/11)).
27. **Part of every mandate.** Pushing assignment branches and the job branch is part of every repository job's mandate, including research-only and planning-only jobs ([AssemblyAI#11](https://github.com/talvor/AssemblyAI/issues/11)).
28. **Kept until the user deletes them.** Assignment branches stay on origin until the user deletes them, and none is opened as a pull request ([AssemblyAI#11](https://github.com/talvor/AssemblyAI/issues/11)).

### Notes and prototypes

29. **Not copied from the tracker.** A note that its workflow already records in the issue tracker, such as a resolution comment or a PR review, is not copied anywhere ([AssemblyAI#11](https://github.com/talvor/AssemblyAI/issues/11)).
30. **Other notes go on the job branch.** Any other note, such as research findings or a diagnosis log, is committed to the job branch by a writing assignment. It goes where the repository already keeps such notes, according to its repository instructions or existing folders, and otherwise under `docs/<kind>/`; the result says where ([AssemblyAI#11](https://github.com/talvor/AssemblyAI/issues/11)).
31. **Prototypes stay on their branch.** A prototype stays on its own assignment branch on origin. Its verdict, with a pointer to that branch, is a note ([AssemblyAI#11](https://github.com/talvor/AssemblyAI/issues/11)).
32. **Notes deliver like code.** A repository job whose outcome is notes is delivered like any other: its job branch is pushed and opened as a pull request holding its notes, for the user to review and merge ([AssemblyAI#11](https://github.com/talvor/AssemblyAI/issues/11), [06](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/06-validation-and-delivery.md)).

### The leaders' view

33. **One read-only view per repository job.** The daemon keeps one read-only view of each repository job at the job branch's tip, refreshed whenever the branch moves. Leaders read code and repository instructions there, and the job's brief points to it. Leaders never write in it, and it is not a workspace ([AssemblyAI#11](https://github.com/talvor/AssemblyAI/issues/11)).

### Repository instructions

34. **Instruction files apply.** Agents follow the repository's instruction files, and both providers see `AGENTS.md` and `CLAUDE.md`, whichever exist. The user's notes for the repository in AsmAI's configuration count as repository instructions too ([AssemblyAI#11](https://github.com/talvor/AssemblyAI/issues/11)).
35. **Provider configuration does not.** The repository's provider configuration (`.claude` settings, hooks, permission rules, MCP servers and `.codex` configuration) is never loaded ([AssemblyAI#11](https://github.com/talvor/AssemblyAI/issues/11)).
36. **Loading instruction files.** Whether a provider loads instruction files without loading project configuration is qualified per provider version; AsmAI can always pass their content itself ([AssemblyAI#11](https://github.com/talvor/AssemblyAI/issues/11)).
37. **Never wider than the mandate.** Repository instructions decide how work is done in the repository but never widen a mandate. A conflict between them and the mandate is escalated ([AssemblyAI#11](https://github.com/talvor/AssemblyAI/issues/11)). They never decide how the job branch is pushed ([AssemblyAI#18](https://github.com/talvor/AssemblyAI/issues/18), [06](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/06-validation-and-delivery.md)).

### Commits

38. **The user's identity.** Agents commit with the user's git identity and use the user's existing git and gh credentials. AsmAI handles no tokens ([AssemblyAI#11](https://github.com/talvor/AssemblyAI/issues/11)).
39. **Trailers.** Every commit carries `AsmAI-Job`, `AsmAI-Agent` and `AsmAI-Dispatch` trailers, which a repository whose conventions forbid trailers can switch off ([AssemblyAI#11](https://github.com/talvor/AssemblyAI/issues/11)).

### Local cleanup

40. **Writing workspaces** are removed once their work is on the job branch, and **read-only workspaces** when their assignment ends ([AssemblyAI#11](https://github.com/talvor/AssemblyAI/issues/11)).
41. **Kept for reconciliation.** A workspace whose assignment needs reconciliation is kept until the reconciliation is recorded ([AssemblyAI#11](https://github.com/talvor/AssemblyAI/issues/11)).
42. **Kept until the job ends.** The workspace of cancelled or abandoned work is kept until the job ends; its work is already pushed ([AssemblyAI#11](https://github.com/talvor/AssemblyAI/issues/11)).
43. **At the end of a job,** everything local to it is removed, and its branches on origin stay ([AssemblyAI#11](https://github.com/talvor/AssemblyAI/issues/11)).
44. **Scratch workspaces** of a job without a repository are kept after the job ends, until the user removes them with `asmai job clean <n>`, which is refused while the job is open ([AssemblyAI#11](https://github.com/talvor/AssemblyAI/issues/11), [AssemblyAI#14](https://github.com/talvor/AssemblyAI/issues/14)).

## Interfaces

### Commands

| Who | Command | Purpose |
| --- | --- | --- |
| The user | `asmai repo add <path-or-url>` | Register a repository (rules 1, 2) |
| The user | `asmai repo list\|show\|remove` | List, show or remove registered repositories (rule 3) |
| The user | `asmai job clean <n>` | Remove an ended job's kept workspaces (rule 44) |
| Leaders | `asmai accept` | Accept a result; the daemon fast-forwards the job branch (rule 18) |
| Agents | `asmai turn -- <command>` | Run one of the repository's checks in its turn (rule 11) |

### Store records

| Record | Holds |
| --- | --- |
| Registered repository | Name, location on the host, origin remote, default branch, and the clone's path ([AssemblyAI#9](https://github.com/talvor/AssemblyAI/issues/9)) |
| Job branch | Its repository, name, the commit it started from, its current tip, the open job it belongs to, and its pull request once opened |
| Workspace | Its assignment, slot, path, branch or fixed commit, and whether it is kept and why |
| Outside change | The commits AsmAI did not make, where they were found, and the merge that took them in |

### Files

- **AsmAI's clone** of each registered repository, and every workspace, in the state directory (rules 5, 6).
- **The leaders' view** of each repository job (rule 33).
- **Notes** on the job branch, where the repository keeps them or under `docs/<kind>/` (rule 30).
- **The clone's own exclude file**, which keeps the Codex skill folders AsmAI writes into a workspace out of git ([08](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/08-skills-and-agent-instructions.md)).

## Settings and defaults

Per registered repository; [09](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/09-cli-and-configuration.md) names the fields.

| Setting | Default | Rule |
| --- | --- | --- |
| Notes, as repository instructions | None | 34 |
| Checks run one at a time (a switch) | Off | 11 |
| Commit trailers | On | 39 |

The no-CI declaration ([06](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/06-validation-and-delivery.md)) and repository-skill switches ([08](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/08-skills-and-agent-instructions.md)) are per-repository settings too. The free-space floor is factory-wide ([07](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/07-limits-holds-and-visibility.md)).

## Failure handling

| Failure | Handling |
| --- | --- |
| The job branch moved after a result was submitted | Back to the same worker to take in the tip; not a rejection (rule 19) |
| A conflict while taking in the base | A worker resolves it in an assignment; a choice between approaches goes to the user (rules 20, 23) |
| Outside commits on origin | Kept, merged in by a worker, reported; never force-pushed over (rule 25) |
| Repository instructions conflict with the mandate | Escalated (rule 37) |
| Below the free-space floor | No new workspace; the assignments hold (rule 12) |
| An assignment needs reconciliation | Its workspace is kept until the reconciliation is recorded (rule 41) |
| Removing a repository with open jobs | Refused (rule 3) |

## Qualification cases and proving scenarios

- **C36**: instruction files load without the repository's provider configuration (rules 34 to 36).
- **C37**: provider write guards are switched on (rule 9; [03](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/03-provider-sessions-and-terminals.md) rule 15).
- **C38**: concurrent jobs in one repository (rule 24).
- **C39**: outside commits are merged in and never force-pushed over (rule 25).
- **C32**: below the free-space floor no new workspace is created (rule 12; [07](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/07-limits-holds-and-visibility.md)).
- **C40**: a crash during a push ([06](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/06-validation-and-delivery.md)), which relies on rules 25 and 26.
- **S1**: several writing assignments accepted onto one job branch.
- **S2**: research notes delivered as a pull request, or in a scratch workspace for a job without a repository.
- **S5**: a second job in S1's repository meets a conflict that a worker resolves inside an assignment.

## Sources

- [Define CLI setup and management experience](https://github.com/talvor/AssemblyAI/issues/9#issuecomment-5979143255) (AssemblyAI#9)
- [Define concurrent repository work and integration](https://github.com/talvor/AssemblyAI/issues/11#issuecomment-5990301132) (AssemblyAI#11)
- [Define operating limits and visibility](https://github.com/talvor/AssemblyAI/issues/14#issuecomment-5991304507) (AssemblyAI#14)
- [Choose skill bundles and update policy](https://github.com/talvor/AssemblyAI/issues/17#issuecomment-5992055697) (AssemblyAI#17)
- [Choose validation and delivery ownership](https://github.com/talvor/AssemblyAI/issues/18#issuecomment-5992792804) (AssemblyAI#18)
- [Choose license, release packaging and upgrade migration](https://github.com/talvor/AssemblyAI/issues/20#issuecomment-6004145724) (AssemblyAI#20)
- [ADR 0005](https://github.com/talvor/AssemblyAI/blob/main/docs/adr/0005-jobs-work-in-an-asmai-owned-clone.md), [ADR 0007](https://github.com/talvor/AssemblyAI/blob/main/docs/adr/0007-asmai-delivers-tested-prs-with-its-own-roles.md) and the [glossary](https://github.com/talvor/AssemblyAI/blob/main/GLOSSARY.md): Registered repository, Repository instructions, Job branch, Assignment branch, Workspace.
- The review of this document: [questions](https://github.com/talvor/AssemblyAI/blob/main/.lavish/spec-doc-05-round1-questions.json) and [answers](https://github.com/talvor/AssemblyAI/blob/main/.lavish/spec-doc-05-answers.json).
