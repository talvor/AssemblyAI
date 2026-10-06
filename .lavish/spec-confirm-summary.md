# The v1 specification, for confirmation

All 21 documents are accepted on their own boards and committed on the branch `fm/asmai-v1-spec`. Confirming the whole lets me push the branch and open the pull request to talvor/AssemblyAI, for you to review and merge. Once merged, the specification is the authority for implementation until v1.0.0.

## The documents

| Document | Accepted with |
| --- | --- |
| [00 Overview](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/00-overview.md) | S7 first possible at M5; "the user" in the rules, "Phillip" only where a decision is about you; the Engineering leader opens M1's draft PR |
| [01 Roles and decisions](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/01-roles-and-decisions.md) | A grant is given in words and recorded by a leader with `asmai decision record`, citing them |
| [02 Daemon and store](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/02-daemon-and-store.md) | After a clean stop, workers resume on the same provider with an uncounted dispatch |
| [03 Provider sessions and terminals](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/03-provider-sessions-and-terminals.md) | Agents run inside the provider's write guard; allowed commands, including git and gh, need no prompt |
| [04 Conversation and Lavish](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/04-conversation-and-lavish.md) | A partly answered Lavish page is routed at once and stays pending |
| [05 Repositories and job branches](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/05-repositories-and-job-branches.md) | Rebase only until the first push, never forced; `asmai turn` for one-at-a-time checks; `asmai/job-<n>-<slug>` branch names |
| [06 Validation and delivery](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/06-validation-and-delivery.md) | Notes PRs follow the draft-then-ready cycle; `asmai push <job>`; the no-CI declaration lives only in the configuration |
| [07 Limits, holds and visibility](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/07-limits-holds-and-visibility.md) | Fallback uses one default model per provider, for any role |
| [08 Skills and agent instructions](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/08-skills-and-agent-instructions.md) | Coordination delivers a repository-setup PR like a notes job |
| [09 CLI and configuration](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/09-cli-and-configuration.md) | The configuration's field names and layout as drafted |
| [10 Release, install and upgrade](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/10-release-install-and-upgrade.md) | As drafted |
| [11 Qualification and proving](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/11-qualification-and-proving.md) | AsmAI's next map, for S3, lives in talvor/asmai |
| [M0 Groundwork](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/milestones/M0-groundwork.md) | You create talvor/asmai and set up its tracker by hand before running to-tickets |
| [M1 Walking skeleton](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/milestones/M1-walking-skeleton.md) | Minimal real forms of provider install, repo add and the configuration; leaders start when work arrives; demos recorded with a terminal recorder |
| [M2 Both providers and skills](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/milestones/M2-both-providers-and-skills.md) | As drafted |
| [M3 Decisions and planning](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/milestones/M3-decisions-and-planning.md) | Each milestone runs only its own cases; all 47 together in M8 |
| [M4 Conversation and intervention](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/milestones/M4-conversation-and-intervention.md) | As drafted |
| [M5 Concurrency and limits](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/milestones/M5-concurrency-and-limits.md) | Two more small fixture repositories for the three-repository demo |
| [M6 Recovery](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/milestones/M6-recovery.md) | As drafted |
| [M7 Remote hosts](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/milestones/M7-remote-hosts.md) | As drafted |
| [M8 Release and upgrade](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/milestones/M8-release-and-upgrade.md) | As drafted |

## Changes to accepted documents since their review

Four changes were made to documents after you had accepted them, each because a later board's answer or a consistency check required it:

1. **06 rule 16** gained one sentence: a repository-setup job is delivered the same way as a notes-only job, by Coordination's leader. This follows your answer on the 08 board.
2. **00, Building v1, "The end of a milestone"** gained one sentence: every demo is recorded with an ordinary terminal recorder running in the demo terminal, with AsmAI's own per-dispatch recordings kept alongside from M4. This follows your answer on the M1 board.
3. **00, the same paragraph,** gained one more sentence: each milestone runs only its own cases; M2 also reruns M1's on Codex, and all 47 run together in M8. This follows your answer on the M3 board.
4. **M2, What it adds, item 2** now says `asmai providers install` covers Claude Code and Codex, with the pinned Lavish arriving in M3 with the Lavish server. It had said "every pinned provider", which contradicted the rule map.

Nothing else in an accepted document changed.

## Checks run on the whole

- Every link in the 21 documents points at talvor/AssemblyAI and resolves to a file in this branch; there are no relative links.
- Every rule number one document cites in another exists and is the rule meant.
- The table of 47 cases in 00 and in 11 agree on each case's document and milestone, and each milestone document lists exactly its cases.
- The rule map (`.lavish/milestone_allocation.py`) assigns every rule of the eleven component documents to a milestone or to proving and launch, with none left out.
- "Phillip" appears in the component documents only where a decision is about you personally: the copyright, the fixture repository, the Mac, the virtual machine for S9 and your verdicts.

## The records

Each document's board, questions, answers, raw Lavish capture and the reply I posted are kept under `.lavish/spec-doc-*`, with the board renderer (`spec_md.py`, `gen_spec_doc.py`) and the rule map, so they ship with the pull request as earlier tickets' records did.
