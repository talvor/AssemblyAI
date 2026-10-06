# 10 Release, install and upgrade

This document specifies how AsmAI is licensed, built, released, installed and upgraded: the license and notices, the build, the release workflow and its attestations, the install script, version numbers, upgrades, new provider pins, the configuration across releases, store migrations and restore. [11 Qualification and proving](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/11-qualification-and-proving.md) specifies the qualification that every release carries.

## Rules

### License and notices

1. **Apache-2.0**, with the copyright held by Phillip Hall ([AssemblyAI#20](https://github.com/talvor/AssemblyAI/issues/20)).
2. **In the repository.** talvor/asmai has a LICENSE file, a short NOTICE naming AsmAI and its copyright, and an SPDX license line at the top of each source file ([AssemblyAI#20](https://github.com/talvor/AssemblyAI/issues/20)).
3. **Contributions.** There is no contributor agreement and no sign-off, because Apache-2.0 section 5 covers contributions. Outside pull requests are welcome, and only the maintainer merges ([AssemblyAI#20](https://github.com/talvor/AssemblyAI/issues/20)).
4. **Notices travel inside the executable.** The release build generates one third-party notices file from every Go module compiled in, plus the bundled skills' MIT notice. That file and AsmAI's LICENSE go in every archive and are embedded in the executable, and `asmai notices` prints them ([AssemblyAI#20](https://github.com/talvor/AssemblyAI/issues/20), [AssemblyAI#17](https://github.com/talvor/AssemblyAI/issues/17), [ADR 0009](https://github.com/talvor/AssemblyAI/blob/main/docs/adr/0009-a-release-is-the-qualified-commit-plus-its-record.md)). Each Lavish build carries its own notices file for lavish-axi, its npm dependencies, its fonts and the Deno runtime, and `asmai notices` also prints the installed Lavish build's ([ADR 0010](https://github.com/talvor/AssemblyAI/blob/main/docs/adr/0010-lavish-is-a-deno-compiled-executable-built-per-pin.md)).
5. **A license allow-list.** The build fails when a compiled-in module's license is not MIT, BSD, Apache-2.0 or ISC; any other license needs the maintainer's decision first ([AssemblyAI#20](https://github.com/talvor/AssemblyAI/issues/20)). The same allow-list applies to everything compiled into a Lavish build: SIL OFL 1.1 is accepted for Lavish's vendored fonts, and the Deno runtime's licenses are audited before the first Lavish build ([ADR 0010](https://github.com/talvor/AssemblyAI/blob/main/docs/adr/0010-lavish-is-a-deno-compiled-executable-built-per-pin.md), [answers](https://github.com/talvor/AssemblyAI/blob/main/.lavish/lavish-delivery-answers.json)).
6. **Copying from the references.** Copying or adapting a component from Firstmate or OpenRig needs its own explicit decision, presented with the source revision, the license and notice requirements, the dependencies, the intended contract, the tests, and who maintains it and handles its updates. Copied code becomes AsmAI's own; no component is approved yet. Ordinary third-party libraries are not affected ([AssemblyAI#16](https://github.com/talvor/AssemblyAI/issues/16)).
7. **Claude Code and Codex are not redistributed.** `asmai providers install` fetches Claude Code and Codex from their official channels. Lavish is the exception: AsmAI builds it (rule 10), and `providers install` fetches the pinned Lavish build from talvor/asmai ([AssemblyAI#20](https://github.com/talvor/AssemblyAI/issues/20), [03](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/03-provider-sessions-and-terminals.md), [ADR 0010](https://github.com/talvor/AssemblyAI/blob/main/docs/adr/0010-lavish-is-a-deno-compiled-executable-built-per-pin.md)).

### Where releases come from

8. **talvor/asmai.** Releases are published at github.com/talvor/asmai/releases, from the repository that holds AsmAI's code ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27), [AssemblyAI#20](https://github.com/talvor/AssemblyAI/issues/20)).
9. **Certified platforms only.** The planned platforms are Linux x86_64 and macOS on Apple silicon. A release publishes an executable only for the platforms its qualification record certifies, so the first releases are Linux x86_64 only. Linux arm64 and Intel macOS are not built; adding a platform means qualifying it, and certifying another platform takes a new release ([AssemblyAI#20](https://github.com/talvor/AssemblyAI/issues/20), [ADR 0009](https://github.com/talvor/AssemblyAI/blob/main/docs/adr/0009-a-release-is-the-qualified-commit-plus-its-record.md)).
10. **The build.** GitHub Actions builds each release from its tag, with no C compiler (a CGo-free SQLite) and reproducible settings, so anyone can rebuild a release from its tag and get the same executables. It publishes one archive per platform, a SHA-256 checksums file, and an artifact attestation for every file, checked with `gh attestation verify` ([AssemblyAI#20](https://github.com/talvor/AssemblyAI/issues/20), [ADR 0009](https://github.com/talvor/AssemblyAI/blob/main/docs/adr/0009-a-release-is-the-qualified-commit-plus-its-record.md)). Lavish is not built per release. When the pins file moves lavish-axi or Deno, a workflow compiles Lavish for every certified platform with deno compile from the committed lock and publishes the executables as a Lavish build: a release in talvor/asmai with its own tag, never marked latest, with checksums and an attestation for every file. The pins file then records each platform's digest. Releases reuse a Lavish build until its pin moves, and certifying a new platform builds Lavish for it under the same pin ([ADR 0010](https://github.com/talvor/AssemblyAI/blob/main/docs/adr/0010-lavish-is-a-deno-compiled-executable-built-per-pin.md), [answers](https://github.com/talvor/AssemblyAI/blob/main/.lavish/lavish-delivery-answers.json)).
11. **A release is the qualified commit plus its record.** The qualification harness runs a development build of the candidate commit. The maintainer commits the qualification record it produces and tags that commit. The release workflow checks that the record is the only change since the qualified commit, and that every certified platform has a published, attested Lavish build matching the digest in the pins file, then builds and publishes ([ADR 0009](https://github.com/talvor/AssemblyAI/blob/main/docs/adr/0009-a-release-is-the-qualified-commit-plus-its-record.md), [AssemblyAI#20](https://github.com/talvor/AssemblyAI/issues/20), [11](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/11-qualification-and-proving.md)).
12. **Development builds** may start unqualified combinations, and say so ([ADR 0009](https://github.com/talvor/AssemblyAI/blob/main/docs/adr/0009-a-release-is-the-qualified-commit-plus-its-record.md)). They may also reset their store ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27)).
13. **Release candidates** (`v1.0.0-rc.N`) are GitHub prereleases used for the proving scenarios. The install script skips them unless asked ([AssemblyAI#20](https://github.com/talvor/AssemblyAI/issues/20), [ADR 0009](https://github.com/talvor/AssemblyAI/blob/main/docs/adr/0009-a-release-is-the-qualified-commit-plus-its-record.md)).
14. **Only the maintainer tags releases.** AsmAI's own agents never tag or publish one ([AssemblyAI#20](https://github.com/talvor/AssemblyAI/issues/20)).

### Version numbers

15. **Semantic versions with fixed meanings** ([AssemblyAI#20](https://github.com/talvor/AssemblyAI/issues/20)):
    - v1.0.0 is the launch;
    - a patch release fixes defects or moves a pinned provider version, and adds no behaviour;
    - a minor release adds behaviour, settings or a certified platform;
    - a major release is the only kind that may need more than stop, upgrade, start, for example to drop retired settings, and its release notes say what to do;
    - store migrations can come in any release, because they run by themselves.
16. **`asmai doctor`** reports a newer release together with its kind, ignoring Lavish builds ([AssemblyAI#20](https://github.com/talvor/AssemblyAI/issues/20), [AssemblyAI#9](https://github.com/talvor/AssemblyAI/issues/9), [ADR 0010](https://github.com/talvor/AssemblyAI/blob/main/docs/adr/0010-lavish-is-a-deno-compiled-executable-built-per-pin.md)).

### Installing

17. **One channel: the install script.** It is the only way to install AsmAI; there is no Homebrew tap, no package registry and no self-update ([AssemblyAI#20](https://github.com/talvor/AssemblyAI/issues/20), [ADR 0003](https://github.com/talvor/AssemblyAI/blob/main/docs/adr/0003-go-executable-runs-pinned-providers.md), [ADR 0009](https://github.com/talvor/AssemblyAI/blob/main/docs/adr/0009-a-release-is-the-qualified-commit-plus-its-record.md)).
18. **One command:** `curl -fsSL https://github.com/talvor/asmai/releases/latest/download/install.sh | sh`. The script is itself a release file, attested with the release ([AssemblyAI#20](https://github.com/talvor/AssemblyAI/issues/20)).
19. **What the script does** ([AssemblyAI#20](https://github.com/talvor/AssemblyAI/issues/20)):
    - it detects the platform and refuses one the release does not certify, naming those it does;
    - it downloads that platform's archive and the checksums file and checks the SHA-256, failing closed; when gh is installed and signed in, it also runs `gh attestation verify` and fails on a mismatch, and otherwise it says how to check by hand;
    - it installs into `~/.local/bin`, or `ASMAI_INSTALL_DIR`, never with sudo; if that folder is not on PATH, it prints the line to add and leaves shell files alone;
    - `--version v1.2.3` installs a specific release: a release candidate, or an older release to go back to;
    - rerunning it upgrades; it refuses to replace a running factory's executable unless given `--force`;
    - it ends by naming `asmai init` after a first install, or `asmai start` after an upgrade.
20. **macOS needs no Apple Developer ID.** curl sets no quarantine, and Go's linker signs each Apple silicon executable ad hoc. An archive downloaded in a browser needs its quarantine cleared by hand, and the release notes say how ([AssemblyAI#20](https://github.com/talvor/AssemblyAI/issues/20), [ADR 0009](https://github.com/talvor/AssemblyAI/blob/main/docs/adr/0009-a-release-is-the-qualified-commit-plus-its-record.md)).

### Upgrading

21. **Stop, upgrade, start.** Upgrading is stopping the factory, rerunning the install script and starting it again. There is no hot upgrade ([AssemblyAI#20](https://github.com/talvor/AssemblyAI/issues/20), [AssemblyAI#7](https://github.com/talvor/AssemblyAI/issues/7)).
22. **A running factory keeps its version.** At start, the daemon copies its own executable to one fixed path in the state directory, replacing the previous copy, and every agent session runs that copy, so agents never meet another version ([AssemblyAI#20](https://github.com/talvor/AssemblyAI/issues/20)).
23. **Hooks name the fixed path,** never a versioned one, so Codex's trust in them can survive an upgrade ([AssemblyAI#20](https://github.com/talvor/AssemblyAI/issues/20), [03](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/03-provider-sessions-and-terminals.md)).
24. **Other versions.** A command from a version other than the running daemon's does only `stop`, `status` and `doctor` ([09](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/09-cli-and-configuration.md)), and the status line shows "AsmAI vX installed; restart to apply" ([AssemblyAI#20](https://github.com/talvor/AssemblyAI/issues/20)).
25. **Skills change with the release.** After an upgrade, work continues on the new skill bundle from the next dispatch ([08](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/08-skills-and-agent-instructions.md)).

### New provider pins

26. **Offered at start.** After an upgrade, `asmai start` lists the newly pinned Claude Code, Codex and Lavish versions. At a terminal it offers to install them and continues once the user confirms. Without a terminal, for example under the service, it refuses and names `asmai providers install` ([AssemblyAI#20](https://github.com/talvor/AssemblyAI/issues/20)).
27. **Kept copies.** The previous release's pinned copies are kept, so reinstalling that release needs no download; older copies are removed ([AssemblyAI#20](https://github.com/talvor/AssemblyAI/issues/20)).
28. **Codex trust.** A Codex trust review that the new version needs is named the same way ([AssemblyAI#20](https://github.com/talvor/AssemblyAI/issues/20)).

### The configuration across releases

29. **Never rewritten.** AsmAI never rewrites `config.toml` during an upgrade ([AssemblyAI#20](https://github.com/talvor/AssemblyAI/issues/20)).
30. **Old names keep working within v1.** A new setting has a default, and a renamed or retired setting keeps working, with a warning in `asmai doctor` and `asmai config check` that names its replacement ([AssemblyAI#20](https://github.com/talvor/AssemblyAI/issues/20)).
31. **Refusing only what cannot be honoured.** Only a setting that can no longer be honoured makes `asmai start` refuse, naming the line and the fix. A major release may drop retired settings ([AssemblyAI#20](https://github.com/talvor/AssemblyAI/issues/20)).

### The store across releases

32. **Versioned.** Each release embeds numbered migrations, and the store records its schema version and the AsmAI version that last wrote it ([AssemblyAI#20](https://github.com/talvor/AssemblyAI/issues/20)).
33. **A checked backup first.** When `asmai start` finds migrations pending, it first takes a pre-migration backup into the state directory's `backups` folder, the same way `asmai backup` does, and checks it. If the volume lacks space for the backup, start refuses before changing anything ([AssemblyAI#20](https://github.com/talvor/AssemblyAI/issues/20)).
34. **One transaction.** It then applies every pending migration in one transaction. If one fails, everything rolls back, and start refuses and names the backup ([AssemblyAI#20](https://github.com/talvor/AssemblyAI/issues/20)).
35. **Three backups kept.** The three newest pre-migration backups are kept, and `asmai status` counts them in disk use ([AssemblyAI#20](https://github.com/talvor/AssemblyAI/issues/20), [07](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/07-limits-holds-and-visibility.md)).
36. **Forward only, kept from the first release candidate.** From v1.0.0-rc.1 every schema change is a kept forward-only migration, and every release keeps all of them, so any v1 release, and a proving-scenario factory on a release candidate, upgrades straight to any later one. There are no down migrations; the way back is the backup taken just before the change ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27), [AssemblyAI#20](https://github.com/talvor/AssemblyAI/issues/20)).
37. **A store start cannot use.** `asmai start` refuses before starting any agent in four cases ([AssemblyAI#20](https://github.com/talvor/AssemblyAI/issues/20)):
    - **a downgrade:** the store was written by a newer schema than this executable knows;
    - **an unreadable store:** not a SQLite database, failing SQLite's integrity check, or lacking AsmAI's tables;
    - **a lost store:** there is none, but the state directory still holds AsmAI's clones, workspaces or recordings;
    - **a held store:** another AsmAI daemon has it open.
38. **Explained, never repaired.** `asmai doctor` names the case, the AsmAI version that last wrote the store, and the newest backups. AsmAI never repairs, replaces or deletes a store ([AssemblyAI#20](https://github.com/talvor/AssemblyAI/issues/20)).
39. **A fresh store** is created only when the state directory holds no AsmAI state at all ([AssemblyAI#20](https://github.com/talvor/AssemblyAI/issues/20)).

### Restore

40. **`asmai restore <file>`**, with the factory stopped, checks a backup's integrity and schema version, sets the current store aside as a dated broken copy instead of deleting it, and puts the backup in place ([AssemblyAI#20](https://github.com/talvor/AssemblyAI/issues/20)).
41. **Resolving a downgrade.** A downgrade is resolved by reinstalling the newer release, or by restoring a backup the older one can read ([AssemblyAI#20](https://github.com/talvor/AssemblyAI/issues/20)).
42. **After a restore,** every open assignment needs reconciliation at start, and commits pushed since the backup count as outside changes ([AssemblyAI#20](https://github.com/talvor/AssemblyAI/issues/20), [02](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/02-daemon-and-store.md), [05](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/05-repositories-and-job-branches.md)).

## Interfaces

### Commands

| Who | Command | Purpose |
| --- | --- | --- |
| The user | `curl -fsSL https://github.com/talvor/asmai/releases/latest/download/install.sh \| sh`, and the script's `--version <tag>` and `--force` | Install or upgrade (rules 18, 19) |
| The user | `asmai notices` | Print the license and third-party notices (rule 4) |
| The user | `asmai restore <file>` | Put a backup in place, with the factory stopped (rule 40) |
| The user | `asmai backup <file>` | A consistent copy of the store ([02](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/02-daemon-and-store.md)) |
| The user | `asmai providers install` | Install new pins after an upgrade (rule 26) |
| The maintainer | Tagging the record commit | Starts the release workflow (rule 11) |

### Store records

| Record | Holds |
| --- | --- |
| Schema version | The store's schema version and the AsmAI version that last wrote it (rule 32) |
| Migration | Each migration applied, with the pre-migration backup taken for it |

### Files

| File | Where | Holds |
| --- | --- | --- |
| Release archive | One per certified platform, on the release | The executable, LICENSE and the notices file |
| Checksums file | On the release | SHA-256 of every archive |
| Attestations | On the release | One for every file, including the install script |
| `install.sh` | On the release | The install script (rule 19) |
| The daemon's copy of the executable | One fixed path in the state directory | What every agent session runs (rule 22) |
| Pre-migration backups | `backups` in the state directory | The three newest (rule 35) |
| Dated broken copy | The state directory | A store set aside by `asmai restore` (rule 40) |
| Third-party notices | Generated at build, embedded and in every archive | Every compiled-in module's license and the skills' MIT notice (rule 4) |
| The pins file | Committed in talvor/asmai, embedded in each release | The pinned Claude Code, Codex, lavish-axi and Deno versions, and each platform's Lavish digest (rule 10) |
| Lavish build | A release in talvor/asmai for each Lavish pin, never marked latest | One Lavish executable per certified platform, its notices, the checksums and the attestations (rule 10) |

## Settings and defaults

| Variable | Default | Meaning |
| --- | --- | --- |
| `ASMAI_INSTALL_DIR` | `~/.local/bin` | Where the install script puts `asmai` (rule 19) |

The number of pre-migration backups kept (three) and the license allow-list are fixed by the release, not settings.

## Failure handling

| Failure | Handling |
| --- | --- |
| Platform not certified by the release | The install script refuses and names the platforms it certifies (rule 19) |
| Checksum or attestation mismatch | The install script fails closed (rule 19) |
| A Lavish executable's checksum, attestation or digest does not match | `asmai providers install` fails closed (rules 7, 10) |
| No Lavish build for a certified platform | The release workflow refuses to publish (rule 11) |
| Replacing a running factory's executable | Refused unless `--force` (rule 19) |
| A compiled-in module's license is not on the allow-list | The build fails (rule 5) |
| The record is not the only change since the qualified commit | The release workflow refuses to publish (rule 11) |
| New pins at start without a terminal | Start refuses and names `asmai providers install` (rule 26) |
| A migration fails | Everything rolls back; start refuses and names the backup (rule 34) |
| No space for the pre-migration backup | Start refuses before changing anything (rule 33) |
| Downgrade, unreadable, lost or held store | Start refuses before any agent; doctor explains (rules 37, 38) |
| A setting that can no longer be honoured | Start refuses, naming the line and the fix (rule 31) |

## Qualification cases and proving scenarios

- **C5**: Codex hook trust survives an AsmAI upgrade (rules 22, 23).
- **C1** and **C2** ([09](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/09-cli-and-configuration.md), [03](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/03-provider-sessions-and-terminals.md)) rely on the qualification record this document builds into each release.
- **All 47 cases** run together on the candidate commit before a release candidate is tagged ([11](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/11-qualification-and-proving.md)).
- **The proving scenarios** run on a release candidate installed with `--version`, and a later release reruns a scenario only when it changes what that scenario proves ([AssemblyAI#12](https://github.com/talvor/AssemblyAI/issues/12)).

## Sources

- [Choose factory hosting and lifecycle](https://github.com/talvor/AssemblyAI/issues/7#issuecomment-5976506834) (AssemblyAI#7)
- [Define CLI setup and management experience](https://github.com/talvor/AssemblyAI/issues/9#issuecomment-5979143255) (AssemblyAI#9)
- [Define v1 acceptance scenarios and evidence](https://github.com/talvor/AssemblyAI/issues/12#issuecomment-5993314453) (AssemblyAI#12)
- [Choose inspiration versus reuse of reference systems](https://github.com/talvor/AssemblyAI/issues/16#issuecomment-5974485663) (AssemblyAI#16)
- [Choose skill bundles and update policy](https://github.com/talvor/AssemblyAI/issues/17#issuecomment-5992055697) (AssemblyAI#17)
- [Choose license, release packaging and upgrade migration](https://github.com/talvor/AssemblyAI/issues/20#issuecomment-6004145724) (AssemblyAI#20), with its [answers](https://github.com/talvor/AssemblyAI/blob/main/.lavish/release-answers.json) and [resolution](https://github.com/talvor/AssemblyAI/blob/main/.lavish/release-resolution.md)
- [Choose the specification's structure and implementation sequence](https://github.com/talvor/AssemblyAI/issues/27#issuecomment-6004852593) (AssemblyAI#27)
- [ADR 0003](https://github.com/talvor/AssemblyAI/blob/main/docs/adr/0003-go-executable-runs-pinned-providers.md), [ADR 0009](https://github.com/talvor/AssemblyAI/blob/main/docs/adr/0009-a-release-is-the-qualified-commit-plus-its-record.md) and the [glossary](https://github.com/talvor/AssemblyAI/blob/main/GLOSSARY.md): Release, Lavish build, Upgrade, Store, Qualification record, Certified platform.
- The [Lavish and skill delivery review](https://github.com/talvor/AssemblyAI/blob/main/.lavish/lavish-delivery-answers.json) (2026-10-07), with the [Lavish deno compile check](https://github.com/talvor/AssemblyAI/blob/main/docs/research/lavish-deno-compile-check.md) and [ADR 0010](https://github.com/talvor/AssemblyAI/blob/main/docs/adr/0010-lavish-is-a-deno-compiled-executable-built-per-pin.md): Lavish built as a Deno-compiled executable when its pin moves, and how the daemon runs it.
- The review of this document: [board](https://github.com/talvor/AssemblyAI/blob/main/.lavish/spec-doc-10.html) and [answers](https://github.com/talvor/AssemblyAI/blob/main/.lavish/spec-doc-10-answers.json).
