# M2 Both providers and skills

M2 widens the walking skeleton to both providers and gives agents their skills: Codex sessions and mixed staffing, the setup commands and the full configuration file, the skill bundle with its per-session delivery and hiding, and platform certification checks. M1's cases run again on Codex ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27)).

## What it adds

1. **Codex sessions and mixed staffing.** Any role's leader and workers can run on either provider, and one job can mix them ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27), [03](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/03-provider-sessions-and-terminals.md), [07](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/07-limits-holds-and-visibility.md)).
2. **Setup:** `asmai providers install` for every pinned provider, `asmai init` and `asmai doctor`, completing the minimal forms M1 built ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27), [09](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/09-cli-and-configuration.md), [M1](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/milestones/M1-walking-skeleton.md)).
3. **The configuration file** with every field, `asmai config check|show|edit|apply` and `asmai role list|set` ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27), [09](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/09-cli-and-configuration.md)).
4. **The skill bundle,** the operating guide, the skill lists and leaders' indexes, per-session delivery to each provider, and hiding everything else ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27), [08](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/08-skills-and-agent-instructions.md)).
5. **Platform certification checks** at init, doctor and start, and refusal of provider versions that are not pinned ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27), [03](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/03-provider-sessions-and-terminals.md)).
6. **M1's cases rerun on Codex** in the harness ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27)).

## Builds on

[M1 Walking skeleton](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/milestones/M1-walking-skeleton.md): the daemon, the store, Claude sessions and the end-to-end path to a tested pull request.

## Rules delivered

Where a rule arrives in parts, the table names the part this milestone delivers.

**[01 Roles and decisions](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/01-roles-and-decisions.md)**

| Rule | | Part delivered here |
| --- | --- | --- |
| 7 | What an assignment states | named skill, narrowed list, provider override |

**[02 Daemon and store](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/02-daemon-and-store.md)**

| Rule | | Part delivered here |
| --- | --- | --- |
| 6 | Checks before anything runs | setup checks, platform and provider refusals |
| 29 | What each dispatch records | the bundle version and skill fingerprints |

**[03 Provider sessions and terminals](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/03-provider-sessions-and-terminals.md)**

| Rule | | Part delivered here |
| --- | --- | --- |
| 1 | Never the user's copies | Codex |
| 2 | Installed on the user's command | Codex |
| 3 | Node | All |
| 4 | Only qualified combinations run | refusing versions that are not pinned |
| 5 | A provider that updated itself | All |
| 7 | Checking readiness | All |
| 9 | Passed per session only | Codex |
| 12 | Native review is kept | Codex |
| 14 | Elsewhere | skills |
| 15 | What runs without a prompt | Codex |

**[05 Repositories and job branches](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/05-repositories-and-job-branches.md)**

| Rule | | Part delivered here |
| --- | --- | --- |
| 34 | Instruction files apply | the user's notes in the configuration |
| 39 | Trailers | the per-repository switch |

**[06 Validation and delivery](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/06-validation-and-delivery.md)**

| Rule | | Part delivered here |
| --- | --- | --- |
| 4 | Never a self-review | All |
| 23 | Workers write their part | the pr skill's form |

**[07 Limits, holds and visibility](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/07-limits-holds-and-visibility.md)**

| Rule | | Part delivered here |
| --- | --- | --- |
| 9 | Staffing | All |

**[08 Skills and agent instructions](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/08-skills-and-agent-instructions.md)**

| Rule | | Part delivered here |
| --- | --- | --- |
| 1 | Bundled and pinned | All |
| 2 | Contents | All |
| 3 | Not shipped | All |
| 4 | Updates come with releases | All |
| 6 | Upstream text plus one guide | All |
| 7 | The mappings | All |
| 8 | Only the skill list | All |
| 10 | Patches are the exception | All |
| 11 | Workers run the skills, in every role | All |
| 12 | Leaders get an index | All |
| 13 | Narrowing | All |
| 16 | The lists | All |
| 17 | Optional skills | All |
| 19 | Agents see only their list | All |
| 20 | Claude Code | All |
| 21 | Codex | All |
| 22 | Names across providers | All |
| 23 | Added skills | All |
| 24 | Copied at start | All |
| 25 | Repository skills | All |
| 26 | No other way in | All |
| 37 | Required content, not wording | the operating guide |
| 39 | A leader's skill index | All |

**[09 CLI and configuration](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/09-cli-and-configuration.md)**

| Rule | | Part delivered here |
| --- | --- | --- |
| 21 | `asmai init` | All |
| 22 | `asmai doctor` | All |
| 23 | `asmai start` | All |
| 25 | One TOML file | every field |
| 26 | Only the user changes it | All |
| 27 | `asmai config check` | All |
| 28 | `asmai config apply` | All |
| 29 | Journaled | All |
| 31 | `asmai role list|set` | All |
| 32 | `asmai repo add` | every field |
| 33 | Every field | every field |
| 34 | An example | every field |

**[10 Release, install and upgrade](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/10-release-install-and-upgrade.md)**

| Rule | | Part delivered here |
| --- | --- | --- |
| 7 | Providers are not redistributed | All |

## Qualification cases

These pass in the harness on Linux at M2's end and have run on the Mac, and M1's cases pass again with Codex ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27), [11](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/11-qualification-and-proving.md)):

| Case | What is qualified |
| --- | --- |
| C1 | Platform certification on Linux and on macOS; an uncertified platform refuses to start agents and says what to do |
| C2 | An unqualified provider version is refused before any dispatch; a provider CLI that upgraded itself holds its agent at the next restart |
| C33 | Personal, provider built-in and repository skills are hidden, including Claude's built-in code-review next to the shipped one |
| C34 | Per-session skill delivery works although Claude namespaces plugin skills and upstream skills call each other by bare name |
| C35 | Codex finds the skills written into its workspace |
| C3, C4, C7, C11, C19, C36, C37, C41, C42, C43, C45 | M1's cases, again on Codex |

## Demo path

S1's skeleton with each role on either provider ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27)): a new host set up with `asmai init`, then M1's demo path on the fixture repository with the three roles staffed across both providers in one job, and Coordination, Engineering and Quality each running on Codex in at least one run and on Claude in at least one. Workers name the skills they ran, from their role's list.

## Exit checks

M2 ends when ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27)):

- its tickets are closed;
- the development tests are green on Linux and on macOS;
- its qualification cases, and M1's again on Codex, pass in the harness on Linux and have run on the Mac; a macOS failure becomes a ticket in M3 and does not hold up M2;
- its demo path has run once on the fixture repository, with the terminal recording kept for Phillip to watch.

## Not in M2

Repository setup and every rule that asks the user a question (M3, with decision requests); `asmai doctor`'s list of what changed in the skills after an upgrade, and the qualification record that `asmai start` enforces (M8).

## Sources

- [Choose the specification's structure and implementation sequence](https://github.com/talvor/AssemblyAI/issues/27#issuecomment-6004852593) (AssemblyAI#27)
- The component documents linked in Rules delivered, and the decision tickets they cite.
- The review of this document: [board](https://github.com/talvor/AssemblyAI/blob/main/.lavish/spec-doc-M2.html) and [answers](https://github.com/talvor/AssemblyAI/blob/main/.lavish/spec-doc-M2-answers.json).
