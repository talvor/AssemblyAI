## Resolution — confirmed by Phillip in Lavish

Phillip answered three live Lavish rounds on 2026-10-05 (21 questions with recommendations, plus one clarifying question of his own), then confirmed the complete resolution below. This is a planning decision; it authorizes no implementation.

### Budgets
- The **spending budget** is zero by default, so any action that would spend money needs Phillip's grant naming the amount and scope.
- **Allowance**, the usage a subscription permits in its rolling windows, is not budgeted per job. Worker caps pace it, and the rules below apply when a provider reports its limit.
- AsmAI records token counts per dispatch and shows each provider's allowance used and reset times in `asmai status`.
- There is no reserve for Phillip's own use: the factory uses allowance until the provider stops it.

### Concurrency
- Each provider has a cap on workers whose dispatch is in progress, by default 3 for Claude and 3 for Codex. Workers waiting on their leader, on Phillip or on a hold, and a paused job's workers, do not count, and their sessions stay alive. Leaders do not count.
- There is no cap on jobs or per repository.
- An assignment that finds its provider's cap full is queued, first come first served across jobs, and shown as queued to its leader and in the status line. It waits for its configured provider and never overflows to the other one. A full cap is not lack of access.

### Leaders on demand
- Coordination always runs while the factory runs.
- The daemon starts any other role's leader when a message for that role arrives and no leader is running. Coordination ensures a leader by handing work to its role and never manages processes.
- The daemon stops a leader at a boundary, after a 10-minute idle grace, once its role has no open work in any unpaused job: no open handoffs to it, no assignments it owns, no decision it requested still pending, and nothing in its inbox. The daemon knows all of this from its store, where every handoff, assignment, decision request and inbox message is recorded with its job and role. A role with no running leader and no work is normal, not a fault.
- At most one leader per role still holds. A crashed leader with open work still restarts, up to 3 times within 15 minutes, before its role holds.
- **A leader's provider.** A leader that starts while its role has no open work in any job, paused or not, counts as before first dispatch. It may start on the other configured, compatible provider automatically; this is recorded and shown in status, and it returns to its configured provider at a later start once access is back. While its role has open work, changing its provider needs Phillip's decision.

### Allowance used up
- Agents on that provider stop at their boundary and **hold**. At the reported reset time AsmAI resumes each on the same provider with a new dispatch and tells its owning leader.
- Queued assignments not yet dispatched may start on the other configured, compatible provider; otherwise they wait for the reset.
- A leader with open work on that provider leaves its role waiting until the reset. Coordination, or the status line if Coordination itself is held, offers Phillip the provider change.

### Provider failures
- When a provider positively reports that a turn ended on an error, the daemon resumes the same live session with a new dispatch, up to 5 times, waiting 30 seconds and doubling to at most 8 minutes. Claude Code reports this through its StopFailure hook; the Codex signal is still to be qualified. The agent can see what it already did, so this is not a blind retry. An unexplained stop is still unknown.
- Past that bound, or while the provider stays down, the provider is marked unavailable. Its agents hold, queued work may use the other provider before first dispatch, and the daemon rechecks every 5 minutes and resumes held agents when it answers.
- A lost or expired sign-in holds the same way. The status line, catch-up and `asmai status` show the native sign-in command, and work resumes when a recheck sees sign-in restored. AsmAI never starts a login.
- A pinned CLI that fails to start follows the leader crash rule for a leader; a worker's assignment needs reconciliation.

### Work that keeps failing
- An assignment that reaches 5 dispatches without acceptance holds, and its owning leader escalates to Phillip with what was tried. The rest of the job and other jobs continue.
- Only dispatches that redo or correct the work count:
  - a rejection
  - a re-dispatch chosen in reconciliation
  - a new dispatch after Phillip typed during an intervention

  Resumptions after an allowance reset, a reported provider error, a pause or `asmai stop` do not count.
- A side-effect-free assignment is retried automatically at most twice.

### Job pause, resume and cancel
- **Pause.** `asmai job pause` dispatches nothing new for the job.
  - Running turns finish to their boundary and stop.
  - The job's workers keep their sessions without counting against the cap, and queued assignments stay queued.
  - Pending decisions stay answerable, and answers apply on resume.
  - Leaders do not act on the job until it resumes, and its work does not keep a leader running.
- **Resume.** Each stopped assignment continues with a new dispatch after its owning leader reloads the job's brief. Resume also lifts a hold on the job's work once the hold's cause has cleared.
- **Cancel.** `asmai job cancel` asks for confirmation, then:
  - stops all of the job's work at a boundary (`--now` interrupts instead)
  - withdraws its pending decisions
  - ends its assignments as cancelled
  - reports effects, pushed branches and any open PR, which is left open for Phillip to close

  The job then ends.
- **Who.** Phillip pauses, resumes or cancels with `asmai job pause|resume|cancel`, or by telling Coordination, which acts citing his witnessed message. No other agent pauses or cancels a whole job. There is no factory-wide pause beyond `asmai stop`.

### Timeouts
- A working dispatch with no correlated observation for 30 minutes becomes unknown.
- `asmai stop` drains for up to 10 minutes, then interrupts the rest.

### While Phillip is away
- v1 has **no notifications** and **no browser dashboard**.
- Holds and other events appear in the status line, in the catch-up on return, and in `asmai status`.
- Both features are recorded as v2 candidates in the map's Out of scope section.
- The notification design from round 1 is kept here for v2:
  - a notify command Phillip configures, which the daemon runs on the host when something needs him or a job ends
  - sent only while no terminal is attached, and batched
  - carries the event, the job number and title, and a decision's title, never code or diffs
  - any credentials live in his command, not in AsmAI

