# M8 Release and upgrade

M8 turns the qualified code into a release: the release workflow and its attestations, the install script, the running factory keeping its version, new provider pins offered at start, store migrations, backups and `asmai restore`, `asmai notices`, and the qualification record that `asmai start` enforces. C5 passes, then all 47 cases pass together on the candidate commit, and the first release candidate is published ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27)).

## What it adds

1. **The release workflow and attestations:** a release built in GitHub Actions from the commit that adds the qualification record to the qualified commit, checked to be the only change, reproducibly and without a C compiler, with checksums and an attestation for every file, refusing to publish without a Lavish build for every certified platform ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27), [10](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/10-release-install-and-upgrade.md)).
2. **The install script,** the only install channel ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27), [10](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/10-release-install-and-upgrade.md)).
3. **The running factory keeping its version,** through the daemon's copy of its executable at one fixed path, and the version guard ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27), [10](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/10-release-install-and-upgrade.md), [09](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/09-cli-and-configuration.md)).
4. **New provider pins at start** ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27), [10](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/10-release-install-and-upgrade.md)).
5. **Store migrations, backups and `asmai restore`,** with the store checks at start; from v1.0.0-rc.1 every schema change is a kept migration ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27), [10](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/10-release-install-and-upgrade.md)).
6. **`asmai notices`** ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27), [10](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/10-release-install-and-upgrade.md)).
7. **The qualification record** inside the release, enforced by `asmai start` and shown by `asmai doctor`, with doctor's self-check ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27), [11](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/11-qualification-and-proving.md)).
8. **The configuration across releases:** never rewritten, with renamed settings warned about and only unhonourable ones refused ([10](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/10-release-install-and-upgrade.md), [09](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/09-cli-and-configuration.md)).

## Builds on

[M7 Remote hosts](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/milestones/M7-remote-hosts.md), and through it every earlier milestone: M8's candidate commit carries all of v1's behaviour.

## Rules delivered

Where a rule arrives in parts, the table names the part this milestone delivers.

**[02 Daemon and store](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/02-daemon-and-store.md)**

| Rule | | Part delivered here |
| --- | --- | --- |
| 6 | Checks before anything runs | the store's checks and migration, the qualification record |
| 18 | Copies | asmai backup |
| 64 | After a restore | All |

**[03 Provider sessions and terminals](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/03-provider-sessions-and-terminals.md)**

| Rule | | Part delivered here |
| --- | --- | --- |
| 4 | Only qualified combinations run | the qualification record |
| 13 | Hooks name a fixed path | All |

**[08 Skills and agent instructions](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/08-skills-and-agent-instructions.md)**

| Rule | | Part delivered here |
| --- | --- | --- |
| 5 | After an upgrade | All |

**[09 CLI and configuration](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/09-cli-and-configuration.md)**

| Rule | | Part delivered here |
| --- | --- | --- |
| 6 | Version guard | All |
| 24 | No `asmai qualify` | All |
| 30 | Across releases | All |
| 35 | Variables AsmAI reads or sets | ASMAI_INSTALL_DIR |

**[10 Release, install and upgrade](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/10-release-install-and-upgrade.md)**

| Rule | | Part delivered here |
| --- | --- | --- |
| 8 | talvor/asmai | releases |
| 9 | Certified platforms only | All |
| 10 | The build | the release build |
| 11 | A release is the qualified commit plus its record | All |
| 12 | Development builds | All |
| 13 | Release candidates | All |
| 14 | Only the maintainer tags releases | All |
| 15 | Semantic versions with fixed meanings | All |
| 16 | `asmai doctor` | All |
| 17 | One channel: the install script | All |
| 18 | One command | All |
| 19 | What the script does | All |
| 20 | macOS needs no Apple Developer ID | All |
| 21 | Stop, upgrade, start | All |
| 22 | A running factory keeps its version | All |
| 23 | Hooks name the fixed path | All |
| 24 | Other versions | All |
| 25 | Skills change with the release | All |
| 26 | Offered at start | All |
| 27 | Kept copies | All |
| 28 | Codex trust | All |
| 29 | Never rewritten | All |
| 30 | Old names keep working within v1 | All |
| 31 | Refusing only what cannot be honoured | All |
| 32 | Versioned | All |
| 33 | A checked backup first | All |
| 34 | One transaction | All |
| 35 | Three backups kept | All |
| 36 | Forward only, kept from the first release candidate | All |
| 37 | A store start cannot use | All |
| 38 | Explained, never repaired | All |
| 39 | A fresh store | All |
| 40 | `asmai restore <file>` | All |
| 41 | Resolving a downgrade | All |
| 42 | After a restore | All |

**[11 Qualification and proving](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/11-qualification-and-proving.md)**

| Rule | | Part delivered here |
| --- | --- | --- |
| 19 | What it holds | All |
| 20 | Inside the release | All |
| 21 | Enforced | All |
| 22 | A platform | All |
| 23 | The user's host is not qualified again | All |
| 24 | All 47 are the v1 qualification cases | all 47 together |

## Qualification cases

At M8's end ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27), [11](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/11-qualification-and-proving.md)):

| Case | What is qualified |
| --- | --- |
| C5 | Codex hook trust survives an AsmAI upgrade |
| C1 to C47 | All 47 cases, together, on the candidate commit, in the harness on Linux, and run on the Mac |

## Demo path

The first release candidate ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27), [10](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/10-release-install-and-upgrade.md)):

1. All 47 cases pass on the candidate commit; the maintainer commits the qualification record and tags v1.0.0-rc.1.
2. The release workflow confirms the record is the only change and publishes the Linux x86_64 archive, the checksums, the attestations and the install script as a GitHub prerelease.
3. On this host the install script installs the release candidate with `--version v1.0.0-rc.1`, checking the checksum and the attestation; `asmai init` (which installs the pinned providers, Lavish from its Lavish build) and `asmai start` run with the record enforced, and `asmai notices` prints the notices.
4. A job on the fixture repository is delivered as a tested pull request.
5. `asmai backup` takes a copy while the factory runs, and `asmai restore` puts it back with the factory stopped.

## Exit checks

M8 ends when ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27)):

- its tickets are closed;
- the development tests are green on Linux and on macOS;
- C5, and then all 47 cases together on the candidate commit, pass in the harness on Linux and have run on the Mac; a macOS failure becomes a ticket for a later release and never holds up the Linux release candidate;
- its demo path has run once, with the terminal recording kept for Phillip to watch, and v1.0.0-rc.1 is published.

## After M8

The proving scenarios S1 to S9 run on the release candidate with Phillip's verdicts, and AsmAI builds the v2 notify command (S1) and fixes a real defect (S4) in talvor/asmai. With all 47 cases passing on Linux x86_64 and every scenario passed, v1.0.0 is released on Linux; macOS is certified by a later release ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27), [11](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/11-qualification-and-proving.md)).

## Sources

- [Choose the specification's structure and implementation sequence](https://github.com/talvor/AssemblyAI/issues/27#issuecomment-6004852593) (AssemblyAI#27)
- The component documents linked in Rules delivered, and the decision tickets they cite.
- The review of this document: [board](https://github.com/talvor/AssemblyAI/blob/main/.lavish/spec-doc-M8.html) and [answers](https://github.com/talvor/AssemblyAI/blob/main/.lavish/spec-doc-M8-answers.json).
