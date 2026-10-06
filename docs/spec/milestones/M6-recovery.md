# M6 Recovery

M6 makes the factory survive what goes wrong on a host: full reconciliation, generations and fencing, termination of orphaned agents, agent and daemon crashes, a host reboot with the service installed, `asmai stop` draining, terminal disconnects, and a crash during a push or between the push and the pull request ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27)).

## What it adds

1. **Full reconciliation** by the owning leader, against the real repository and GitHub, with silence and conflicting observations making a dispatch unknown ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27), [02](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/02-daemon-and-store.md)).
2. **Generations and fencing,** so a superseded session can never write ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27), [02](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/02-daemon-and-store.md)).
3. **Orphan termination** at every start ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27), [02](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/02-daemon-and-store.md)).
4. **Crash recovery:** an agent crash, a daemon crash, and a host reboot with the service installed, as a systemd user unit or a launchd LaunchAgent ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27), [02](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/02-daemon-and-store.md)).
5. **`asmai stop` draining,** and `--now` ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27), [02](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/02-daemon-and-store.md), [07](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/07-limits-holds-and-visibility.md)).
6. **Terminal disconnect** leaving agents running ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27), [02](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/02-daemon-and-store.md), [03](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/03-provider-sessions-and-terminals.md)).
7. **Delivery crashes:** a crash during a push, or between the push and the pull request ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27), [06](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/06-validation-and-delivery.md)).
8. **Automatic retries** of assignments declared side-effect-free, in place of reconciliation ([02](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/02-daemon-and-store.md), [07](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/07-limits-holds-and-visibility.md)).

## Builds on

[M5 Concurrency and limits](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/milestones/M5-concurrency-and-limits.md): concurrent jobs, holds and leaders on demand, which recovery must restore correctly.

## Rules delivered

Where a rule arrives in parts, the table names the part this milestone delivers.

**[01 Roles and decisions](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/01-roles-and-decisions.md)**

| Rule | | Part delivered here |
| --- | --- | --- |
| 4 | At most one leader process per role at any instant | fencing |
| 7 | What an assignment states | the side-effect-free declaration |
| 29 | Reconciliation is a delegated decision | All |

**[02 Daemon and store](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/02-daemon-and-store.md)**

| Rule | | Part delivered here |
| --- | --- | --- |
| 7 | Every start is a recovery | terminating orphans and reconciling |
| 8 | Opt-in | All |
| 9 | `asmai stop` drains | draining up to the timeout, and --now |
| 11 | Continuing after a stop | recovering an unclean stop |
| 27 | Missing observations | All |
| 28 | Duplicate, late, reordered and conflicting observations | All |
| 30 | Assignment states | needs reconciliation |
| 32 | Automatic retries | All |
| 39 | Generations | All |
| 40 | No stale writer | All |
| 41 | One leader per role | All |
| 44 | Evidence, not proof | checking it in reconciliation |
| 46 | The owning leader reconciles | All |
| 47 | The record | All |
| 48 | When the user is asked | All |
| 49 | Reporting | All |
| 54 | What v1 recovers from | All |
| 55 | Orphans | All |
| 56 | A leader crash | All |
| 57 | A worker crash | All |
| 58 | A provider CLI that fails to start | All |
| 59 | Workers outlive their leader's restart | All |
| 60 | A daemon crash | All |
| 61 | A host reboot | All |
| 62 | A terminal or SSH disconnect | All |
| 63 | Unknown means reconcile | All |

**[05 Repositories and job branches](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/05-repositories-and-job-branches.md)**

| Rule | | Part delivered here |
| --- | --- | --- |
| 41 | Kept for reconciliation | All |

**[06 Validation and delivery](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/06-validation-and-delivery.md)**

| Rule | | Part delivered here |
| --- | --- | --- |
| 40 | A crash during a push | All |
| 41 | A crash between the push and the pull request | All |

**[07 Limits, holds and visibility](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/07-limits-holds-and-visibility.md)**

| Rule | | Part delivered here |
| --- | --- | --- |
| 31 | Silence | All |
| 32 | Draining | All |
| 37 | If Coordination cannot be restored | All |

## Qualification cases

These pass in the harness on Linux at M6's end and have run on the Mac ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27), [11](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/11-qualification-and-proving.md)):

| Case | What is qualified |
| --- | --- |
| C15 | Lost, duplicate, reordered and late hooks and observations |
| C16 | A superseded leader or worker generation is rejected |
| C17 | Agent processes left by a previous daemon are terminated at start |
| C18 | A crash during an effect is recovered through reconciliation |
| C20 | A working dispatch with no observation for 30 minutes becomes unknown |
| C21 | Agent crash: a leader restarts within its bound; a worker's assignment needs reconciliation |
| C22 | Daemon crash |
| C23 | Host reboot with the service installed |
| C24 | Terminal and SSH disconnect |
| C25 | `asmai stop` drains; `asmai stop --now` interrupts |
| C40 | A crash during a push |
| C46 | A leader-opened pull request reconciled as an effect, including a crash between the push and the pull request |

## Demo path

S8, local continuity, on the fixture repository ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27), [11](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/11-qualification-and-proving.md)): during a feature job, the user leaves and comes back to a catch-up; the daemon is killed; and the host reboots with the service installed. Each affected assignment either continues or has a recorded reconciliation, no effect appears twice in the journal or on GitHub, and the job still ends as a tested pull request.

## Exit checks

M6 ends when ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27)):

- its tickets are closed;
- the development tests are green on Linux and on macOS;
- its qualification cases pass in the harness on Linux and have run on the Mac, including the reboot with launchd there; a macOS failure becomes a ticket in M7 and does not hold up M6;
- its demo path has run once on the fixture repository, with the terminal recording kept for Phillip to watch.

## Not in M6

Remote hosts (M7); store migrations, backups and restore (M8).

## Sources

- [Choose the specification's structure and implementation sequence](https://github.com/talvor/AssemblyAI/issues/27#issuecomment-6004852593) (AssemblyAI#27)
- The component documents linked in Rules delivered, and the decision tickets they cite.
- The review of this document: [board](https://github.com/talvor/AssemblyAI/blob/main/.lavish/spec-doc-M6.html) and [answers](https://github.com/talvor/AssemblyAI/blob/main/.lavish/spec-doc-M6-answers.json).
