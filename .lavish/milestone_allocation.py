"""Which milestone delivers each rule of each component document.

Each entry is (document, rules, milestone, part). `rules` is a list of rule numbers or (first, last)
ranges. `part` says which part of the rule the milestone delivers, or "" for the whole rule.
A rule may appear under several milestones, each delivering a stated part.

usage: python3 milestone_allocation.py check            # every rule allocated at least once
       python3 milestone_allocation.py render <M>       # Markdown for one milestone's rules
"""
import os
import re
import sys

SPEC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "docs", "spec")
BASE = "https://github.com/talvor/AssemblyAI/blob/main/docs/spec/"
DOCS = {
    "01": "01-roles-and-decisions.md",
    "02": "02-daemon-and-store.md",
    "03": "03-provider-sessions-and-terminals.md",
    "04": "04-conversation-and-lavish.md",
    "05": "05-repositories-and-job-branches.md",
    "06": "06-validation-and-delivery.md",
    "07": "07-limits-holds-and-visibility.md",
    "08": "08-skills-and-agent-instructions.md",
    "09": "09-cli-and-configuration.md",
    "10": "10-release-install-and-upgrade.md",
    "11": "11-qualification-and-proving.md",
}
P = "Proving"
NAMES = {
    "01": "Roles and decisions",
    "02": "Daemon and store",
    "03": "Provider sessions and terminals",
    "04": "Conversation and Lavish",
    "05": "Repositories and job branches",
    "06": "Validation and delivery",
    "07": "Limits, holds and visibility",
    "08": "Skills and agent instructions",
    "09": "CLI and configuration",
    "10": "Release, install and upgrade",
    "11": "Qualification and proving",
}

