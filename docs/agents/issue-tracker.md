# Issue tracker: GitHub

Issues and specs live in GitHub Issues for talvor/AssemblyAI.

Prefer gh-axi for GitHub operations; consult its command help.
Use gh when an operation is unavailable through gh-axi.
For multiline bodies with gh, write a temporary file and use
--body-file.

When a skill says "publish to the issue tracker", create a
GitHub issue. When it says "fetch the relevant ticket", read
the issue body, labels, and comments.

The software-factory wayfinder session was migrated to GitHub:
[Chart AsmAI](https://github.com/talvor/AssemblyAI/issues/1).
Files in .scratch/software-factory are historical source snapshots;
maintain the live map, tickets, resolutions, and dependencies on GitHub.

## Pull requests as a triage surface

**PRs as a request surface: no.**

## Wayfinding operations

- Map: one issue labelled wayfinder:map, containing Notes,
  Decisions-so-far, and Fog.
- Child tickets: link issues to the map as GitHub sub-issues.
  If unavailable, use a task list in the map and a
  "Part of #<map>" reference in each child.
- Ticket types: use wayfinder:research, wayfinder:prototype,
  wayfinder:grilling, or wayfinder:task.
- Blocking: use native GitHub issue dependencies. If unavailable,
  record "Blocked by: #<number>" references in the child body.
- Frontier: select the first open, unassigned child in map order
  whose blockers are all closed.
- Claim: assign the ticket to the driving developer.
- Resolve: comment with the answer, close the ticket, and add
  a summary and link to the map's Decisions-so-far.
