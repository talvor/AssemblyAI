## Resolution — confirmed by Phillip in Lavish

### License and notices
- **Apache-2.0**, with the copyright held by Phillip Hall. This settles the license that [Choose runtime adapters and authentication](https://github.com/talvor/AssemblyAI/issues/15) left unselected.
- **Notices travel inside the executable.** The release build generates one third-party notices file from every Go module compiled in, plus the bundled skills' MIT notice that [Choose skill bundles and update policy](https://github.com/talvor/AssemblyAI/issues/17) handed here. That file and AsmAI's LICENSE go in every archive and are embedded in the executable, and a new `asmai notices` command prints them.
- **A license allow-list.** The build fails when a compiled-in module's license is not MIT, BSD, Apache-2.0 or ISC, so any other license needs Phillip's decision first. Copying a component from Firstmate or OpenRig still needs its own decision ([Choose inspiration versus reuse of reference systems](https://github.com/talvor/AssemblyAI/issues/16)).
- **Contributions.** There is no contributor agreement and no sign-off, because Apache-2.0 section 5 covers contributions. Outside pull requests are welcome, and only the maintainer merges. The repository has LICENSE, a short NOTICE naming AsmAI and its copyright, and an SPDX license line at the top of each source file.
- **Providers are not redistributed.** `asmai providers install` fetches Claude Code, Codex and Lavish from their official channels.

### Where releases come from
- **Repository.** talvor/AssemblyAI is renamed to talvor/asmai before the first release, so releases live at github.com/talvor/asmai/releases. The map's issues and history move with it.
- **Platforms.** The planned platforms are Linux x86_64 and macOS on Apple silicon. A release publishes an executable only for the platforms its qualification record certifies, so the first releases are Linux x86_64 only. Linux arm64 and Intel macOS are not built; adding a platform means qualifying it.
- **Build.** GitHub Actions builds each release from its tag, with no C compiler (a CGo-free SQLite) and reproducible settings, so anyone can rebuild a release from its tag and get the same executables. It publishes one archive per platform, a SHA-256 checksums file, and an artifact attestation for every file, checked with `gh attestation verify`.
- **The qualification record goes inside the release** (ADR 0009). The qualification harness runs a development build of the candidate commit, which may start unqualified combinations and says so. The maintainer commits the record it produces and tags that commit. The release workflow checks that the record is the only change since the qualified commit, then builds and publishes. Certifying another platform, such as macOS after Linux, takes a new release.
- **Release candidates** (`v1.0.0-rc.N`) are GitHub prereleases used for the proving scenarios. The install script skips them unless asked.
- **Only the maintainer tags releases.** AsmAI's own agents never tag or publish one.
- **Version numbers** are semantic versions with fixed meanings.
  - v1.0.0 is the launch.
  - A patch release fixes defects or moves a pinned provider version, and adds no behaviour.
  - A minor release adds behaviour, settings or a certified platform.
  - A major release is the only kind that may need more than stop, upgrade, start, for example to drop retired settings, and its release notes say what to do.
  - Store migrations can come in any release, because they run by themselves.
  - `asmai doctor` reports a newer release together with its kind.

### Installing
- **One channel: the install script.** There is no Homebrew tap. This replaces the tap listed in [Define CLI setup and management experience](https://github.com/talvor/AssemblyAI/issues/9), and ADR 0003 gains a dated line saying so.
- **One command:** `curl -fsSL https://github.com/talvor/asmai/releases/latest/download/install.sh | sh`. The script is itself a release file, attested with the release.
  - It detects the platform and refuses one the release does not certify, naming those it does.
  - It downloads that platform's archive and the checksums file and checks the SHA-256, failing closed. When gh is installed and signed in, it also runs `gh attestation verify` and fails on a mismatch. Otherwise it says how to check by hand.
  - It installs into `~/.local/bin` (or `ASMAI_INSTALL_DIR`), never with sudo. If that folder is not on PATH, it prints the line to add and leaves shell files alone.
  - `--version v1.2.3` installs a specific release: a release candidate, or an older release to go back to.
  - Rerunning it upgrades. It refuses to replace a running factory's executable unless given `--force`. It ends by naming `asmai init` after a first install, or `asmai start` after an upgrade.
- **macOS needs no Apple Developer ID.** curl sets no quarantine, and Go's linker signs each Apple silicon executable ad hoc. An archive downloaded in a browser needs its quarantine cleared by hand, and the release notes say how.
- **No names are claimed.** Nothing is published to npm or crates.io, and there is no tap to create. This replaces "the names are claimed when implementation starts" in [Define CLI setup and management experience](https://github.com/talvor/AssemblyAI/issues/9). npm's terms and crates.io's policy both forbid packages that only reserve a name. If AsmAI ever ships on a registry, it takes the name then, or another one if it is gone.

### Upgrading
Upgrading stays stop, rerun the install script, start.
- **A running factory keeps its version.**
  - At start the daemon copies its own executable to one fixed path in the state directory, replacing the previous copy, and every agent session runs that copy. Agents therefore never meet another version.
  - Hook definitions name that fixed path, never a versioned one, so Codex's trust in them can survive an upgrade (qualification case C5).
  - A command from a version other than the running daemon's does only `stop`, `status` and `doctor`. For anything else it says which version is installed, which is running, and to run `asmai stop` and then `asmai start`.
  - The status line shows "AsmAI vX installed; restart to apply".
- **New pinned providers.**
  - After an upgrade, `asmai start` lists the newly pinned Claude Code, Codex and Lavish versions.
  - At a terminal it offers to install them and continues once the user confirms. Without a terminal, for example under the service, it refuses and names `asmai providers install`.
  - The previous release's pinned copies are kept, so reinstalling that release needs no download, and older copies are removed.
  - A Codex trust review that the new version needs is named the same way.
- **Configuration.**
  - AsmAI never rewrites `config.toml` during an upgrade.
  - Within v1 a new setting has a default, and a renamed or retired setting keeps working, with a warning in `asmai doctor` and `asmai config check` that names its replacement.
  - Only a setting that can no longer be honoured makes `asmai start` refuse, naming the line and the fix.
  - A major release may drop retired settings.

### The store across releases
- **Forward-only migrations at start.**
  - Each release embeds numbered migrations, and the store records its schema version and the AsmAI version that last wrote it.
  - When `asmai start` finds migrations pending, it first takes a pre-migration backup into the state directory's `backups` folder (the same way `asmai backup` does) and checks it.
  - It then applies every pending migration in one transaction. If one fails, everything rolls back, and start refuses and names the backup.
  - If the volume lacks space for the backup, start refuses before changing anything.
  - The three newest pre-migration backups are kept, and `asmai status` counts them in disk use.
  - Every release keeps all migrations since v1.0, so any v1 release upgrades straight to any later one. There are no down migrations; the way back is the backup taken just before the change.
- **A store start cannot use.** `asmai start` refuses before starting any agent in four cases:
  - a downgrade: the store was written by a newer schema than this executable knows;
  - an unreadable store: not a SQLite database, failing SQLite's integrity check, or lacking AsmAI's tables;
  - a lost store: there is none, but the state directory still holds AsmAI's clones, workspaces or recordings;
  - a held store: another AsmAI daemon has it open.

  `asmai doctor` names the case, the AsmAI version that last wrote the store, and the newest backups. AsmAI never repairs, replaces or deletes a store.
- **Restore.**
  - A new `asmai restore <file>` (factory stopped) checks a backup's integrity and schema version, sets the current store aside as a dated broken copy instead of deleting it, and puts the backup in place.
  - A downgrade is resolved by reinstalling the newer release, or by restoring a backup the older one can read.
  - After a restore, every open assignment needs reconciliation at start, and commits pushed since the backup count as outside changes.
- **A fresh store** is created only when the state directory holds no AsmAI state at all.
- **New commands.** `asmai notices` and `asmai restore` join the command set from [Define CLI setup and management experience](https://github.com/talvor/AssemblyAI/issues/9).

### Glossary and ADR
- [GLOSSARY.md](https://github.com/talvor/AssemblyAI/blob/main/GLOSSARY.md) gains **Release**, **Store** and **Upgrade** (pending archive).
- [ADR 0009](https://github.com/talvor/AssemblyAI/blob/main/docs/adr/0009-a-release-is-the-qualified-commit-plus-its-record.md) records that a release is the qualified commit plus its qualification record (pending archive).
- [ADR 0003](https://github.com/talvor/AssemblyAI/blob/main/docs/adr/0003-go-executable-runs-pinned-providers.md) gains a dated line: the Homebrew tap was dropped, and the install script is the only install channel (pending archive).

### Map follow-through
- **Decisions so far** gains this ticket's line, and **Notes** gain a pointer: the license, releases, installation and upgrades are settled here.
- **Out of scope** gains one line: Homebrew, package registries (npm, crates.io) and Apple Developer ID signing are not v1 channels, and AsmAI installs only through its install script from GitHub Releases.
- **No new ticket.** Renaming the repository to talvor/asmai and building the release workflow are implementation steps, to be ordered by [Choose the specification's structure and implementation sequence](https://github.com/talvor/AssemblyAI/issues/27). This resolution unblocks that ticket.
- **No fog graduates.** The configuration-schema fog item is unchanged.
- **No implementation.** This is a planning resolution; it authorizes no implementation.

### Evidence
Three live Lavish rounds on 2026-10-06: 19 questions with recommendations, then confirmation. The answers are recorded verbatim here:
- **Round 1:**
  - Q1 A: Apache-2.0
  - Q2 A: notices generated, embedded and in every archive; asmai notices; permissive allow-list
  - Q3 A: rename to talvor/asmai before the first release
  - Q4 A: Linux x86_64 and macOS arm64 planned; publish only what the record certifies
  - Q5 A: GitHub Actions from the tag, no C compiler, reproducible; checksums plus attestations
  - Q6 A: no Developer ID; a formula in talvor/homebrew-tap installs the prebuilt executable. Note: "I do not want to use homebrew, I want an install script that installs the latest build from github releases." (the note overrides the formula: no Homebrew tap; no Developer ID stands)
  - Q7 A: qualify a commit, then release that commit plus its record; release candidates as prereleases; only the maintainer tags
  - Q8 A: forward-only migrations at start, after a checked pre-migration backup; keep three; any v1 upgrades to any later one
  - Q9 A: refuse and explain; asmai restore; never repair, replace or delete
  - Q10 A: the running factory keeps its version; agents run the daemon's own copy; other versions only stop, status, doctor
  - Q11 A: start offers to install the new pins at a terminal, refuses without one; keep the previous release's copies
  - Q12 A: never rewritten; old names keep working within v1 with a warning; start refuses only what it cannot honour
  - Q13 A: claim nothing on npm or crates.io; create the tap with the first release candidate. Note: "No need to claim any names, using an install script to do the install" (the note overrides the tap: nothing is claimed anywhere)
- **Round 2:**
  - R2-Q1 A: one curl command from the latest release; checksum always, attestation when gh can; ~/.local/bin; --version; no profile edits
  - R2-Q2 A: no agreement and no sign-off; section 5 covers it; LICENSE, NOTICE and SPDX lines
  - R2-Q3 A: semantic versions with fixed meanings; only a major may need more than stop, upgrade, start
  - R2-Q4 A: add all three as drafted
  - R2-Q5 A: record ADR 0009 as drafted, and add a dated line to ADR 0003
  - R2-Q6 A: as listed
- **Confirmation:** CONFIRM "Confirm and record", on a page holding the full resolution above.

Facts checked on 2026-10-05 and 2026-10-06, used as evidence and not as decisions:
- talvor/AssemblyAI is public and has no license. Neither talvor/asmai nor talvor/homebrew-tap exists.
- Licenses: mattpocock/skills, Lavish, Firstmate and no-mistakes are MIT. OpenRig and Codex are Apache-2.0. Claude Code has no open-source license.
- [Homebrew 5.0.0](https://brew.sh/2025/11/12/homebrew-5.0.0) deprecated `--no-quarantine` and unsigned casks, and disables Homebrew's own casks that fail Gatekeeper in September 2026. Intel macOS moves to Tier 3 in September 2026. [GoReleaser](https://goreleaser.com/customization/homebrew_casks/) deprecated Homebrew formulae in favour of casks in v2.10.
- The [Go linker](https://go.googlesource.com/go/+/HEAD/src/cmd/internal/codesign/codesign.go) ad-hoc signs darwin/arm64 executables. Gatekeeper checks quarantined files only, and curl sets no quarantine.
- [GitHub artifact attestations](https://docs.github.com/en/actions/how-tos/secure-your-work/use-artifact-attestations/use-artifact-attestations) are free for public repositories, use Sigstore's public-good log, and are checked with `gh attestation verify`.
- [modernc.org/sqlite](https://pkg.go.dev/modernc.org/sqlite) is a CGo-free SQLite for Linux and macOS on x86_64 and arm64.
- [npm](https://docs.npmjs.com/policies/disputes) forbids publishing a package simply to reserve a name. [crates.io](https://rust-lang.github.io/rfcs/3463-crates-io-policy-update.html) forbids crates that only reserve a name and may delete them.

The board, the round-by-round questions and answers, the glossary terms, ADR 0009 and the ADR 0003 line were produced in a disposable worktree and are being archived separately.
