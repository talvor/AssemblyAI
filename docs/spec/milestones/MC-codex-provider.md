# MC Codex provider

MC adds Codex as the second provider: Codex sessions and mixed staffing, Codex's installation and hook trust, Codex's skill delivery, and M1's cases again on Codex. M1 and M2 run on Claude Code alone ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27)).

MC has no number. It sits outside the M0 to M8 order so that it can be inserted at any time after M2, and later milestones keep their numbers whenever it is. Until it is inserted, the factory runs on Claude Code alone.

## What it adds

1. **Codex sessions and mixed staffing.** Any role's leader and workers can run on either provider, and one job can mix them ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27), [03](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/03-provider-sessions-and-terminals.md), [07](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/07-limits-holds-and-visibility.md)).
2. **Codex in setup:** `asmai providers install` fetches the pinned Codex, `asmai init` and `asmai doctor` check its sign-in, `asmai init` takes it through its hook trust review, and role staffing names a provider and a default model for each provider ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27), [09](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/09-cli-and-configuration.md), [M2](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/milestones/M2-skills.md)).
3. **Codex in the configuration file:** `[providers.codex]` and `"codex"` as a role's leader and worker provider, in `asmai config check|show|edit|apply` and `asmai role list|set` ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27), [09](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/09-cli-and-configuration.md)).
4. **Codex's skill delivery:** the list written into `.agents/skills/asmai-<name>/` of each workspace, hiding on Codex, and the repository's `.agents/skills` off by default ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27), [08](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/08-skills-and-agent-instructions.md)).
5. **The provider checks for Codex:** refusal of Codex versions that are not pinned, and a Codex CLI that upgraded itself holding its agent ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27), [03](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/03-provider-sessions-and-terminals.md)).
6. **M1's cases rerun on Codex** in the harness ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27)).

## Builds on

[M1 Walking skeleton](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/milestones/M1-walking-skeleton.md) and [M2 Skills](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/milestones/M2-skills.md). Codex's skill delivery writes the skill bundle that M2 delivers, and Codex joins the setup commands, the configuration fields and the checks that M2 completes. MC can be inserted at any point after M2 ends.

## What assumes Codex

Parts of M2, of M4 to M8 and of the case mapping were written with both providers present. M3, M6 and M7 assume nothing about Codex. The rest is below, with what is true while MC has not been inserted. This document does not decide what a milestone's exit then waits for: that is listed under Not decided here.

| Where | What assumes Codex | While MC is not inserted |
| --- | --- | --- |
| Case mapping ([00](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/00-overview.md), [11](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/11-qualification-and-proving.md) rule 24) | M1's cases run again on Codex; C35 passes | They have run on Claude Code only, and C35 has not passed |
| M2 | C2 and C33 depend on the provider | They pass with Claude Code; their Codex combinations have not run |
| [M4](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/milestones/M4-conversation-and-intervention.md) | C9 qualifies the attach client's rendering of each provider's screen | Only Claude Code's screen exists to render |
| [M5](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/milestones/M5-concurrency-and-limits.md) | C27 reports allowance for each provider; C30 falls back to the other provider; rules that choose between providers ([07](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/07-limits-holds-and-visibility.md) rules 5, 8, 10, 11 and 13, [02](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/02-daemon-and-store.md) rule 53, provider changes as decisions in [01](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/01-roles-and-decisions.md) rule 41) | C30 cannot run, there being no other provider; C27 has one provider to report |
| [M8](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/milestones/M8-release-and-upgrade.md) | C5, Codex hook trust surviving an upgrade; all 47 cases together on the candidate commit, C35 and M1's cases on Codex among them; the pins file, the qualification record and the offer of new pins at start, which name Codex | C5 cannot run and the 47 cannot all pass, so M8 cannot end |
| Proving scenarios ([11](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/11-qualification-and-proving.md) rule 29) | Each role runs at least once on Claude and once on Codex, and S1 mixes providers inside one job | They cannot be passed on Claude Code alone |

## Rules delivered

Where a rule arrives in parts, the table names the part this milestone delivers.

**[01 Roles and decisions](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/01-roles-and-decisions.md)**

| Rule | | Part delivered here |
| --- | --- | --- |
| 7 | What an assignment states | provider override |

**[02 Daemon and store](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/02-daemon-and-store.md)**

| Rule | | Part delivered here |
| --- | --- | --- |
| 6 | Checks before anything runs | setup checks, platform and provider refusals, for Codex |

