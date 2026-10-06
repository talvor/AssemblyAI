# 07 Limits, holds and visibility

This document specifies the factory's operating limits and how the user sees what is happening: worker caps and the queue, allowance, provider failures and lost sign-in, choosing a provider before first dispatch, holds, work that keeps failing, pausing, resuming and cancelling a job, timeouts, `asmai status`, disk use and logs. v1 has no notifications and no browser dashboard; everything here is visible in the status line, the catch-up and `asmai status`.

## Rules

### Spending and allowance

1. **No spending without a grant.** The spending budget is zero unless granted ([01](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/01-roles-and-decisions.md), [AssemblyAI#14](https://github.com/talvor/AssemblyAI/issues/14)).
2. **Allowance is not budgeted per job.** Allowance, the usage a subscription permits in its rolling windows, is paced by the worker caps, and the rules below apply when a provider reports its limit. There is no per-job token budget ([AssemblyAI#14](https://github.com/talvor/AssemblyAI/issues/14)).
3. **Recorded and shown.** AsmAI records token counts per dispatch and shows each provider's allowance used and reset times in `asmai status`, read from the signals each provider version gives, which are qualified ([AssemblyAI#14](https://github.com/talvor/AssemblyAI/issues/14), [AssemblyAI#12](https://github.com/talvor/AssemblyAI/issues/12)).
4. **No reserve.** The factory uses allowance until the provider stops it; nothing is kept back for the user's own use ([AssemblyAI#14](https://github.com/talvor/AssemblyAI/issues/14)).

### Worker caps and the queue

5. **A cap per provider** limits the workers whose dispatch is in progress. Workers waiting on their leader, on the user or on a hold, and a paused job's workers, do not count, and their sessions stay alive. Leaders do not count ([AssemblyAI#14](https://github.com/talvor/AssemblyAI/issues/14)).
6. **No other concurrency limit.** There is no cap on jobs, on jobs per repository, or on CPU or memory; the worker caps are the control ([AssemblyAI#14](https://github.com/talvor/AssemblyAI/issues/14)).
7. **The queue.** An assignment that finds its provider's cap full is queued, first come first served across jobs, and shown as queued to its leader and in the status line ([AssemblyAI#14](https://github.com/talvor/AssemblyAI/issues/14)).
8. **No overflow.** A queued assignment waits for its configured provider and never overflows to the other one. A full cap is not a lack of access ([AssemblyAI#14](https://github.com/talvor/AssemblyAI/issues/14)).

### Choosing a provider

9. **Staffing.** Each role has a provider and model for its leader and a default for its workers, and an assignment may override them ([AssemblyAI#15](https://github.com/talvor/AssemblyAI/issues/15), [AssemblyAI#9](https://github.com/talvor/AssemblyAI/issues/9), [09](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/09-cli-and-configuration.md)).
10. **Fallback before first dispatch only.** When an assignment's configured provider lacks access before its first dispatch, it uses the other configured, compatible provider automatically; the selection is recorded and reported ([AssemblyAI#15](https://github.com/talvor/AssemblyAI/issues/15)). The configuration names one default model for each provider, and falling back uses the other provider with its default model, for any role. Compatible means in the qualified combination, signed in and not held; a provider with no default model configured is not available for fallback ([answers](https://github.com/talvor/AssemblyAI/blob/main/.lavish/spec-doc-07-answers.json)).
11. **No suitable provider.** If no suitable provider is available, the affected work holds and independent authorized work continues ([AssemblyAI#15](https://github.com/talvor/AssemblyAI/issues/15)).
12. **After first dispatch, the user decides.** After an assignment's first dispatch, changing its provider needs the user's decision, even if nothing has been output or done yet. Resuming on the same provider once access returns needs none ([AssemblyAI#15](https://github.com/talvor/AssemblyAI/issues/15), [01](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/01-roles-and-decisions.md)).
13. **A leader's provider.** A leader that starts while its role has no open work in any job, paused or not, counts as before first dispatch: it may start on the other configured, compatible provider automatically, which is recorded and shown in status, and it returns to its configured provider at a later start once access is back. While its role has open work, changing its provider needs the user's decision ([AssemblyAI#14](https://github.com/talvor/AssemblyAI/issues/14), [AssemblyAI#15](https://github.com/talvor/AssemblyAI/issues/15)).
14. **An approved replacement** reconciles the effects already made and keeps the assignment's context, its grants, its pending decisions and its single owner. Provider conversations are never assumed to carry across providers ([AssemblyAI#15](https://github.com/talvor/AssemblyAI/issues/15)). The user can also approve one by confirming the change in `asmai config apply` ([AssemblyAI#9](https://github.com/talvor/AssemblyAI/issues/9), [09](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/09-cli-and-configuration.md)).

### Allowance used up

15. **Hold, then resume at the reset.** When a provider reports its allowance used up, its agents stop at their boundary and hold. At the reported reset time, AsmAI resumes each on the same provider with a new dispatch and tells its owning leader ([AssemblyAI#14](https://github.com/talvor/AssemblyAI/issues/14)).
16. **Queued work** not yet dispatched may start on the other configured, compatible provider; otherwise it waits for the reset ([AssemblyAI#14](https://github.com/talvor/AssemblyAI/issues/14)).
17. **A leader with open work** on that provider leaves its role waiting until the reset. Coordination offers the user the provider change; if Coordination itself is held, the status line offers it ([AssemblyAI#14](https://github.com/talvor/AssemblyAI/issues/14)).

### Provider failures and lost sign-in

18. **A reported error resumes with backoff.** When a provider positively reports that a turn ended on an error, the daemon resumes the same live session with a new dispatch, with bounded retries and a doubling wait. Claude Code reports this through its StopFailure hook; the Codex signal is qualified separately. The agent can see what it already did, so this is not a blind retry. An unexplained stop is still unknown ([AssemblyAI#14](https://github.com/talvor/AssemblyAI/issues/14), [02](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/02-daemon-and-store.md)).
19. **Unavailable.** Past that bound, or while the provider stays down, the provider is marked unavailable. Its agents hold, queued work may use the other provider before first dispatch, and the daemon rechecks the provider periodically and resumes the held agents when it answers ([AssemblyAI#14](https://github.com/talvor/AssemblyAI/issues/14)).
20. **A lost or expired sign-in** holds the same way. The status line, the catch-up and `asmai status` show the native sign-in command, and work resumes when a recheck sees the sign-in restored. AsmAI never starts a sign-in ([AssemblyAI#14](https://github.com/talvor/AssemblyAI/issues/14), [AssemblyAI#15](https://github.com/talvor/AssemblyAI/issues/15)).

### Holds

21. **What a hold is.** A hold is a stop the factory places on work when a limit is reached, recorded with its cause, and lifted when the cause clears or is resolved. A pause is always the user's ([AssemblyAI#14](https://github.com/talvor/AssemblyAI/issues/14)).
22. **The holds in v1**, with where each is specified:

| Cause | What holds | Lifted when | Where |
| --- | --- | --- | --- |
| Allowance used up | The provider's agents | The reported reset | Rule 15 |
| Provider unavailable | Its agents | A recheck finds it answering | Rule 19 |
| Sign-in lost or expired | That provider's agents | A recheck finds sign-in restored | Rule 20 |
| No suitable provider before first dispatch | The affected work | A provider becomes available | Rule 11 |
| Leader restart bound passed | The role | The leader is restored | [02](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/02-daemon-and-store.md) |
| Unknown input state | That agent | The user resolves it | [03](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/03-provider-sessions-and-terminals.md) |
| Provider CLI upgraded itself | That agent, at its next restart | The combination is qualified | [03](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/03-provider-sessions-and-terminals.md) |
| Dispatch limit reached | The assignment | The user's decision | Rule 23 |
| Failed-validation limit reached | The job's delivery | The user's decision | [06](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/06-validation-and-delivery.md) |
| No first CI check in time | The job | The user's answer | [06](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/06-validation-and-delivery.md) |
| Below the free-space floor | Assignments waiting for a workspace | Space returns | Rule 41 |

### Work that keeps failing

23. **The dispatch limit.** An assignment that reaches the dispatch limit without acceptance holds, and its owning leader escalates to the user with what was tried. The rest of the job and other jobs continue ([AssemblyAI#14](https://github.com/talvor/AssemblyAI/issues/14)).
24. **What counts.** Only dispatches that redo or correct the work count: a rejection, a re-dispatch chosen in reconciliation, and a new dispatch after the user typed during an intervention. Resumptions do not count: after an allowance reset, a reported provider error, a pause or an `asmai stop` ([AssemblyAI#14](https://github.com/talvor/AssemblyAI/issues/14), [02](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/02-daemon-and-store.md)).
25. **Side-effect-free retries.** An assignment declared side-effect-free is retried automatically at most the retry limit ([AssemblyAI#14](https://github.com/talvor/AssemblyAI/issues/14), [AssemblyAI#8](https://github.com/talvor/AssemblyAI/issues/8)).
26. **Failed validations** of a job are limited separately ([06](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/06-validation-and-delivery.md)).

### Pausing, resuming and cancelling a job

27. **Who.** The user pauses, resumes or cancels a job with `asmai job pause|resume|cancel`, or by telling Coordination, which acts citing the user's witnessed message. No other agent pauses or cancels a whole job. There is no factory-wide pause beyond `asmai stop` ([AssemblyAI#14](https://github.com/talvor/AssemblyAI/issues/14)).
28. **Pause.** `asmai job pause` dispatches nothing new for the job ([AssemblyAI#14](https://github.com/talvor/AssemblyAI/issues/14)):
    - running turns finish to their boundary and stop;
    - the job's workers keep their sessions without counting against the cap, and queued assignments stay queued;
    - pending decisions stay answerable, and the answers apply on resume;
    - leaders do not act on the job until it resumes, and its work does not keep a leader running.
29. **Resume.** Each stopped assignment continues with a new dispatch after its owning leader reloads the job's brief. Resume also lifts a hold on the job's work once the hold's cause has cleared ([AssemblyAI#14](https://github.com/talvor/AssemblyAI/issues/14)).
30. **Cancel.** `asmai job cancel` asks for confirmation, then ([AssemblyAI#14](https://github.com/talvor/AssemblyAI/issues/14), [AssemblyAI#8](https://github.com/talvor/AssemblyAI/issues/8)):
    - stops all of the job's work at a boundary (`--now` interrupts instead);
    - withdraws its pending decisions;
    - ends its assignments as cancelled;
    - reports the effects, the pushed branches and any open pull request, which is left open for the user to close; effects are reported, never claimed undone.

    The job then ends.

### Timeouts

31. **Silence.** A working dispatch with no correlated observation for the silence timeout becomes unknown ([AssemblyAI#14](https://github.com/talvor/AssemblyAI/issues/14), [02](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/02-daemon-and-store.md)).
32. **Draining.** `asmai stop` drains for up to the drain timeout, then interrupts the rest ([AssemblyAI#14](https://github.com/talvor/AssemblyAI/issues/14), [02](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/02-daemon-and-store.md)).

### Visibility

33. **No notifications and no dashboard in v1.** Holds and other events appear in the status line, in the catch-up when the user returns, and in `asmai status`. Both are v2 candidates, and the notification design to start v2 from is kept in [AssemblyAI#14](https://github.com/talvor/AssemblyAI/issues/14).
34. **`asmai status` shows** ([AssemblyAI#14](https://github.com/talvor/AssemblyAI/issues/14)):
    - the daemon and its version, and platform certification;
    - each leader: running, stopped with no work, restarting, or held;
    - workers in progress against each provider's cap, and queued assignments;
    - each provider's state: ready, with allowance used and reset times; held until a reset; unavailable; or signed out;
    - the Lavish server, paused jobs, and holds with their causes;
    - disk use (rule 39);
    - added and repository skills, marked as the user's or the repository's and unqualified ([AssemblyAI#17](https://github.com/talvor/AssemblyAI/issues/17), [08](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/08-skills-and-agent-instructions.md)).
35. **`asmai status --check`** exits non-zero when anything needs the user, so the user can wire it into their own monitoring, for example over SSH. There is still no network listener ([AssemblyAI#14](https://github.com/talvor/AssemblyAI/issues/14)).
36. **Periodic checks.** The daemon periodically checks the Lavish server (restarting it if it is down), provider sign-in, free disk and leader liveness, and reports problems through the status line, the catch-up and `asmai status` ([AssemblyAI#14](https://github.com/talvor/AssemblyAI/issues/14)).
37. **If Coordination cannot be restored,** `asmai status` reports it ([AssemblyAI#7](https://github.com/talvor/AssemblyAI/issues/7)).

### Disk

38. **No quotas.** There are no per-job disk quotas ([AssemblyAI#14](https://github.com/talvor/AssemblyAI/issues/14)).
39. **Disk use is reported** by clones, workspaces, kept workspaces, recordings, the store, and the pre-migration backups ([AssemblyAI#14](https://github.com/talvor/AssemblyAI/issues/14), [AssemblyAI#20](https://github.com/talvor/AssemblyAI/issues/20)).
40. **Cleaning.** Kept workspaces are removed with `asmai job clean <n>`, which is refused while the job is open ([AssemblyAI#14](https://github.com/talvor/AssemblyAI/issues/14), [05](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/05-repositories-and-job-branches.md)).
41. **The free-space floor.** Below the floor on the state directory's volume, the daemon creates no new workspace, so the assignments waiting for one hold; they continue when space returns ([AssemblyAI#14](https://github.com/talvor/AssemblyAI/issues/14)).

### Logs

42. **The daemon's log** rotates through a fixed number of files of a fixed size and is read with `asmai log [--follow]` ([AssemblyAI#14](https://github.com/talvor/AssemblyAI/issues/14)).
43. **Elsewhere.** Terminal recordings and provider transcripts are specified in [03](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/03-provider-sessions-and-terminals.md), and the journal, which is append-only and kept in full and never records environment variables, in [02](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/02-daemon-and-store.md) ([AssemblyAI#14](https://github.com/talvor/AssemblyAI/issues/14)).

## Interfaces

### Commands

| Who | Command | Purpose |
| --- | --- | --- |
| The user | `asmai status [--check]` | Health, and an exit code for monitoring (rules 34, 35) |
| The user | `asmai job pause\|resume\|cancel <n>` | Pause, resume or cancel a job (rules 27 to 30); `cancel --now` interrupts |
| The user | `asmai job clean <n>` | Remove an ended job's kept workspaces (rule 40) |
| The user | `asmai log [--follow]` | Read the daemon's log (rule 42) |
| Every agent | `asmai status` | The same view, read-only |

### Store records

| Record | Holds |
| --- | --- |
| Hold | Its cause, what it holds, when it started, and how and when it was lifted |
| Queue entry | The assignment, its provider, and when it was queued |
| Provider state | Each provider's state, allowance used, reset times, and the last recheck |
| Provider selection | An automatic fallback or a user-approved replacement, with its reason |
| Pause, resume, cancel | The job, who asked, and the witnessed message when Coordination acted |
| Dispatch count | Per assignment, the dispatches that count toward the limit (rule 24) |

### Files

- **The daemon's log**, rotated (rule 42).

## Settings and defaults

All are factory-wide settings in the configuration file, shown by `asmai config show`; [09](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/09-cli-and-configuration.md) names the fields ([AssemblyAI#14](https://github.com/talvor/AssemblyAI/issues/14)).

| Setting | Default | Rule |
| --- | --- | --- |
| Default model, Claude and Codex | None; set by the user | 10 |
| Worker cap, Claude | 3 | 5 |
| Worker cap, Codex | 3 | 5 |
| Resumes after a reported provider error | 5, waiting 30 seconds and doubling to at most 8 minutes | 18 |
| Recheck of an unavailable provider or a lost sign-in | Every 5 minutes | 19, 20 |
| Dispatch limit per assignment | 5 dispatches without acceptance | 23 |
| Automatic retries of a side-effect-free assignment | 2 | 25 |
| Silence timeout | 30 minutes | 31 |
| Drain timeout | 10 minutes | 32 |
| Free-space floor | 5 GB on the state directory's volume | 41 |
| Daemon log | 5 files of 20 MB | 42 |

The leader idle grace and the leader restart bound are in [02](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/02-daemon-and-store.md), the failed-validation limit and the first-check wait in [06](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/06-validation-and-delivery.md), and recording retention in [03](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/03-provider-sessions-and-terminals.md).

## Failure handling

The holds table (rule 22) is this document's failure handling: every limit reached stops only the work it concerns, records why, shows it to the user, and lifts when its cause clears or is resolved. Independent work always continues.

## Qualification cases and proving scenarios

- **C26**: an expired or revoked sign-in holds work, shows the native sign-in command, and resumes when sign-in is back (rule 20).
- **C27**: allowance used and reset times, for each provider (rule 3).
- **C28**: allowance used up: agents hold, then resume at the reset (rule 15). Replayed from recorded payloads.
- **C29**: a reported provider error resumes with backoff; past the bound the provider is unavailable (rules 18, 19).
- **C30**: fallback to the other provider only before first dispatch, including a leader's on-demand start; afterwards the user is asked (rules 10 to 13).
- **C32**: below the free-space floor no new workspace is created (rule 41).
- **C20** and **C25**: the silence and drain timeouts ([02](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/02-daemon-and-store.md)).
- **S5**: full worker caps queue assignments, shown as queued, started first come first served, and never overflowing to the other provider.
- **S7**: one job paused and resumed, and another cancelled, each leaving its reported state.
- **S1** to **S9**: each scenario's record states the allowance it used.

## Sources

- [Choose factory hosting and lifecycle](https://github.com/talvor/AssemblyAI/issues/7#issuecomment-5976506834) (AssemblyAI#7)
- [Define work state and coordination contracts](https://github.com/talvor/AssemblyAI/issues/8#issuecomment-5976668034) (AssemblyAI#8)
- [Define CLI setup and management experience](https://github.com/talvor/AssemblyAI/issues/9#issuecomment-5979143255) (AssemblyAI#9)
- [Define v1 acceptance scenarios and evidence](https://github.com/talvor/AssemblyAI/issues/12#issuecomment-5993314453) (AssemblyAI#12)
- [Define operating limits and visibility](https://github.com/talvor/AssemblyAI/issues/14#issuecomment-5991304507) (AssemblyAI#14), with its [answers](https://github.com/talvor/AssemblyAI/blob/main/.lavish/limits-answers.json)
- [Choose runtime adapters and authentication](https://github.com/talvor/AssemblyAI/issues/15#issuecomment-5968867443) (AssemblyAI#15)
- [Choose skill bundles and update policy](https://github.com/talvor/AssemblyAI/issues/17#issuecomment-5992055697) (AssemblyAI#17)
- [Choose license, release packaging and upgrade migration](https://github.com/talvor/AssemblyAI/issues/20#issuecomment-6004145724) (AssemblyAI#20)
- The [glossary](https://github.com/talvor/AssemblyAI/blob/main/GLOSSARY.md): Allowance, Hold.
- The review of this document: [questions](https://github.com/talvor/AssemblyAI/blob/main/.lavish/spec-doc-07-round1-questions.json) and [answers](https://github.com/talvor/AssemblyAI/blob/main/.lavish/spec-doc-07-answers.json).
