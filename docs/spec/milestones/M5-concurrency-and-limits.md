# M5 Concurrency and limits

M5 lets the factory run many jobs at once within its limits: worker caps and the queue, concurrent jobs and repositories, conflicts and outside commits, leaders on demand, allowance, provider failures, lost sign-in and holds, pausing, resuming and cancelling jobs, the no-CI declaration and the wait for a first check, the failed-validation limit, and the free-space floor ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27)).

## What it adds

1. **Worker caps and the queue,** first come first served, never overflowing to the other provider ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27), [07](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/07-limits-holds-and-visibility.md)).
2. **Concurrent jobs and repositories,** including several jobs in one repository, with conflicts resolved by workers, outside commits merged in, rebase conventions followed until the first push, and checks that take turns ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27), [05](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/05-repositories-and-job-branches.md)).
3. **Leaders on demand:** idle leaders stopped after the grace, and a leader's provider chosen at its start ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27), [02](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/02-daemon-and-store.md), [07](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/07-limits-holds-and-visibility.md)).
4. **Allowance, provider failures, lost sign-in and holds,** with fallback only before first dispatch and provider changes as the user's decisions ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27), [07](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/07-limits-holds-and-visibility.md)).
5. **Job pause, resume and cancel,** by command or through Coordination ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27), [07](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/07-limits-holds-and-visibility.md)).
6. **The no-CI declaration and the 15-minute wait** for a first check ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27), [06](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/06-validation-and-delivery.md)).
7. **The failed-validation limit** and the dispatch limit ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27), [06](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/06-validation-and-delivery.md), [07](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/07-limits-holds-and-visibility.md)).
8. **The disk floor,** disk use in status, and `asmai job clean` ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27), [07](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/07-limits-holds-and-visibility.md)).
9. **`asmai status` in full,** with `--check` ([07](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/07-limits-holds-and-visibility.md)).
10. **Two more small fixture repositories** Phillip owns, for the demo across three repositories ([answers](https://github.com/talvor/AssemblyAI/blob/main/.lavish/spec-doc-M5-answers.json)).

## Builds on

[M4 Conversation and intervention](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/milestones/M4-conversation-and-intervention.md): the status line and catch-up that show holds and queued work, and interventions.

## Rules delivered

Where a rule arrives in parts, the table names the part this milestone delivers.

**[01 Roles and decisions](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/01-roles-and-decisions.md)**

| Rule | | Part delivered here |
| --- | --- | --- |
| 4 | At most one leader process per role at any instant | leaders on demand |
| 40 | Pause and cancel | All |
| 41 | Kinds of decision the user always makes | provider changes |

**[02 Daemon and store](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/02-daemon-and-store.md)**

| Rule | | Part delivered here |
| --- | --- | --- |
| 12 | No factory-wide pause | All |
| 29 | What each dispatch records | token counts |
| 30 | Assignment states | queued and held |
| 52 | Stopping a leader | All |
| 53 | A leader's provider | All |

**[04 Conversation and Lavish](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/04-conversation-and-lavish.md)**

| Rule | | Part delivered here |
| --- | --- | --- |
| 11 | Acting on the user's word | All |
| 18 | A lost sign-in | All |

**[05 Repositories and job branches](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/05-repositories-and-job-branches.md)**

| Rule | | Part delivered here |
| --- | --- | --- |
| 11 | Checks that cannot run side by side | All |
| 12 | Disk | All |
| 20 | Workers resolve conflicts | All |
| 22 | Merge or rebase | All |
| 23 | Conflicts are ordinary work | All |
| 24 | Concurrent jobs in one repository | All |
| 25 | Outside commits | merging outside commits in |
| 42 | Kept until the job ends | All |
| 44 | Scratch workspaces | asmai job clean |

**[06 Validation and delivery](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/06-validation-and-delivery.md)**

| Rule | | Part delivered here |
| --- | --- | --- |
| 10 | The failed-validation limit | All |
| 18 | Outside commits refuse the push | a worker merging outside commits in |
| 30 | The declaration | All |
| 31 | Asked at setup | All |
| 32 | The wait for a first check | All |
| 36 | The user's own tools | All |

**[07 Limits, holds and visibility](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/07-limits-holds-and-visibility.md)**

| Rule | | Part delivered here |
| --- | --- | --- |
| 2 | Allowance is not budgeted per job | All |
| 3 | Recorded and shown | All |
| 4 | No reserve | All |
| 5 | A cap per provider | All |
| 6 | No other concurrency limit | All |
| 7 | The queue | All |
| 8 | No overflow | All |
| 10 | Fallback before first dispatch only | All |
| 11 | No suitable provider | All |
| 12 | After first dispatch, the user decides | All |
| 13 | A leader's provider | All |
| 14 | An approved replacement | All |
| 15 | Hold, then resume at the reset | All |
| 16 | Queued work | All |
| 17 | A leader with open work | All |
| 18 | A reported error resumes with backoff | All |
| 19 | Unavailable | All |
| 20 | A lost or expired sign-in | All |
| 21 | What a hold is | All |
| 22 | The holds in v1 | All |
| 23 | The dispatch limit | All |
| 24 | What counts | All |
| 25 | Side-effect-free retries | All |
| 26 | Failed validations | All |
| 27 | Who | All |
| 28 | Pause | All |
| 29 | Resume | All |
| 30 | Cancel | All |
| 34 | `asmai status` shows | caps, the queue, providers, holds and disk |
| 35 | `asmai status --check` | All |
| 36 | Periodic checks | All |
| 38 | No quotas | All |
| 39 | Disk use is reported | All |
| 40 | Cleaning | All |
| 41 | The free-space floor | All |

**[11 Qualification and proving](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/11-qualification-and-proving.md)**

| Rule | | Part delivered here |
| --- | --- | --- |
| 9 | Replay only what cannot be caused | All |

## Qualification cases

These pass in the harness on Linux at M5's end and have run on the Mac ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27), [11](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/11-qualification-and-proving.md)):

| Case | What is qualified |
| --- | --- |
| C26 | Expired or revoked sign-in holds work, shows the native sign-in command, and resumes when sign-in is back |
| C27 | Allowance used and reset times, for each provider |
| C28 | Allowance used up: agents hold, then resume at the reset (replayed) |
| C29 | A reported provider error resumes with backoff; past the bound the provider is unavailable |
| C30 | Fallback to the other provider only before first dispatch, including a leader's on-demand start; afterwards the user is asked |
| C31 | Leaders start when a message for their role arrives and stop after the idle grace |
| C32 | Below the free-space floor no new workspace is created |
| C38 | Concurrent jobs in one repository |
| C39 | Outside commits are merged in and never force-pushed over |
| C44 | The 15-minute wait for a first check, and the hold for a repository with no declared CI |

## Demo path

S5, S6 and S7, completed ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27), [00](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/00-overview.md)):

