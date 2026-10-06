# M1 Walking skeleton

M1 is the walking skeleton: on Claude only, one job travels from the user's request to a tested pull request on the fixture repository, end to end, through every layer it needs. Every later milestone widens it ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27)).

## What it adds

1. **The daemon, on Claude only:** `asmai start` and `stop`, the daemon, the store and its journal, daemon-owned terminals with hooks, nudges and `asmai inbox`, and attaching to the conversation ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27)).
2. **One job, end to end.** Coordination opens a job from the user's witnessed message and hands it to Engineering. One writing assignment works in a workspace of AsmAI's clone, and its acceptance fast-forwards the job branch. Quality validates the head. The daemon pushes, the Engineering leader opens a draft pull request, and the daemon watches CI and marks the pull request ready. Coordination reports the link ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27), [00](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/00-overview.md)).
3. **What the skeleton needs to run,** in minimal real forms that M2 completes: `asmai providers install` for Claude Code only, with its version in the pins file, `asmai repo add` to register the fixture repository, and the configuration file with only the fields M1 uses, namely Claude staffing for Coordination, Engineering and Quality and the fixture repository's entry. M2 adds Codex, `asmai init`, `doctor`, `config apply` and every other field ([answers](https://github.com/talvor/AssemblyAI/blob/main/.lavish/spec-doc-M1-answers.json)).
4. **Leaders start when work arrives.** From M1 the daemon starts a role's leader when a message for its role arrives (02 rule 51). Stopping idle leaders and a leader's choice of provider (02 rules 52 and 53) come in M5 ([answers](https://github.com/talvor/AssemblyAI/blob/main/.lavish/spec-doc-M1-answers.json)).
5. **The harness**, in its own directory of talvor/asmai and built only into development builds, running M1's cases with the real pinned Claude Code under the harness's OS user ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27), [11](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/11-qualification-and-proving.md)).

## Builds on

[M0 Groundwork](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/milestones/M0-groundwork.md): talvor/asmai, hosted CI with the fake provider, the fixture repository and the harness's OS users.

## Rules delivered

Where a rule arrives in parts, the table names the part this milestone delivers; later milestones deliver the rest.

**[01 Roles and decisions](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/01-roles-and-decisions.md)**

| Rule | | Part delivered here |
| --- | --- | --- |
| 1 | Five factory-wide roles | Coordination, Engineering and Quality |
| 2 | Roles are responsibilities, not stages | All |
| 3 | One leader per role | All |
| 4 | At most one leader process per role at any instant | one leader per role |
| 5 | What a leader does itself | All |
| 6 | One owner, one assignment | All |
| 7 | What an assignment states | outcome and acceptance criteria |
| 8 | Cross-role work | All |
| 9 | Results | All |
| 10 | Acceptance and rejection | All |
| 12 | What a handoff carries | All |
| 13 | Answering a handoff | All |
| 16 | Opening a job | All |
| 17 | The default mandate | a tested-PR job |
| 20 | Merging | All |
| 21 | Limits outside the mandate | All |
| 27 | Leaders may accept | All |
| 45 | What is witnessed | All |
| 46 | Attribution | a job opened from a witnessed message |
| 49 | Not a security boundary | All |

**[02 Daemon and store](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/02-daemon-and-store.md)**

| Rule | | Part delivered here |
| --- | --- | --- |
| 1 | One factory per user per host | All |
| 2 | The daemon owns the factory | All |
| 3 | No network listener | All |
| 4 | One executable | All |
| 5 | `asmai start` runs the daemon | All |
| 6 | Checks before anything runs | start runs the checks that exist |
| 7 | Every start is a recovery | restoring the leaders |
| 9 | `asmai stop` drains | stopping and persisting |
| 10 | What survives a stop | All |
| 11 | Continuing after a stop | continuing after a clean stop |
| 13 | The daemon is the only writer | All |
| 14 | Current state and the journal together | All |
| 15 | Kept in full | All |
| 16 | What is never recorded | All |
| 17 | Every record knows its job and role | All |
| 18 | Copies | asmai export |
| 19 | A job | repository jobs |
| 21 | The end of a job | All |
| 22 | Briefs are the leaders' context | All |
| 23 | A dispatch | All |
| 24 | Dispatch states | All |
| 25 | Only current evidence counts | All |
| 26 | No inference from silence | All |
| 29 | What each dispatch records | the transcript location |
| 30 | Assignment states | active, submitted, accepted, rejected and cancelled |
| 33 | A durable inbox | All |
| 34 | Content never travels through the terminal | All |
| 35 | The fetch is the evidence | All |
| 36 | Nudges may repeat | All |
| 37 | No boundary, no nudge | waiting for a boundary |
| 38 | Identity | All |
| 42 | Recorded as they happen | All |
| 43 | Leaders and the daemon record theirs too | All |
| 44 | Evidence, not proof | the ledger |
| 45 | No exactly-once claim | All |
| 50 | Coordination always runs | All |
| 51 | Starting a leader | starting a leader when a message for its role arrives |

