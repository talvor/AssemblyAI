# M0 Groundwork

M0 prepares everything the later milestones build on: the talvor/asmai repository and its tracker, the Go module, hosted CI with the fake provider, the license checks and notices, the fixture repository, and the harness's separate OS users. It delivers no factory behaviour and passes no qualification case ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27)).

Each milestone document says which rules of which component documents the milestone delivers, its exit checks, and the cases and demo path that close it. Phillip runs to-tickets in talvor/asmai on the milestone documents, in order, one milestone at a time; its tickets are vertical slices that link into the component documents, each blocked by tickets of its own run or by the previous milestone ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27), [00](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/00-overview.md)).

## What it adds

1. **talvor/asmai**, a new repository for AsmAI's code, its implementation tickets and its releases. Nothing is brought across from talvor/AssemblyAI except a copy of `GLOSSARY.md` and ADRs 0001 to 0009 as they stand when the specification is confirmed. From then on they evolve in talvor/asmai, and new ADRs there are numbered from 0010. Its README explains the split between the two repositories ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27)).
2. **Its tracker, set up for the skills** that build AsmAI, and **no-mistakes gating its pull requests**. Firstmate crews implement each ticket as a pull request with the implement and tdd skills, and Phillip merges ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27)). Because to-tickets runs in talvor/asmai, Phillip does these first steps by hand before running it on M0: he creates talvor/asmai, copies the glossary and ADRs 0001 to 0009, runs setup-matt-pocock-skills there and sets up no-mistakes. M0's tickets cover the rest of this list ([answers](https://github.com/talvor/AssemblyAI/blob/main/.lavish/spec-doc-M0-answers.json)).
3. **The Go module** `github.com/talvor/asmai`, with LICENSE, NOTICE and an SPDX line at the top of each source file ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27), [10](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/10-release-install-and-upgrade.md)).
4. **Hosted CI on Linux and macOS** for every pull request: the build for both platforms, the development tests with the scripted fake provider, the license allow-list, and the generated third-party notices ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27), [10](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/10-release-install-and-upgrade.md), [11](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/11-qualification-and-proving.md)).
5. **The fixture repository**, a separate small repository Phillip owns (for example talvor/asmai-fixture), whose CI can be made red, slow or absent ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27), [11](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/11-qualification-and-proving.md)).
6. **The harness's separate OS users**, on this host and on the Mac Phillip already has, each with its own provider sign-in ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27), [11](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/11-qualification-and-proving.md)).

## Builds on

Nothing: M0 is the first milestone. Every later milestone builds on it.

## Rules delivered

**[09 CLI and configuration](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/09-cli-and-configuration.md)**

| Rule | | Part delivered here |
| --- | --- | --- |
| 2 | No package names are claimed | All |
| 3 | The Go module | All |

**[10 Release, install and upgrade](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/10-release-install-and-upgrade.md)**

| Rule | | Part delivered here |
| --- | --- | --- |
| 1 | Apache-2.0 | All |
| 2 | In the repository | All |
| 3 | Contributions | All |
| 4 | Notices travel inside the executable | the executable's notices |
| 5 | A license allow-list | compiled-in Go modules |
| 6 | Copying from the references | All |
| 8 | talvor/asmai | the repository |

**[11 Qualification and proving](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/11-qualification-and-proving.md)**

| Rule | | Part delivered here |
| --- | --- | --- |
| 4 | On every PR | All |
| 5 | A scripted fake provider | All |
| 6 | Real providers on a real host | the separate OS users |
| 10 | The fixture repository | All |
| 11 | The hosts | All |

## Qualification cases

None. The harness itself starts in M1 with the first cases ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27)).

## Demo path

None. M0 makes every later milestone possible ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27)).

## Exit checks

M0 ends when ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27)):

- its tickets are closed;
- the development tests, with the fake provider, the license allow-list and the generated notices, are green in hosted CI on Linux and on macOS;
- the fixture repository's CI can be made red, slow and absent;
- the harness's OS users exist, with their own sign-in, on this host and on the Mac.

The general end-of-milestone rule (cases passing in the harness on Linux and run on the Mac, and a recorded demo path) applies from M1, the first milestone with cases and a demo path.

## Sources

- [Choose the specification's structure and implementation sequence](https://github.com/talvor/AssemblyAI/issues/27#issuecomment-6004852593) (AssemblyAI#27)
- [Choose license, release packaging and upgrade migration](https://github.com/talvor/AssemblyAI/issues/20#issuecomment-6004145724) (AssemblyAI#20)
- [Define v1 acceptance scenarios and evidence](https://github.com/talvor/AssemblyAI/issues/12#issuecomment-5993314453) (AssemblyAI#12)
- [ADR 0008](https://github.com/talvor/AssemblyAI/blob/main/docs/adr/0008-qualification-runs-real-provider-clis-on-real-hosts.md) and [ADR 0009](https://github.com/talvor/AssemblyAI/blob/main/docs/adr/0009-a-release-is-the-qualified-commit-plus-its-record.md)
- The review of this document: [questions](https://github.com/talvor/AssemblyAI/blob/main/.lavish/spec-doc-M0-round1-questions.json) and [answers](https://github.com/talvor/AssemblyAI/blob/main/.lavish/spec-doc-M0-answers.json).
