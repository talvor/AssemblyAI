# M2 Skills

M2 gives agents their skills on the walking skeleton, which runs on Claude Code: the setup commands and the full configuration file, the skill bundle with its per-session delivery and hiding, and platform certification checks. Codex sessions, mixed staffing and Codex's skill delivery are not here: they are [MC Codex provider](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/milestones/MC-codex-provider.md), which sits outside the M0 to M8 order so that it can be inserted at any time after M2 without renumbering anything ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27)).

## What it adds

1. **Setup:** `asmai init` and `asmai doctor`, completing the minimal forms M1 built; `asmai providers install` stays as M1 built it, for Claude Code (Codex comes with MC and the pinned Lavish with the Lavish server in M3) ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27), [09](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/09-cli-and-configuration.md), [M1](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/milestones/M1-walking-skeleton.md)).
2. **The configuration file** with every field except the ones that name Codex (`[providers.codex]` and `"codex"` as a role's provider), `asmai config check|show|edit|apply` and `asmai role list|set` ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27), [09](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/09-cli-and-configuration.md)).
3. **The skill bundle,** the operating guide, the skill lists and leaders' indexes, per-session delivery to Claude Code, and hiding everything else from it ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27), [08](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/08-skills-and-agent-instructions.md)).
4. **Platform certification checks** at init, doctor and start, and refusal of Claude Code versions that are not pinned ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27), [03](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/03-provider-sessions-and-terminals.md)).

## Builds on

[M1 Walking skeleton](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/milestones/M1-walking-skeleton.md): the daemon, the store, Claude sessions and the end-to-end path to a tested pull request.

## Rules delivered

Where a rule arrives in parts, the table names the part this milestone delivers.

**[01 Roles and decisions](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/01-roles-and-decisions.md)**

| Rule | | Part delivered here |
| --- | --- | --- |
| 7 | What an assignment states | named skill, narrowed list |

**[02 Daemon and store](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/02-daemon-and-store.md)**

| Rule | | Part delivered here |
| --- | --- | --- |
| 6 | Checks before anything runs | setup checks, platform and provider refusals, for Claude Code |
| 29 | What each dispatch records | the bundle version and skill fingerprints |

**[03 Provider sessions and terminals](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/03-provider-sessions-and-terminals.md)**

| Rule | | Part delivered here |
| --- | --- | --- |
| 4 | Only qualified combinations run | refusing versions that are not pinned, for Claude Code |
| 5 | A provider that updated itself | Claude Code |
| 7 | Checking readiness | Claude Code |
| 14 | Elsewhere | skills, for Claude Code |

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
| 9 | Staffing | a provider and model for each role, on Claude Code |

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
| 19 | Agents see only their list | hiding on Claude Code |
| 20 | Claude Code | All |
| 22 | Names across providers | All |
| 23 | Added skills | All |
| 24 | Copied at start | All |
| 25 | Repository skills | `.claude/skills` |
| 26 | No other way in | All |
| 37 | Required content, not wording | the operating guide |
| 39 | A leader's skill index | All |

**[09 CLI and configuration](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/09-cli-and-configuration.md)**

| Rule | | Part delivered here |
| --- | --- | --- |
| 21 | `asmai init` | every step, for Claude Code only |
| 22 | `asmai doctor` | the same checks, for Claude Code only |
| 23 | `asmai start` | the same checks, for Claude Code only |
| 25 | One TOML file | every field except Codex's |
| 26 | Only the user changes it | All |
| 27 | `asmai config check` | All |
| 28 | `asmai config apply` | All |
| 29 | Journaled | All |
| 31 | `asmai role list|set` | All, for Claude Code only |
| 32 | `asmai repo add` | every field except Codex's |
| 33 | Every field | every field except Codex's |
| 34 | An example | every field except Codex's |

**[10 Release, install and upgrade](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/10-release-install-and-upgrade.md)**

| Rule | | Part delivered here |
| --- | --- | --- |
| 7 | Claude Code and Codex are not redistributed | Claude Code |

## Qualification cases

These pass in the harness on Linux at M2's end and have run on the Mac ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27), [11](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/11-qualification-and-proving.md)):

| Case | What is qualified |
| --- | --- |
| C1 | Platform certification on Linux and on macOS; an uncertified platform refuses to start agents and says what to do |
| C2 | An unqualified provider version is refused before any dispatch; a provider CLI that upgraded itself holds its agent at the next restart |
| C33 | Personal, provider built-in and repository skills are hidden, including Claude's built-in code-review next to the shipped one |
| C34 | Per-session skill delivery works although Claude namespaces plugin skills and upstream skills call each other by bare name |

C2 and C33 depend on the provider, and M2 runs them with the pinned Claude Code, the only provider the skeleton has. Their Codex combinations run when Codex exists, with all 47 in M8 at the latest (11 rule 12). C35, Codex finding the skills written into its workspace, is [MC's](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/milestones/MC-codex-provider.md).

## Demo path

S1's skeleton with the skill bundle ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27)): a new host set up with `asmai init`, then M1's demo path on the fixture repository with the three roles on Claude Code. Workers name the skills they ran, from their role's list.

## Exit checks

M2 ends when ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27)):

- its tickets are closed;
- the development tests are green on Linux and on macOS;
- its qualification cases pass in the harness on Linux and have run on the Mac; a macOS failure becomes a ticket in the next milestone, which is M3 unless MC has been inserted first, and does not hold up M2;
- its demo path has run once on the fixture repository, with the terminal recording kept for Phillip to watch.

## Not in M2

Codex sessions, mixed staffing, Codex's skill delivery and M1's cases again on Codex ([MC](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/milestones/MC-codex-provider.md)); repository setup and every rule that asks the user a question (M3, with decision requests); `asmai doctor`'s list of what changed in the skills after an upgrade, and the qualification record that `asmai start` enforces (M8).

## Sources

- [Choose the specification's structure and implementation sequence](https://github.com/talvor/AssemblyAI/issues/27#issuecomment-6004852593) (AssemblyAI#27)
- The component documents linked in Rules delivered, and the decision tickets they cite.
- The review of this document before Codex was split out as MC: [board](https://github.com/talvor/AssemblyAI/blob/main/.lavish/spec-doc-M2.html) and [answers](https://github.com/talvor/AssemblyAI/blob/main/.lavish/spec-doc-M2-answers.json).