A = [
    # 01 Roles and decisions
    ("01", [1], "M1", "Coordination, Engineering and Quality"),
    ("01", [1], "M3", "Planning and Research"),
    ("01", [2, 3, 5, 6], "M1", ""),
    ("01", [4], "M1", "one leader per role"),
    ("01", [4], "M5", "leaders on demand"),
    ("01", [4], "M6", "fencing"),
    ("01", [7], "M1", "outcome and acceptance criteria"),
    ("01", [7], "M2", "named skill, narrowed list, provider override"),
    ("01", [7], "M6", "the side-effect-free declaration"),
    ("01", [8, 9, 10, 12, 13, 16, 20, 27, 45, 49], "M1", ""),
    ("01", [17], "M1", "a tested-PR job"),
    ("01", [17], "M3", "planning-only and research-only jobs"),
    ("01", [21], "M1", ""),
    ("01", [46], "M1", "a job opened from a witnessed message"),
    ("01", [46], "M3", "answers and grants"),
    ("01", [11, 14, 15, 18, 19, (22, 26), 28, (30, 39), (42, 44), 47, 48], "M3", ""),
    ("01", [41], "M3", "needs-you and disputed findings, anything outside the mandate"),
    ("01", [41], "M5", "provider changes"),
    ("01", [29], "M6", ""),
    ("01", [40], "M5", ""),
    # 02 Daemon and store
    ("02", [(1, 5), 10, (13, 17), 21, 22, (23, 26), 38, 42, 43, 45, 50], "M1", ""),
    ("02", [6], "M1", "start runs the checks that exist"),
    ("02", [6], "M2", "setup checks, platform and provider refusals"),
    ("02", [6], "M8", "the store's checks and migration, the qualification record"),
    ("02", [7], "M1", "restoring the leaders"),
    ("02", [7], "M6", "terminating orphans and reconciling"),
    ("02", [9], "M1", "stopping and persisting"),
    ("02", [9], "M6", "draining up to the timeout, and --now"),
    ("02", [11], "M1", "continuing after a clean stop"),
    ("02", [11], "M6", "recovering an unclean stop"),
    ("02", [12], "M5", ""),
    ("02", [18], "M1", "asmai export"),
    ("02", [18], "M8", "asmai backup"),
    ("02", [19], "M1", "repository jobs"),
    ("02", [19], "M3", "jobs without a repository"),
    ("02", [20, 31], "M3", ""),
    ("02", [27, 28], "M6", ""),
    ("02", [29], "M1", "the transcript location"),
    ("02", [29], "M2", "the bundle version and skill fingerprints"),
    ("02", [29], "M4", "the recording"),
    ("02", [29], "M5", "token counts"),
    ("02", [30], "M1", "active, submitted, accepted, rejected and cancelled"),
    ("02", [30], "M5", "queued and held"),
    ("02", [30], "M6", "needs reconciliation"),
    ("02", [32], "M6", ""),
    ("02", [(33, 36)], "M1", ""),
    ("02", [37], "M1", "waiting for a boundary"),
    ("02", [37], "M4", "while the user holds input or at an unknown input state"),
    ("02", [(39, 41)], "M6", ""),
    ("02", [44], "M1", "the ledger"),
    ("02", [44], "M6", "checking it in reconciliation"),
    ("02", [(46, 49)], "M6", ""),
    ("02", [51], "M1", "starting a leader when a message for its role arrives"),
    ("02", [52, 53], "M5", ""),
    ("02", [8, (54, 63)], "M6", ""),
    ("02", [64], "M8", ""),
    # 03 Provider sessions and terminals
    ("03", [1, 9, 12, 15], "M1", "Claude Code"),
    ("03", [1, 9, 12, 15], "M2", "Codex"),
    ("03", [1], "M3", "Lavish"),
    ("03", [2], "M1", "Claude Code"),
    ("03", [2], "M2", "Codex"),
    ("03", [2], "M3", "Lavish"),
    ("03", [3, 5, 7], "M2", ""),
    ("03", [4], "M2", "refusing versions that are not pinned"),
    ("03", [4], "M8", "the qualification record"),
    ("03", [6, 8, 10, 11, 16, 18, 19, (21, 23), 26, 27, 44], "M1", ""),
    ("03", [13], "M8", ""),
    ("03", [14], "M1", "repository configuration and write guards"),
    ("03", [14], "M2", "skills"),
    ("03", [17], "M1", "rendering for attach"),
    ("03", [17], "M4", "qualified fidelity at reduced height"),
    ("03", [20], "M1", "the safe default"),
    ("03", [20], "M4", "an interrupted Claude turn"),
    ("03", [28], "M1", "drawing the screen"),
    ("03", [28], "M4", "one row less"),
    ("03", [24, 25, 29, 30, 31, (32, 43)], "M4", ""),
    ("03", [45], "M1", ""),
    # 04 Conversation and Lavish
    ("04", [1, 2, 3], "M1", ""),
    ("04", [4, 5, 6, 7, 8, (12, 17), 19], "M4", ""),
    ("04", [9], "M3", "presenting a decision once"),
    ("04", [9], "M4", "the status line keeping it visible"),
    ("04", [10, 20, 22, (23, 29)], "M3", ""),
    ("04", [11, 18], "M5", ""),
    ("04", [21], "M3", "localhost, the URL and the forwarding command"),
    ("04", [21], "M7", "--host forwarding"),
    # 05 Repositories and job branches
    ("05", [1, 2, 3, 5, 6, 9, 10, 13, 14, 15, 17, 18, 21, (26, 28), 33, 35, 36, 37, 40, 43], "M1", ""),
    ("05", [7], "M1", "a writing assignment, and Quality's read-only one"),
    ("05", [34], "M1", "instruction files"),
    ("05", [34], "M2", "the user's notes in the configuration"),
    ("05", [38, 39], "M1", ""),
    ("05", [39], "M2", "the per-repository switch"),
    ("05", [25], "M1", "refusing a push over outside commits"),
    ("05", [25], "M5", "merging outside commits in"),
    ("05", [4, 8, 16, 19, (29, 32)], "M3", ""),
    ("05", [44], "M3", "keeping scratch workspaces"),
    ("05", [44], "M5", "asmai job clean"),
    ("05", [11, 12, 20, 22, 23, 24, 42], "M5", ""),
    ("05", [41], "M6", ""),
    # 06 Validation and delivery
    ("06", [1, 2, 3, 11, 13, 14, 15, 17, 19, 20, 21, 22, 24, 25, (26, 29), 33, 34, 35], "M1", ""),
    ("06", [5], "M1", "validation of the finished job branch"),
    ("06", [5], "M3", "an earlier review on request"),
    ("06", [8], "M1", "the three kinds, and blocking findings"),
    ("06", [8], "M3", "needs-you findings"),
    ("06", [18], "M1", "the refusal"),
    ("06", [18], "M5", "a worker merging outside commits in"),
    ("06", [23], "M1", "the PR section"),
    ("06", [23], "M2", "the pr skill's form"),
    ("06", [4], "M2", ""),
    ("06", [6, 7, 9, 12, 16, (37, 39)], "M3", ""),
    ("06", [10, (30, 32), 36], "M5", ""),
    ("06", [40, 41], "M6", ""),
    # 07 Limits, holds and visibility
    ("07", [1], "M3", ""),
    ("07", [9], "M2", ""),
    ("07", [(2, 8), (10, 30), 35, 36, (38, 41)], "M5", ""),
    ("07", [31, 32, 37], "M6", ""),
    ("07", [33], "M4", ""),
    ("07", [34], "M1", "the daemon, its version and the leaders"),
    ("07", [34], "M5", "caps, the queue, providers, holds and disk"),
    ("07", [42, 43], "M1", ""),
    # 08 Skills and agent instructions
    ("08", [(1, 3), 4, (6, 8), 10, (11, 13), 16, 17, (19, 26), 39], "M2", ""),
    ("08", [5], "M8", ""),
    ("08", [9, 14, 15, 18, (27, 36)], "M3", ""),
    ("08", [37], "M1", "Coordination's, Engineering's and Quality's instructions for the skeleton"),
    ("08", [37], "M2", "the operating guide"),
    ("08", [37], "M3", "Planning's and Research's instructions, and decisions"),
    ("08", [38], "M1", ""),
    # 09 CLI and configuration
    ("09", [1, 4, 5, (8, 17)], "M1", ""),
    ("09", [2, 3], "M0", ""),
    ("09", [7], "M1", "each command arrives with the milestone of the rule it serves"),
    ("09", [6, 24, 30], "M8", ""),
    ("09", [(18, 20)], "M7", ""),
    ("09", [(21, 23), 26, 27, 28, 29, 31], "M2", ""),
    ("09", [25, 32, 33, 34], "M1", "the file and the fields M1 uses"),
    ("09", [25, 32, 33, 34], "M2", "every field"),
    ("09", [35], "M1", "ASMAI_SLOT and TMPDIR"),
    ("09", [35], "M7", "ASMAI_HOST"),
    ("09", [35], "M8", "ASMAI_INSTALL_DIR"),
    # 10 Release, install and upgrade
    ("10", [(1, 6)], "M0", ""),
    ("10", [8], "M0", "the repository"),
    ("10", [8], "M8", "releases"),
    ("10", [7], "M2", ""),
    ("10", [(9, 42)], "M8", ""),
    # 11 Qualification and proving
    ("11", [4, 5, 10, 11], "M0", ""),
    ("11", [6], "M0", "the separate OS users"),
    ("11", [6], "M1", "the harness"),
    ("11", [7, (12, 16), 18], "M1", ""),
    ("11", [8], "M1", "each milestone adds the faults its cases need"),
    ("11", [9], "M5", ""),
    ("11", [17], "M4", "Ghostty locally"),
    ("11", [17], "M7", "Ghostty over SSH"),
    ("11", [(19, 23)], "M8", ""),
    ("11", [24], "M1", "each milestone passes its own cases"),
    ("11", [24], "M8", "all 47 together"),
    ("11", [31], "M7", ""),
    ("11", [(1, 3), (25, 30), (32, 38)], P, ""),
]