### Health
- `asmai status` shows:
  - the daemon and its version, and platform certification
  - each leader: running, stopped with no work, restarting, or held
  - workers in progress against each provider's cap, and queued assignments
  - each provider's state: ready with allowance used and reset times, held until a reset, unavailable, or signed out
  - the Lavish server, paused jobs and holds with their causes, and disk use
- `asmai status --check` exits non-zero when anything needs Phillip, so he can wire it into his own monitoring, for example over SSH. There is still no network listener.
- The daemon periodically checks the Lavish server (restarting it if it is down), provider sign-in, free disk and leader liveness. It reports problems through the status line, catch-up and status.

### Disk and host
- There are no per-job quotas. Status reports disk use by clones, workspaces, kept workspaces, recordings and the store.
- Below 5 GB free on the state directory's volume, the daemon creates no new workspaces, so their assignments hold. It continues when space returns.
- Kept workspaces are removed with `asmai job clean <n>`, which is refused while the job is open.
- There are no CPU or memory limits; the worker caps are the control.

### Logs
- The daemon's operational log rotates through 5 files of 20 MB and is read with `asmai log [--follow]`.
- Every agent terminal is recorded per dispatch and compressed. Recordings are replayed with `asmai replay <agent> [--dispatch <id>]` and deleted 14 days after their job ends.
- Provider transcripts stay where the provider writes them, and the journal records their location per dispatch.
- Nothing records environment variables. The journal stays append-only and is kept in full.

### Settings
Every number above is a factory-wide setting in the configuration file, shown by `asmai config show`. The field names stay in the configuration-schema fog.

### Changes to earlier decisions
- [Choose factory hosting and lifecycle](https://github.com/talvor/AssemblyAI/issues/7) assumed every role's leader runs all the time. Now only Coordination does, and other leaders run on demand as above. Its rules for at most one leader per role, fencing and leader crashes are unchanged.
- [Choose runtime adapters and authentication](https://github.com/talvor/AssemblyAI/issues/15) allowed a leader's automatic provider selection only before the leader first starts. That now also applies to any start while its role has no open work.
- The factory's own stops that earlier tickets called pauses are **holds**, such as a role after repeated leader crashes or an agent at unknown input. A pause is always Phillip's.

### Domain model
- The glossary gains **Allowance** and **Hold**.
- No ADR is recorded; none of these choices is hard to reverse.

### Facts checked on this host
These were observed, not qualified:
- Claude Code 2.1.283 passes a status-line command `rate_limits.five_hour` and `rate_limits.seven_day`, each with `used_percentage` and `resets_at`. Its `StopFailure` hook fires when a turn ends on an API error, with `error` and `error_details`.
- Codex 0.157.0 writes `rate_limits` (`used_percent`, `window_minutes`, `resets_at`) in its session log's `token_count` events.
- Both record token counts per turn.

### Deferred to existing tickets
[Define v1 acceptance scenarios and evidence](https://github.com/talvor/AssemblyAI/issues/12) qualifies the following, per provider version:
- the allowance figures and the reported-error signals, including Codex's equivalent of StopFailure
- resuming after a reported error
- holding and resuming at a reset
- before-first-dispatch fallback on a limited provider, including a leader's on-demand start
- leaders starting when a message arrives and stopping after the idle grace
- the free-space floor
- terminal recording and replay

### Map follow-through
- No new ticket.
- The browser-dashboard fog item is removed.
- The Out of scope section gains one line: notifications while Phillip is away and a browser dashboard are v2 candidates.
- The configuration-schema fog item notes that the operating-limit settings and their defaults are settled here.

### Evidence
The board, question and answer files and the glossary change were produced in a disposable worktree and are being archived separately, so the answers are recorded verbatim here:
- **Round 1:**
  - Q1 A (spending budget zero unless granted; no per-job token budgets; allowance shown in status)
  - Q2 A (worker cap per provider; leaders exempt; extra assignments queue first come first served), note: "Also, I do not think we need to have all leaders running all the time.  We need at least the coordinator running, and the coordinator will need to ensure required leaders to complete the in flight jobs are running.  The leaders can be removed when they are no longer needed."
  - Q3 A (hold that provider's agents, resume at reset; queued work may use the other provider)
  - Q4 **C: no reserve**
  - Q5 A (daemon resumes the live session after a reported error; outages and lost sign-in hold, then resume automatically)
  - Q6 A (per-assignment dispatch limit; hold it and escalate)
  - Q7 A (pause, resume and cancel as listed)
  - Q8 **D: no notifications in v1**, note: "Document this as a future v2 feature"
  - Q9 A (full status, a --check exit code, periodic daemon checks)
  - Q10 A (free-space floor, reporting and a clean command; no per-job quotas)
  - Q11 A (rotating daemon log; per-dispatch terminal recordings deleted after the job ends)
- **Round 2:**
  - First a question: "Does the daemon know what jobs each leader have inflight?" Answered in Lavish: yes, from the store's handoffs, assignments, decision requests and inbox messages, each recorded with its job and role.
  - R2-Q1 A (the daemon starts a leader when a message for its role arrives, and stops it when no longer needed)
  - R2-Q2 A (when its role has no open work in any unpaused job, after an idle grace period)
  - R2-Q3 A (only dispatches that redo or correct the work)
  - R2-Q4 A (default limits approved as listed)
  - R2-Q5 A (no dashboard in v1; a v2 candidate like notifications)
  - R2-Q6 A (the map's Out of scope section plus the design kept in the resolution)
  - R2-Q7 A (add Allowance and Hold as written)
- **Round 3:**
  - R3-Q1 **B: a start with no open work counts as before first dispatch**
  - R3-Q2 A (only workers with a dispatch in progress)
  - R3-Q3 A (it waits for its configured provider)
- **Confirmation:** CONFIRM "Confirm and record", on a page holding the full resolution above.