**[03 Provider sessions and terminals](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/03-provider-sessions-and-terminals.md)**

| Rule | | Part delivered here |
| --- | --- | --- |
| 1 | Never the user's copies | Claude Code |
| 2 | Installed on the user's command | Claude Code, and the pins file |
| 6 | Subscription only | All |
| 8 | No API keys in sessions | All |
| 9 | Passed per session only | Claude Code |
| 10 | The user's provider configuration is never written | All |
| 11 | `asmai` is allowed | All |
| 12 | Native review is kept | Claude Code |
| 14 | Elsewhere | repository configuration and write guards |
| 15 | What runs without a prompt | Claude Code |
| 16 | Unmodified interactive CLIs | All |
| 17 | Terminal emulation is AsmAI's | rendering for attach |
| 18 | Hook intake | All |
| 19 | Separate states | All |
| 20 | Missing signals | the safe default |
| 21 | One input owner | All |
| 22 | Typing only at a known boundary | All |
| 23 | Positive submission acknowledgment | All |
| 26 | Witnessed messages | All |
| 27 | Attaching observes | All |
| 28 | The client draws the screen | drawing the screen |
| 44 | Transcripts stay put | All |
| 45 | The same-user terminal relay, the agent | All |

**[04 Conversation and Lavish](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/04-conversation-and-lavish.md)**

| Rule | | Part delivered here |
| --- | --- | --- |
| 1 | Coordination's terminal | All |
| 2 | Not an intervention | All |
| 3 | Delivery never waits for the user | All |

**[05 Repositories and job branches](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/05-repositories-and-job-branches.md)**

| Rule | | Part delivered here |
| --- | --- | --- |
| 1 | Registered repositories only | All |
| 2 | What registration records | All |
| 3 | Listing and removing | All |
| 5 | Never the user's checkout | All |
| 6 | The daemon owns them | All |
| 7 | Writing and read-only | a writing assignment, and Quality's read-only one |
| 9 | Staying inside | All |
| 10 | Slots | All |
| 13 | One per repository job | All |
| 14 | Branch names | All |
| 15 | One writer per branch | All |
| 17 | Workers take in the tip | All |
| 18 | Fast-forward on acceptance | All |
| 21 | Taking in the base | All |
| 25 | Outside commits | refusing a push over outside commits |
| 26 | Assignment branches are pushed | All |
| 27 | Part of every mandate | All |
| 28 | Kept until the user deletes them | All |
| 33 | One read-only view per repository job | All |
| 34 | Instruction files apply | instruction files |
| 35 | Provider configuration does not | All |
| 36 | Loading instruction files | All |
| 37 | Never wider than the mandate | All |
| 38 | The user's identity | All |
| 39 | Trailers | All |
| 40 | Writing workspaces | All |
| 43 | At the end of a job | All |

**[06 Validation and delivery](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/06-validation-and-delivery.md)**

| Rule | | Part delivered here |
| --- | --- | --- |
| 1 | Engineering tests its own work | All |
| 2 | Quality validates independently | All |
| 3 | Quality never fixes | All |
| 5 | When | validation of the finished job branch |
| 8 | Three kinds | the three kinds, and blocking findings |
| 11 | The five conditions | All |
| 13 | Where the evidence lives | All |
| 14 | A fixed order | All |
| 15 | Engineering owns code delivery | All |
| 17 | The daemon pushes | All |
| 18 | Outside commits refuse the push | the refusal |
| 19 | When | All |
| 20 | Repository instructions never decide the push | All |
| 21 | The leader opens it | All |
| 22 | Draft first | All |
| 23 | Workers write their part | the PR section |
| 24 | The leader composes the whole | All |
| 25 | The body | All |
| 26 | The daemon watches CI | All |
| 27 | Green | All |
| 28 | Red | All |
| 29 | An empty list is not green | All |
| 33 | AsmAI never merges in v1 | All |
| 34 | A code job ends at delivery | All |
| 35 | Afterwards is a follow-up | All |

**[07 Limits, holds and visibility](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/07-limits-holds-and-visibility.md)**

| Rule | | Part delivered here |
| --- | --- | --- |
| 34 | `asmai status` shows | the daemon, its version and the leaders |
| 42 | The daemon's log | All |
| 43 | Elsewhere | All |

**[08 Skills and agent instructions](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/08-skills-and-agent-instructions.md)**

| Rule | | Part delivered here |
| --- | --- | --- |
| 37 | Required content, not wording | Coordination's, Engineering's and Quality's instructions for the skeleton |
| 38 | The PR section in a writing worker's result | All |

**[09 CLI and configuration](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/09-cli-and-configuration.md)**

