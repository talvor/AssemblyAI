# Research Firstmate and Openrig coordination patterns

Status: resolved
Assignee: Phillip
Researcher: research_references
Type: research
Label: wayfinder:research
Parent: ../map.md

## Question

What mechanisms in the exact Firstmate and Openrig projects support leader/worker delegation, inter-agent communication, durable context, and unattended work? Identify primary-source evidence, limitations, and reusable ideas without selecting a dependency. Firstmate is locally available at /home/phillip/firstmate with origin https://github.com/kunchenguid/firstmate. Verify the intended Openrig identity; flag ambiguity rather than guessing.

## Answer

Resolved by source inspection on 2026-10-03: [Reference systems findings](../research/reference-systems.md).

Firstmate combines a single supervisor contract with isolated workers, durable filesystem inboxes, acknowledgement/retry, and reconciliation of live state against task records. The likely OpenRig reference, mvschwarz/openrig, combines persistent seats with SQLite-owned work, recorded handoffs, and transition-derived wake escalation. Both separate durable obligations from notifications; neither source inspection establishes live reliability or chooses a dependency.

Identity remains explicitly unresolved: mvschwarz/openrig fits the user's description, but EliasOenal/OpenRig is another agent runtime. Human confirmation is required before treating the likely match as the intended product.

Context pointer: isolated research repository `/tmp/aifactory-reference-research`, branch `research/reference-systems`, commit `1ce67ef9f88a5f8b040d4dc0cde4ca48c3e83853`, file `reference-systems.md`. The workspace's Git directory was unavailable for writing. This throwaway commit is unsigned because the inherited signing agent was inaccessible; no user Git configuration was changed.

## Comments

Phillip confirmed in the live Lavish map review that the intended reference is https://github.com/mvschwarz/openrig. The identity caveat in the research snapshot is now resolved.
