# 04 Conversation and Lavish

This document specifies the user's two ways of talking to the factory: the conversation with Coordination in its interactive terminal, and the Lavish pages where reviews and questions are answered. It covers the focused job, one-line updates, the catch-up, unsent text, a second attach, the Lavish server, rendering decision requests and collecting answers. [01 Roles and decisions](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/01-roles-and-decisions.md) specifies which decisions go to which surface and how answers are attributed; [03 Provider sessions and terminals](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/03-provider-sessions-and-terminals.md) specifies the attach client and its status line.

## Rules

### The conversation

1. **Coordination's terminal.** The user's primary conversation is Coordination's interactive provider terminal ([AssemblyAI#15](https://github.com/talvor/AssemblyAI/issues/15)). A bare `asmai`, or `asmai chat`, opens it, starting a stopped factory first and saying so ([AssemblyAI#9](https://github.com/talvor/AssemblyAI/issues/9)).
2. **Not an intervention.** The conversation is not an intervention: leaving it returns Coordination to automated delivery at once, and never pauses anything ([AssemblyAI#9](https://github.com/talvor/AssemblyAI/issues/9), [AssemblyAI#10](https://github.com/talvor/AssemblyAI/issues/10)).
3. **Delivery never waits for the user.** Coordination keeps delivering automated items while the user talks, and delivery never waits on whether the user is present ([AssemblyAI#10](https://github.com/talvor/AssemblyAI/issues/10)).
4. **Never over the user's text.** The daemon never types into the conversation while the user has unsent text in it ([AssemblyAI#9](https://github.com/talvor/AssemblyAI/issues/9)). A nudge waits until the user submits or leaves ([AssemblyAI#10](https://github.com/talvor/AssemblyAI/issues/10)).
5. **The user's keys always arrive.** The user's keys always reach the conversation, including Esc during an automated turn ([AssemblyAI#10](https://github.com/talvor/AssemblyAI/issues/10)).
6. **An interrupted automated turn** is nudged again afterwards. Coordination re-reads the same messages, which reads by message ID make safe, and checks its own recorded `asmai` calls before acting again, so nothing is blindly repeated ([AssemblyAI#10](https://github.com/talvor/AssemblyAI/issues/10)).

### Updates and decisions in the conversation

7. **One line per item.** Each automated item appears as one line tagged with its job number. Anything that needs the user appears as a flagged block. Detail is given when the user asks ([AssemblyAI#10](https://github.com/talvor/AssemblyAI/issues/10)).
8. **Job numbers everywhere.** Every Coordination line about a job carries the job's number ([AssemblyAI#10](https://github.com/talvor/AssemblyAI/issues/10)).
9. **Escalated once.** A decision is presented once, with its answer surface, and the status line keeps it visible until it is answered ([AssemblyAI#10](https://github.com/talvor/AssemblyAI/issues/10), [01](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/01-roles-and-decisions.md)).
10. **Answering here.** A decision whose answer surface is the conversation is answered by the user's message in it. Coordination records the answer with its reading beside the user's witnessed message ([AssemblyAI#10](https://github.com/talvor/AssemblyAI/issues/10), [01](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/01-roles-and-decisions.md)).
11. **Acting on the user's word.** When the user tells Coordination to pause, resume or cancel a job, it acts citing the user's witnessed message ([AssemblyAI#14](https://github.com/talvor/AssemblyAI/issues/14), [07](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/07-limits-holds-and-visibility.md)).

### The focused job

12. **One focused job.** The conversation has one focused job. The user's messages apply to it unless they name another job (`14: …` or `job 14`) ([AssemblyAI#10](https://github.com/talvor/AssemblyAI/issues/10)).
13. **Switching.** "Switch to 14" moves the focus; Coordination says so and loads that job's brief ([AssemblyAI#10](https://github.com/talvor/AssemblyAI/issues/10), [02](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/02-daemon-and-store.md)).
14. **New requests.** A new request opens a job, which takes the focus. Factory-wide questions need no job ([AssemblyAI#10](https://github.com/talvor/AssemblyAI/issues/10)).

### Leaving and coming back

15. **What leaving is.** The user leaves the conversation by detaching, by moving the terminal elsewhere with the Ctrl-] menu, when the terminal or SSH connection drops, or when a newer attach takes the conversation over ([AssemblyAI#10](https://github.com/talvor/AssemblyAI/issues/10), [03](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/03-provider-sessions-and-terminals.md)).
16. **Unsent text.** Leaving saves the user's unsent text to the journal, clears Coordination's input box at the next boundary, and resumes delivery. The catch-up offers the text back; it is never retyped ([AssemblyAI#10](https://github.com/talvor/AssemblyAI/issues/10)).
17. **The catch-up.** When the user returns to the conversation, the attach client first prints a catch-up drawn from the journal, before the live conversation. It covers what changed since the user last left: what is waiting on the user (with Lavish links and the forwarding command), jobs that finished, failed or paused, holds with their causes, agents waiting in their own terminal, input the user still holds, and the saved unsent text. It is one line when nothing changed. Coordination narrates only if asked ([AssemblyAI#10](https://github.com/talvor/AssemblyAI/issues/10), [AssemblyAI#14](https://github.com/talvor/AssemblyAI/issues/14)).
18. **A lost sign-in** shows its native sign-in command in the catch-up as well as the status line ([AssemblyAI#14](https://github.com/talvor/AssemblyAI/issues/14), [07](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/07-limits-holds-and-visibility.md)).

### A second terminal

19. **The newest attach takes the conversation.** The older terminal shows a one-line notice and only observes, and its unsent text is saved as if the user had left ([AssemblyAI#10](https://github.com/talvor/AssemblyAI/issues/10)).

### The Lavish server

20. **The daemon runs it.** The daemon supervises the factory's own Lavish server, running AsmAI's pinned Lavish build, so pending review pages survive agent restarts and a reboot. It runs the server itself, in the foreground, with AsmAI's own Lavish state directory and port, never Lavish's defaults, which the user's personal Lavish uses, and with Lavish's telemetry off. It restarts the server whenever it exits, also checks it periodically and restarts it if it is down, and never relies on Lavish starting a server itself ([AssemblyAI#7](https://github.com/talvor/AssemblyAI/issues/7), [AssemblyAI#9](https://github.com/talvor/AssemblyAI/issues/9), [AssemblyAI#14](https://github.com/talvor/AssemblyAI/issues/14), [ADR 0010](https://github.com/talvor/AssemblyAI/blob/main/docs/adr/0010-lavish-is-a-deno-compiled-executable-built-per-pin.md), [answers](https://github.com/talvor/AssemblyAI/blob/main/.lavish/lavish-delivery-answers.json)).
21. **Local only.** Lavish binds only to localhost: the daemon sets its bind address explicitly, so it never also listens on another interface, such as a Tailscale address ([ADR 0010](https://github.com/talvor/AssemblyAI/blob/main/docs/adr/0010-lavish-is-a-deno-compiled-executable-built-per-pin.md)). On a remote host it is reached through SSH port forwarding, and Coordination gives the page's URL and the forwarding command ([AssemblyAI#7](https://github.com/talvor/AssemblyAI/issues/7)). `asmai lavish` lists the pending review links and the forwarding command, and `--host` forwards the remote Lavish port for the conversation and attach ([AssemblyAI#9](https://github.com/talvor/AssemblyAI/issues/9), [09](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/09-cli-and-configuration.md)).
22. **No agent runs Lavish.** Agents never run Lavish themselves; the lavish skill is not shipped, because the daemon owns Lavish and renders decision requests ([AssemblyAI#17](https://github.com/talvor/AssemblyAI/issues/17)).

### Rendering decision requests

23. **Structured questions.** A decision request whose answer surface is Lavish carries structured questions, each with an id, title, body, options and a recommendation ([AssemblyAI#10](https://github.com/talvor/AssemblyAI/issues/10)). Grilling and Wayfinder questions arrive this way ([AssemblyAI#10](https://github.com/talvor/AssemblyAI/issues/10), [08](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/08-skills-and-agent-instructions.md)).
24. **One standard layout.** The daemon renders the questions in one standard layout, keyed to the decision version, and can tell when every question has an answer ([AssemblyAI#10](https://github.com/talvor/AssemblyAI/issues/10)).
25. **The agent's own content.** The requesting agent may put its own content above the questions, such as a prototype, a diff or a report ([AssemblyAI#10](https://github.com/talvor/AssemblyAI/issues/10)).
26. **A new version, a new page.** A new version of a request reissues its page, and answers from the old page are refused ([AssemblyAI#10](https://github.com/talvor/AssemblyAI/issues/10)).

### Collecting answers

27. **The daemon collects.** The daemon, not an agent, collects what the user sends from a Lavish page: answers, comments and annotations, journaled word for word ([AssemblyAI#10](https://github.com/talvor/AssemblyAI/issues/10)).
28. **Routing.** The daemon routes what it collected to the owning leader's inbox, and Coordination confirms it in the conversation in one line ([AssemblyAI#10](https://github.com/talvor/AssemblyAI/issues/10)).
29. **Partly answered pages.** When the user sends a page with some questions unanswered, the daemon routes what was sent to the owning leader at once. The version stays pending, shown as partly answered, until every question has an answer or the leader issues a new version for the rest ([answers](https://github.com/talvor/AssemblyAI/blob/main/.lavish/spec-doc-04-answers.json)).

## Interfaces

### Commands

| Who | Command | Purpose |
| --- | --- | --- |
| The user | `asmai`, `asmai chat` | Open the conversation, starting a stopped factory first (rule 1) |
| The user | `asmai lavish` | Pending review links and the forwarding command (rule 21) |
| The user | `asmai decisions` | Pending decisions and their answer surfaces; not a way to answer ([01](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/01-roles-and-decisions.md)) |
| The user | `asmai --host <ssh-destination>` | The conversation on a remote host, with Lavish forwarded ([09](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/09-cli-and-configuration.md)) |
| Leaders and workers | `asmai decision request` | A request with structured questions and optional content of the agent's own (rules 23 to 25) |

### Store records

| Record | Holds |
| --- | --- |
| Focus | The conversation's focused job, and each change with the witnessed message that made it |
| Saved unsent text | The text, when it was saved, and whether the catch-up offered it back |
| Last left | When the user last left the conversation, which the catch-up starts from |
| Lavish page | Its decision request and version, its URL, which questions have answers, and whether it is current or replaced |
| Lavish answer | What the user sent, word for word: each answer with its question id and notes, comments and annotations, and when |

## Settings and defaults

None of this document's rules has a setting.

## Failure handling

| Failure | Handling |
| --- | --- |
| The terminal or SSH connection drops | Counts as leaving: unsent text saved, delivery continues (rules 15, 16) |
| Two terminals attach to the conversation | The newer takes it; the older observes (rule 19) |
| The user interrupts an automated turn | Re-nudged and checked, never blindly repeated (rule 6) |
| The Lavish server is down | Restarted when it exits and by the daemon's periodic check; pending pages survive (rule 20) |
| An answer arrives on an old page | Refused; the current page stands (rule 26) |
| An answer in the conversation against an older version | Refused; Coordination presents the current version ([01](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/01-roles-and-decisions.md)) |

## Qualification cases and proving scenarios

- **C10**: detecting the user's unsent text in the conversation and clearing the input box (rules 4, 16).
- **C13**: a second attach takes over; the older terminal only observes and its unsent text is saved (rule 19).
- **C9** and **C11** ([03](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/03-provider-sessions-and-terminals.md)) and **C47** ([09](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/09-cli-and-configuration.md)) cover the status line, witnessed messages, and Lavish through port forwarding, which this document relies on.
- **S1** and **S3**: Planning's questions reach the user in Lavish and the answers are recorded word for word.
- **S7**: a choice answered in the conversation and a request with several questions answered in Lavish.
- **S8**: the catch-up shown when the user returns.
- **S9**: a Lavish answer given through the forwarded port, and the SSH drop leaving delivery running.

## Sources

- [Choose factory hosting and lifecycle](https://github.com/talvor/AssemblyAI/issues/7#issuecomment-5976506834) (AssemblyAI#7)
- [Define CLI setup and management experience](https://github.com/talvor/AssemblyAI/issues/9#issuecomment-5979143255) (AssemblyAI#9)
- [Explore terminal conversation and Lavish decision flow](https://github.com/talvor/AssemblyAI/issues/10#issuecomment-5989237516) (AssemblyAI#10), with its [conversation prototype](https://github.com/talvor/AssemblyAI/blob/main/.lavish/conversation-flow.html) and [answers](https://github.com/talvor/AssemblyAI/blob/main/.lavish/conversation-answers.json)
- [Define v1 acceptance scenarios and evidence](https://github.com/talvor/AssemblyAI/issues/12#issuecomment-5993314453) (AssemblyAI#12)
- [Define operating limits and visibility](https://github.com/talvor/AssemblyAI/issues/14#issuecomment-5991304507) (AssemblyAI#14)
- [Choose runtime adapters and authentication](https://github.com/talvor/AssemblyAI/issues/15#issuecomment-5968867443) (AssemblyAI#15)
- [Choose skill bundles and update policy](https://github.com/talvor/AssemblyAI/issues/17#issuecomment-5992055697) (AssemblyAI#17)
- [ADR 0004](https://github.com/talvor/AssemblyAI/blob/main/docs/adr/0004-attach-client-draws-status-line.md) and the [glossary](https://github.com/talvor/AssemblyAI/blob/main/GLOSSARY.md): Conversation, Focused job, Catch-up, Answer surface, Witnessed message.
- The [Lavish and skill delivery review](https://github.com/talvor/AssemblyAI/blob/main/.lavish/lavish-delivery-answers.json) (2026-10-07), with the [Lavish deno compile check](https://github.com/talvor/AssemblyAI/blob/main/docs/research/lavish-deno-compile-check.md) and [ADR 0010](https://github.com/talvor/AssemblyAI/blob/main/docs/adr/0010-lavish-is-a-deno-compiled-executable-built-per-pin.md): Lavish built as a Deno-compiled executable when its pin moves, and how the daemon runs it.
- The review of this document: [questions](https://github.com/talvor/AssemblyAI/blob/main/.lavish/spec-doc-04-round1-questions.json) and [answers](https://github.com/talvor/AssemblyAI/blob/main/.lavish/spec-doc-04-answers.json).
