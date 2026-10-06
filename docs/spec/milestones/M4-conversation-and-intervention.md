# M4 Conversation and intervention

M4 makes the conversation and stepping into agents what the user lives with every day: the status line, the focused job, the catch-up, unsent text and a second attach; taking, releasing and the intervention record; the allow-list of qualified modals; and terminal recordings with replay ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27)).

## What it adds

1. **The status line** in every attached terminal, with the attach client giving the provider one row less ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27), [03](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/03-provider-sessions-and-terminals.md)).
2. **The conversation in full:** one-line updates tagged with their job, the focused job and switching, the catch-up on return, saved unsent text, interrupting Coordination, and a second attach taking over ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27), [04](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/04-conversation-and-lavish.md)).
3. **Taking and releasing an agent,** the Ctrl-] menu, answering native prompts, and the intervention record that reaches the owning leader ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27), [03](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/03-provider-sessions-and-terminals.md)).
4. **The modal allow-list,** starting empty, so any unknown input state holds its agent ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27), [03](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/03-provider-sessions-and-terminals.md)).
5. **Recordings and replay** of every agent terminal, per dispatch ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27), [03](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/03-provider-sessions-and-terminals.md)).

## Builds on

[M3 Decisions and planning](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/milestones/M3-decisions-and-planning.md): decision requests, the Lavish server, all five roles and several assignments per job.

## Rules delivered

Where a rule arrives in parts, the table names the part this milestone delivers.

**[02 Daemon and store](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/02-daemon-and-store.md)**

| Rule | | Part delivered here |
| --- | --- | --- |
| 29 | What each dispatch records | the recording |
| 37 | No boundary, no nudge | while the user holds input or at an unknown input state |

**[03 Provider sessions and terminals](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/03-provider-sessions-and-terminals.md)**

| Rule | | Part delivered here |
| --- | --- | --- |
| 17 | Terminal emulation is AsmAI's | qualified fidelity at reduced height |
| 20 | Missing signals | an interrupted Claude turn |
| 24 | The modal allow-list | All |
| 25 | Unknown input states hold | All |
| 28 | The client draws the screen | one row less |
| 29 | The status line | All |
| 30 | The Ctrl-] menu | All |
| 31 | Terminals | All |
| 32 | Taking input is explicit | All |
| 33 | Drafts are cleared, not kept typing | All |
| 34 | Native prompts | All |
| 35 | While the user holds input | All |
| 36 | Release is explicit | All |
| 37 | What release does | All |
| 38 | The intervention record | All |
| 39 | A newer take moves the hold | All |
| 40 | Only the user takes | All |
| 41 | Every dispatch is recorded | All |
| 42 | Replay | All |
| 43 | Retention | All |

**[04 Conversation and Lavish](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/04-conversation-and-lavish.md)**

| Rule | | Part delivered here |
| --- | --- | --- |
| 4 | Never over the user's text | All |
| 5 | The user's keys always arrive | All |
| 6 | An interrupted automated turn | All |
| 7 | One line per item | All |
| 8 | Job numbers everywhere | All |
| 9 | Escalated once | the status line keeping it visible |
| 12 | One focused job | All |
| 13 | Switching | All |
| 14 | New requests | All |
| 15 | What leaving is | All |
| 16 | Unsent text | All |
| 17 | The catch-up | All |
| 19 | The newest attach takes the conversation | All |

**[07 Limits, holds and visibility](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/07-limits-holds-and-visibility.md)**

| Rule | | Part delivered here |
| --- | --- | --- |
| 33 | No notifications and no dashboard in v1 | All |

**[11 Qualification and proving](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/11-qualification-and-proving.md)**

| Rule | | Part delivered here |
| --- | --- | --- |
| 17 | Terminals | Ghostty locally |

## Qualification cases

These pass in the harness on Linux at M4's end and have run on the Mac ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27), [11](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/11-qualification-and-proving.md)):

| Case | What is qualified |
| --- | --- |
| C6 | Native modals: any input state not on the allow-list (which starts empty) holds the agent instead of being typed over |
| C8 | Taking an agent mid-turn and with an unsent automated draft: wait for the boundary or interrupt; the draft is recorded and cleared |
| C9 | The attach client's rendering of each provider's screen under the status line, at reduced height |
| C10 | Detecting the user's unsent text in the conversation and clearing the input box |
| C12 | Recognising an interrupted Claude turn |
| C13 | A second attach takes over; the older terminal only observes and its unsent text is saved |
| C14 | Terminal recording per dispatch, and replay |

## Demo path

S7's decision and intervention parts, on the fixture repository ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27), [00](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/00-overview.md)):

1. Two jobs run while the user talks to Coordination; each update is one line tagged with its job, and the status line shows the focused job, the running jobs and a pending decision until it is answered.
2. A choice between distinct viable approaches is answered in the conversation, and a request with several questions in Lavish, each on its one answer surface, while independent work continues.
3. The user leaves with unsent text and returns to a catch-up that offers it back; a second terminal then takes the conversation over, and the first only observes.
4. The user takes a worker mid-turn, types a correction and releases it; the intervention record reaches the owning leader, followed by a new dispatch.
5. The user replays that worker's recording.

The demo is recorded with an ordinary terminal recorder, and from M4 on AsmAI's own per-dispatch recordings are kept alongside ([M1](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/milestones/M1-walking-skeleton.md)).

## Exit checks

M4 ends when ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27)):

- its tickets are closed;
- the development tests are green on Linux and on macOS;
- its qualification cases pass in the harness on Linux and have run on the Mac; a macOS failure becomes a ticket in M5 and does not hold up M4;
- its demo path has run once on the fixture repository, with the terminal recording kept for Phillip to watch.

## Not in M4

Job pause, resume and cancel, which complete S7 (M5); holds for limits and providers (M5); fencing and recovery (M6).

## Sources

- [Choose the specification's structure and implementation sequence](https://github.com/talvor/AssemblyAI/issues/27#issuecomment-6004852593) (AssemblyAI#27)
- The component documents linked in Rules delivered, and the decision tickets they cite.
- The review of this document: [board](https://github.com/talvor/AssemblyAI/blob/main/.lavish/spec-doc-M4.html) and [answers](https://github.com/talvor/AssemblyAI/blob/main/.lavish/spec-doc-M4-answers.json).
