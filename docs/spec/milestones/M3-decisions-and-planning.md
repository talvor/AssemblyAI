# M3 Decisions and planning

M3 brings the user into the factory's decisions and adds the roles and kinds of job that need them: decision requests, answer surfaces and grants; the Lavish server, its rendering of requests and its collection of answers; the Planning and Research roles; notes delivery; jobs without a repository; and several assignments per job. It passes no new qualification case: the proving scenarios S3 and S7 prove these rules ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27)).

## What it adds

1. **Decisions:** versioned decision requests, answer surfaces, witnessed-message attribution of answers and grants, delegated decision records, and reuse of recorded decisions at skills' human steps ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27), [01](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/01-roles-and-decisions.md), [08](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/08-skills-and-agent-instructions.md)).
2. **The Lavish build and server:** the first Lavish build and the workflow that makes one whenever the Lavish pin moves, the pinned Lavish build installed by `asmai providers install`, and the Lavish server rendering decision requests and collecting answers ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27), [04](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/04-conversation-and-lavish.md), [03](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/03-provider-sessions-and-terminals.md)).
3. **The Planning and Research roles,** with their skills, including grilling and Wayfinder questions reaching the user in Lavish ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27), [01](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/01-roles-and-decisions.md), [08](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/08-skills-and-agent-instructions.md)).
4. **Notes delivery,** including notes pull requests and repository setup for a newly added repository ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27), [05](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/05-repositories-and-job-branches.md), [06](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/06-validation-and-delivery.md), [08](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/08-skills-and-agent-instructions.md)).
5. **Jobs without a repository,** in scratch workspaces ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27), [05](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/05-repositories-and-job-branches.md)).
6. **Several assignments per job,** with fixes after blocking findings or red CI, re-validation after later changes, a moved job branch returning work to its worker, and follow-up jobs ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27), [06](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/06-validation-and-delivery.md), [05](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/05-repositories-and-job-branches.md)).

## Builds on

[M2 Both providers and skills](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/milestones/M2-both-providers-and-skills.md): both providers, the configuration, and the skill bundle with its operating guide.

## Rules delivered

Where a rule arrives in parts, the table names the part this milestone delivers.

**[01 Roles and decisions](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/01-roles-and-decisions.md)**

| Rule | | Part delivered here |
| --- | --- | --- |
| 1 | Five factory-wide roles | Planning and Research |
| 11 | Reusing a session | All |
| 14 | Disagreements | All |
| 15 | Changes of scope | All |
| 17 | The default mandate | planning-only and research-only jobs |
| 18 | What a mandate never covers without a grant | All |
| 19 | Spending | All |
| 22 | Ask the user whenever more than one distinct viable approach remains | All |
| 23 | What counts as distinct | All |
| 24 | Settled routes continue | All |
| 25 | Recording decisions | All |
| 26 | Passing decisions on | All |
| 28 | Genuine human gates | All |
| 30 | What a grant records | All |
| 31 | Scope | All |
| 32 | Reuse | All |
| 33 | Skills' human steps | All |
| 34 | Revocation and changed context | All |
| 35 | Routing | All |
| 36 | Ownership of a question | All |
| 37 | Versions | All |
| 38 | Answers match versions | All |
| 39 | While an answer is pending | All |
| 41 | Kinds of decision the user always makes | needs-you and disputed findings, anything outside the mandate |
| 42 | One answer surface per version | All |
| 43 | Which surface | All |
| 44 | Listing is not answering | All |
| 46 | Attribution | answers and grants |
| 47 | Reading and words together | All |
| 48 | Refusals | All |

**[02 Daemon and store](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/02-daemon-and-store.md)**

| Rule | | Part delivered here |
| --- | --- | --- |
| 19 | A job | jobs without a repository |
| 20 | Follow-ups | All |
| 31 | A moved job branch is not a rejection | All |

**[03 Provider sessions and terminals](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/03-provider-sessions-and-terminals.md)**

| Rule | | Part delivered here |
| --- | --- | --- |
| 1 | Never the user's copies | Lavish |
| 2 | Installed on the user's command | Lavish |
| 3 | Lavish needs no Node | All |

**[04 Conversation and Lavish](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/04-conversation-and-lavish.md)**

| Rule | | Part delivered here |
| --- | --- | --- |
| 9 | Escalated once | presenting a decision once |
| 10 | Answering here | All |
| 20 | The daemon runs it | All |
| 21 | Local only | localhost, the URL and the forwarding command |
| 22 | No agent runs Lavish | All |
| 23 | Structured questions | All |
| 24 | One standard layout | All |
| 25 | The agent's own content | All |
| 26 | A new version, a new page | All |
| 27 | The daemon collects | All |
| 28 | Routing | All |
| 29 | Partly answered pages | All |

