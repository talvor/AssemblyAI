# Round 2 clarification

Phillip's message (verbatim): "Does the daemon know what jobs each leader have inflight?"

Reply posted in Lavish:

**Yes.** Everything that makes a job in flight for a role is recorded through the daemon, which is the only writer to the factory's store (Define work state and coordination contracts):

- **Handoffs** sent to the role, open until accepted, declined, or their job ends
- **Assignments** the role's leader owns, with their state
- **Decision requests** the leader made that you have not answered yet
- **Inbox messages** waiting for the role, such as a worker's result or your answer

Each record names its job, and every `asmai` call is checked against the caller's role. So the daemon can see, per role and per job, exactly R2-Q2's criteria. It also knows from hooks whether the leader is mid-turn, and it stops a leader only at a boundary.

What it cannot see is work a leader has decided on but not yet recorded, such as a handoff it is about to send. The boundary rule and the idle grace cover that.

Round 2's questions are still open on the page.