| Rule | | Part delivered here |
| --- | --- | --- |
| 1 | `asmai` everywhere | All |
| 4 | The same executable | All |
| 5 | Agent callers | All |
| 7 | Everyday actions are top-level verbs; setup is grouped by noun | each command arrives with the milestone of the rule it serves |
| 8 | Agents run only coordination commands | All |
| 9 | The daemon checks every call | All |
| 10 | The agent commands | All |
| 11 | For agents | All |
| 12 | For the user | All |
| 13 | `--json` | All |
| 14 | Agents are addressed `name@role` | All |
| 15 | Worker numbers | All |
| 16 | A bare role name | All |
| 17 | Jobs are addressed by number | All |
| 25 | One TOML file | the file and the fields M1 uses |
| 32 | `asmai repo add` | the file and the fields M1 uses |
| 33 | Every field | the file and the fields M1 uses |
| 34 | An example | the file and the fields M1 uses |
| 35 | Variables AsmAI reads or sets | ASMAI_SLOT and TMPDIR |

**[11 Qualification and proving](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/11-qualification-and-proving.md)**

| Rule | | Part delivered here |
| --- | --- | --- |
| 6 | Real providers on a real host | the harness |
| 7 | Where it lives | All |
| 8 | Faults are injected | each milestone adds the faults its cases need |
| 12 | Per combination or per platform | All |
| 13 | What passes | All |
| 14 | What fails | All |
| 15 | Who and when | All |
| 16 | Never in hosted CI, and no command | All |
| 18 | macOS alongside | All |
| 24 | All 47 are the v1 qualification cases | each milestone passes its own cases |

## Qualification cases

These pass in the harness on Linux at M1's end and have run on the Mac ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27), [11](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/11-qualification-and-proving.md)):

| Case | What is qualified |
| --- | --- |
| C3 | The pinned provider copies reuse the user's existing sign-in without a new login |
| C4 | Every agent session starts without provider API-key variables |
| C7 | Positive acknowledgment of each automated submission, never inferred from a successful PTY write |
| C11 | Capturing witnessed messages and telling them apart from the daemon's nudges |
| C19 | Dispatches and results stay correlated and reconcilable across restarts |
| C36 | Instruction files load without the repository's provider configuration |
| C37 | Provider write guards are switched on |
| C41 | The daemon's push, and its refusal when origin holds commits AsmAI did not make |
| C42 | A draft pull request, and the "[not ready]" fallback when GitHub refuses a draft |
| C43 | CI watched through gh: green; red with one judged re-run; a newer push replacing the wait |
| C45 | Marking the pull request ready when CI is green |

## Demo path

A tested pull request on the fixture repository, end to end ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27)):

1. The user opens the conversation with `asmai` and asks Coordination for a small change to the fixture repository.
2. Coordination opens a job from that witnessed message, with its mandate and acceptance criteria, and hands it to Engineering.
3. The Engineering leader assigns one writing assignment; the worker tests and commits on its assignment branch and submits; the leader accepts, and the daemon fast-forwards the job branch.
4. Engineering hands validation to Quality; a Quality worker validates the exact head and reports no blocking finding.
5. The Engineering leader asks for the push with `asmai push`, the daemon pushes, and the leader opens a draft pull request with the AsmAI section and records it as an effect.
6. The daemon watches CI on the head, marks the pull request ready when it is green, and Coordination reports the link. The job ends.

The demo is recorded with an ordinary terminal recorder running in the demo terminal, as every milestone's demo is; AsmAI's own per-dispatch recordings arrive in M4 ([answers](https://github.com/talvor/AssemblyAI/blob/main/.lavish/spec-doc-M1-answers.json)).

## Exit checks

M1 ends when ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27)):

- its tickets are closed;
- the development tests are green on Linux and on macOS;
- its qualification cases pass in the harness on Linux and have run on the Mac; a macOS failure becomes a ticket in M2 and does not hold up M1;
- its demo path has run once on the fixture repository, with the terminal recording kept for Phillip to watch.

## Not in M1

Codex, skills, `asmai init` and `doctor` (M2); decision requests, Lavish, Planning and Research (M3); the status line, catch-up and intervention (M4); caps, limits, holds and concurrent jobs (M5); fencing, full reconciliation and the service (M6); remote hosts (M7); releases and upgrades (M8).

## Sources

- [Choose the specification's structure and implementation sequence](https://github.com/talvor/AssemblyAI/issues/27#issuecomment-6004852593) (AssemblyAI#27)
- The component documents linked in Rules delivered, and the decision tickets they cite.
- The review of this document: [questions](https://github.com/talvor/AssemblyAI/blob/main/.lavish/spec-doc-M1-round1-questions.json) and [answers](https://github.com/talvor/AssemblyAI/blob/main/.lavish/spec-doc-M1-answers.json).