**[03 Provider sessions and terminals](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/03-provider-sessions-and-terminals.md)**

| Rule | | Part delivered here |
| --- | --- | --- |
| 1 | Never the user's copies | Codex |
| 2 | Installed on the user's command | Codex |
| 4 | Only qualified combinations run | refusing versions that are not pinned, for Codex |
| 5 | A provider that updated itself | Codex |
| 7 | Checking readiness | Codex |
| 9 | Passed per session only | Codex |
| 12 | Native review is kept | Codex |
| 14 | Elsewhere | skills, for Codex |
| 15 | What runs without a prompt | Codex |

**[07 Limits, holds and visibility](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/07-limits-holds-and-visibility.md)**

| Rule | | Part delivered here |
| --- | --- | --- |
| 9 | Staffing | a provider for each role, and mixed staffing |

**[08 Skills and agent instructions](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/08-skills-and-agent-instructions.md)**

| Rule | | Part delivered here |
| --- | --- | --- |
| 19 | Agents see only their list | hiding on Codex |
| 21 | Codex | All |
| 25 | Repository skills | `.agents/skills` |

**[09 CLI and configuration](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/09-cli-and-configuration.md)**

| Rule | | Part delivered here |
| --- | --- | --- |
| 21 | `asmai init` | Codex in steps 2 to 5, including its hook trust review |
| 22 | `asmai doctor` | the same checks, for Codex |
| 23 | `asmai start` | the same checks, for Codex |
| 25 | One TOML file | Codex's fields |
| 31 | `asmai role list|set` | Codex as a provider |
| 32 | `asmai repo add` | Codex's fields |
| 33 | Every field | Codex's fields |
| 34 | An example | Codex's fields |

**[10 Release, install and upgrade](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/10-release-install-and-upgrade.md)**

| Rule | | Part delivered here |
| --- | --- | --- |
| 7 | Claude Code and Codex are not redistributed | Codex |

## Qualification cases

These pass in the harness on Linux at MC's end and have run on the Mac ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27), [11](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/11-qualification-and-proving.md)):

| Case | What is qualified |
| --- | --- |
| C35 | Codex finds the skills written into its workspace |
| C3, C4, C7, C11, C19, C36, C37, C41, C42, C43, C45 | M1's cases, again on Codex |

C5, Codex hook trust surviving an AsmAI upgrade, stays with M8, which owns upgrades. C35 first passes at MC's end, and M1's cases keep M1 as the milestone at whose end they first pass.

## Demo path

S1's skeleton with each role on either provider ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27)): M1's demo path on the fixture repository with the three roles staffed across both providers in one job, and Coordination, Engineering and Quality each running on Codex in at least one run and on Claude in at least one. Workers name the skills they ran, from their role's list.

## Exit checks

MC ends when ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27)):

- its tickets are closed;
- the development tests are green on Linux and on macOS;
- its qualification cases, and M1's again on Codex, pass in the harness on Linux and have run on the Mac; a macOS failure becomes a ticket in the next milestone and does not hold up MC;
- its demo path has run once on the fixture repository, with the terminal recording kept for Phillip to watch.

## Not in MC

Codex hook trust surviving an upgrade (C5, M8); everything else the numbered milestones deliver.

## Not decided here

These are the open questions that splitting MC out raises. The specification states what cannot run without MC and leaves each of these to the captain:

- If MC is inserted after M4 or M5, does that milestone's end wait for MC, or do C9, C27 and C30 pass there on Claude Code alone, with their Codex parts running at MC's end or with all 47 in M8?
- Does MC rerun C2 and C33 on Codex at its own end, or do their Codex combinations run only with all 47 in M8?
- May v1 be released without MC? As written it cannot: C5, C35, M1's cases on Codex and the proving scenarios need Codex, so MC has to be inserted before M8 can end.

## Sources

- [Choose the specification's structure and implementation sequence](https://github.com/talvor/AssemblyAI/issues/27#issuecomment-6004852593) (AssemblyAI#27)
- The component documents linked in Rules delivered, and the decision tickets they cite.
- The review of M2 Both providers and skills, from which MC was split: [board](https://github.com/talvor/AssemblyAI/blob/main/.lavish/spec-doc-M2.html) and [answers](https://github.com/talvor/AssemblyAI/blob/main/.lavish/spec-doc-M2-answers.json).