1. **Concurrent repositories:** a feature job runs while jobs run in two other repositories; a second job in the first repository meets a conflict that a worker resolves inside an assignment; full worker caps queue assignments, shown as queued, started first come first served, and never overflowing. It runs across three repositories: the fixture repository and two more small fixture repositories Phillip owns, added in M5 for this demo ([answers](https://github.com/talvor/AssemblyAI/blob/main/.lavish/spec-doc-M5-answers.json)).
2. **No CI:** a small change in a repository declared as having no CI, delivered with Quality's checks standing in, the gap stated in the pull request, and no wait and no hold.
3. **Pause, resume and cancel:** one job paused and resumed, and another cancelled, each leaving its reported state, which completes S7.

## Exit checks

M5 ends when ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27)):

- its tickets are closed;
- the development tests are green on Linux and on macOS;
- its qualification cases pass in the harness on Linux and have run on the Mac; a macOS failure becomes a ticket in M6 and does not hold up M5;
- its demo path has run once, with the terminal recording kept for Phillip to watch.

## Not in M5

Fencing, full reconciliation, orphan termination, crash and reboot recovery, draining on stop and the service (M6); remote hosts (M7).

## Sources

- [Choose the specification's structure and implementation sequence](https://github.com/talvor/AssemblyAI/issues/27#issuecomment-6004852593) (AssemblyAI#27)
- The component documents linked in Rules delivered, and the decision tickets they cite.
- The review of this document: [questions](https://github.com/talvor/AssemblyAI/blob/main/.lavish/spec-doc-M5-round1-questions.json) and [answers](https://github.com/talvor/AssemblyAI/blob/main/.lavish/spec-doc-M5-answers.json).