**[05 Repositories and job branches](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/05-repositories-and-job-branches.md)**

| Rule | | Part delivered here |
| --- | --- | --- |
| 4 | Setup on registration | All |
| 8 | No repository | All |
| 16 | One open job per job branch | All |
| 19 | A moved tip | All |
| 29 | Not copied from the tracker | All |
| 30 | Other notes go on the job branch | All |
| 31 | Prototypes stay on their branch | All |
| 32 | Notes deliver like code | All |
| 44 | Scratch workspaces | keeping scratch workspaces |

**[06 Validation and delivery](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/06-validation-and-delivery.md)**

| Rule | | Part delivered here |
| --- | --- | --- |
| 5 | When | an earlier review on request |
| 6 | After a later change | All |
| 7 | No tests at all | All |
| 8 | Three kinds | needs-you findings |
| 9 | Clearing a blocking finding | All |
| 12 | Evidence goes stale | All |
| 16 | Notes are delivered by their own leader | All |
| 37 | No validation unless asked | All |
| 38 | A notes pull request | All |
| 39 | A job without a repository | All |

**[07 Limits, holds and visibility](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/07-limits-holds-and-visibility.md)**

| Rule | | Part delivered here |
| --- | --- | --- |
| 1 | No spending without a grant | All |

**[08 Skills and agent instructions](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/08-skills-and-agent-instructions.md)**

| Rule | | Part delivered here |
| --- | --- | --- |
| 9 | Grilling and Wayfinder questions | All |
| 14 | User-invoked skills | All |
| 15 | Questions reach the user through the leader | All |
| 18 | Short notes bodies | All |
| 27 | Where the setup lives | All |
| 28 | When it runs | All |
| 29 | How it runs | All |
| 30 | Answers apply at once | All |
| 31 | CI | All |
| 32 | Which steps | All |
| 33 | Satisfied from the records | All |
| 34 | Through the owning leader | All |
| 35 | Uncovered steps | All |
| 36 | Grilling and Wayfinder | All |
| 37 | Required content, not wording | Planning's and Research's instructions, and decisions |

**[10 Release, install and upgrade](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/10-release-install-and-upgrade.md)**

| Rule | | Part delivered here |
| --- | --- | --- |
| 4 | Notices travel inside the executable | a Lavish build's notices |
| 5 | A license allow-list | everything compiled into a Lavish build |
| 7 | Claude Code and Codex are not redistributed | Lavish |
| 10 | The build | Lavish builds |

## Qualification cases

None new ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27)). The proving scenarios S3 and S7 prove M3's rules. Each milestone runs only its own cases, and all 47 run together in M8, so M3 has no harness check ([answers](https://github.com/talvor/AssemblyAI/blob/main/.lavish/spec-doc-M3-answers.json)).

## Demo path

The full S1 path, S2, S3 and S4, on the fixture repository ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27), [11](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/11-qualification-and-proving.md)):

1. **Feature to tested PR:** a feature request whose Planning questions reach the user in Lavish, with a specification and tickets in the fixture repository's tracker, several Engineering assignments, Quality's validation at the exact head, and a tested pull request.
2. **Research:** a research job delivered as notes with their sources, once as a notes pull request and once without a repository.
3. **Planning:** a Wayfinder ticket in the fixture repository's tracker resolved with the user in Lavish, its resolution recorded there.
4. **Diagnosis:** a defect in the fixture repository reproduced, diagnosed, and fixed as a tested pull request.

Along the way, one choice between distinct viable approaches is answered in the conversation and one request with several questions in Lavish.

## Exit checks

M3 ends when ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27)):

- its tickets are closed;
- the development tests are green on Linux and on macOS;
- its demo path has run once on the fixture repository, with the terminal recording kept for Phillip to watch.

## Not in M3

The status line keeping decisions visible, the focused job and the catch-up (M4); provider changes as decisions and job pause and cancel (M5).

## Sources

- [Choose the specification's structure and implementation sequence](https://github.com/talvor/AssemblyAI/issues/27#issuecomment-6004852593) (AssemblyAI#27)
- The component documents linked in Rules delivered, and the decision tickets they cite.
- The review of this document: [questions](https://github.com/talvor/AssemblyAI/blob/main/.lavish/spec-doc-M3-round1-questions.json) and [answers](https://github.com/talvor/AssemblyAI/blob/main/.lavish/spec-doc-M3-answers.json).