def expand(rules):
    for r in rules:
        if isinstance(r, tuple):
            yield from range(r[0], r[1] + 1)
        else:
            yield r


def titles(doc):
    out = {}
    for line in open(os.path.join(SPEC, DOCS[doc])):
        m = re.match(r"(\d+)\. \*\*(.+?)\*\*", line)
        if m:
            out[int(m.group(1))] = m.group(2).rstrip(".:,")
            continue
        m = re.match(r"(\d+)\. (.+?)[.;]", line)
        if m and not line.startswith(" "):
            out[int(m.group(1))] = " ".join(m.group(2).split()[:6])
    return out


def check():
    bad = 0
    for doc in DOCS:
        t = titles(doc)
        got = {r for d, rs, _, _ in A if d == doc for r in expand(rs)}
        missing = sorted(set(t) - got)
        extra = sorted(got - set(t))
        if missing or extra:
            bad = 1
            print(doc, "missing", missing, "unknown", extra)
    print("ok" if not bad else "incomplete")
    return bad


def render(ms):
    lines = []
    for doc, fname in DOCS.items():
        t = titles(doc)
        rows = sorted((r, part) for d, rs, m, part in A if d == doc and m == ms for r in expand(rs))
        if not rows:
            continue
        name = NAMES[doc]
        lines.append(f"**[{doc} {name}]({BASE}{fname})**\n")
        lines.append("| Rule | | Part delivered here |")
        lines.append("| --- | --- | --- |")
        for r, part in rows:
            lines.append(f"| {r} | {t[r]} | {part or 'All'} |")
        lines.append("")
    return "\n".join(lines)


if __name__ == "__main__":
    if sys.argv[1] == "check":
        sys.exit(check())
    print(render(sys.argv[2]))
