# 09 CLI and configuration

This document specifies AsmAI's names, every command for the user and for agents, the guard on agent calls, output formats, addressing, `asmai init` and `asmai doctor`, and the configuration file: its location, every field with its name, type, default and meaning, and how changes are applied. The rules behind each command and setting are in the document named beside it.

## Rules

### Names

1. **`asmai` everywhere.** The executable is `asmai`. The same name is used for the configuration and state directories and as the `ASMAI_` prefix of environment variables. `assemblyai` is never used as an identifier, because on npm and PyPI it belongs to AssemblyAI Inc.'s speech-to-text SDK ([AssemblyAI#9](https://github.com/talvor/AssemblyAI/issues/9), [AssemblyAI#13](https://github.com/talvor/AssemblyAI/issues/13)). The product name is spelled AsmAI ([AssemblyAI#13](https://github.com/talvor/AssemblyAI/issues/13)).
2. **No package names are claimed.** Nothing is published to npm or crates.io and there is no Homebrew tap; if AsmAI ever ships on a registry, it takes the name then ([AssemblyAI#20](https://github.com/talvor/AssemblyAI/issues/20)).
3. **The Go module** is `github.com/talvor/asmai` ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27)).

### One executable, three callers

4. **The same executable** is the daemon, the user's CLI and the agents' CLI. Each command is a thin client that talks to the daemon over its local Unix socket ([AssemblyAI#9](https://github.com/talvor/AssemblyAI/issues/9), [ADR 0002](https://github.com/talvor/AssemblyAI/blob/main/docs/adr/0002-agents-coordinate-through-asmai-cli.md)).
5. **Agent callers** are recognized by the per-session credential in their environment; any other caller is the user ([AssemblyAI#8](https://github.com/talvor/AssemblyAI/issues/8), [02](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/02-daemon-and-store.md)).
6. **Version guard.** A command from a version other than the running daemon's does only `stop`, `status` and `doctor`. For anything else it says which version is installed, which is running, and to run `asmai stop` and then `asmai start` ([AssemblyAI#20](https://github.com/talvor/AssemblyAI/issues/20), [10](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/10-release-install-and-upgrade.md)).

### The user's commands

7. **Everyday actions are top-level verbs; setup is grouped by noun** ([AssemblyAI#9](https://github.com/talvor/AssemblyAI/issues/9)). The full set:

| Group | Command | Specified in |
| --- | --- | --- |
| Conversation | `asmai`, `asmai chat` (starts a stopped factory first and says so) | [04](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/04-conversation-and-lavish.md) |
| Running | `asmai start [--foreground]`, `asmai stop [--now]` | [02](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/02-daemon-and-store.md) |
| Running | `asmai status [--check]` | [07](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/07-limits-holds-and-visibility.md) |
| Running | `asmai service install\|uninstall\|status` | [02](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/02-daemon-and-store.md) |
| Looking around | `asmai jobs`, `asmai job <n>`, `asmai agents` | [02](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/02-daemon-and-store.md) |
| Looking around | `asmai decisions` | [01](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/01-roles-and-decisions.md) |
| Looking around | `asmai lavish` | [04](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/04-conversation-and-lavish.md) |
| Looking around | `asmai journal [--job <n>\|--agent <agent>] [--follow]`, `asmai export`, `asmai backup <file>` | [02](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/02-daemon-and-store.md) |
| Looking around | `asmai log [--follow]` | [07](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/07-limits-holds-and-visibility.md) |
| Looking around | `asmai replay <agent> [--dispatch <id>]` | [03](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/03-provider-sessions-and-terminals.md) |
| Intervention | `asmai attach <agent>`, `asmai take <agent> [--interrupt]`, `asmai release <agent>`, and the Ctrl-] menu | [03](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/03-provider-sessions-and-terminals.md) |
| Jobs | `asmai job pause\|resume\|cancel <n>` (`cancel --now` interrupts), `asmai job clean <n>` | [07](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/07-limits-holds-and-visibility.md), [05](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/05-repositories-and-job-branches.md) |
| Setup | `asmai init`, `asmai doctor` | Rules 21 to 24 |
| Setup | `asmai providers install\|list` | [03](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/03-provider-sessions-and-terminals.md) |
| Setup | `asmai config check\|show\|edit\|apply` | Rules 25 to 32 |
| Setup | `asmai repo add <path-or-url>`, `asmai repo list\|show\|remove` | [05](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/05-repositories-and-job-branches.md) |
| Setup | `asmai role list\|set` | Rule 31 |
| Setup | `asmai grants`, `asmai grant revoke <id>` | [01](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/01-roles-and-decisions.md) |
| Release | `asmai notices`, `asmai restore <file>` | [10](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/10-release-install-and-upgrade.md) |

([AssemblyAI#9](https://github.com/talvor/AssemblyAI/issues/9), [AssemblyAI#14](https://github.com/talvor/AssemblyAI/issues/14), [AssemblyAI#20](https://github.com/talvor/AssemblyAI/issues/20))

### Agents' commands and the guard

8. **Agents run only coordination commands.** An agent's credential may run only the commands below. Any other command refuses it; a factory-changing command (starting and stopping, configuration, repositories, the service, take and release, grants) prints the command for the user to run instead. Same-user processes can do anything the user can, so the guard prevents mistakes and keeps authority clear; it is not a security boundary ([AssemblyAI#9](https://github.com/talvor/AssemblyAI/issues/9)).
9. **The daemon checks every call** against the caller's session: its role, whether it is a leader or a worker, its generation, and the assignments it owns ([AssemblyAI#9](https://github.com/talvor/AssemblyAI/issues/9), [AssemblyAI#8](https://github.com/talvor/AssemblyAI/issues/8)).
10. **The agent commands:**

| Who may run it | Command | Specified in |
| --- | --- | --- |
| Every agent | `asmai inbox` (the fetch is delivery evidence), `asmai inbox show`, `asmai brief <job>` | [02](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/02-daemon-and-store.md) |
| Every agent | `asmai status`, `asmai jobs`, `asmai agents` (read-only) | [02](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/02-daemon-and-store.md) |
| Every agent | `asmai turn -- <command>` | [05](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/05-repositories-and-job-branches.md) |
| Coordination's leader | `asmai job open`, `asmai job link` | [01](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/01-roles-and-decisions.md) |
| Coordination's leader | `asmai job pause\|resume\|cancel <n>`, citing the user's witnessed message | [07](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/07-limits-holds-and-visibility.md) |
| Leaders | `asmai handoff send\|accept\|clarify\|decline` | [01](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/01-roles-and-decisions.md) |
| Leaders | `asmai assign [--provider <provider> --model <model>] [--side-effect-free]` | [01](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/01-roles-and-decisions.md) |
| Leaders | `asmai accept`, `asmai reject`, `asmai cancel` | [01](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/01-roles-and-decisions.md), [05](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/05-repositories-and-job-branches.md) |
| Leaders | `asmai reconcile` | [02](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/02-daemon-and-store.md) |
| Leaders | `asmai decision record` (delegated decisions, and the user's answers and grants citing their source) | [01](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/01-roles-and-decisions.md) |
| Leaders and workers | `asmai decision request` (a worker's goes to its owning leader) | [01](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/01-roles-and-decisions.md), [04](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/04-conversation-and-lavish.md) |
| The delivery owner of a job | `asmai push <job>` | [06](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/06-validation-and-delivery.md) |
| Workers, and the delivery owner of a job | `asmai effect <kind> <ref>` | [02](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/02-daemon-and-store.md) |
| Workers | `asmai result`, `asmai blocked` | [01](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/01-roles-and-decisions.md) |

([AssemblyAI#9](https://github.com/talvor/AssemblyAI/issues/9), [AssemblyAI#14](https://github.com/talvor/AssemblyAI/issues/14), [AssemblyAI#18](https://github.com/talvor/AssemblyAI/issues/18); `asmai turn` and `asmai push` were named in review of [05](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/05-repositories-and-job-branches.md) and [06](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/06-validation-and-delivery.md))

### Output

11. **For agents:** compact text by default: key/value lines and short tables, a hint at the next step, and errors that say what to do ([AssemblyAI#9](https://github.com/talvor/AssemblyAI/issues/9)).
12. **For the user:** readable tables ([AssemblyAI#9](https://github.com/talvor/AssemblyAI/issues/9)).
13. **`--json`.** Every command accepts `--json` ([AssemblyAI#9](https://github.com/talvor/AssemblyAI/issues/9)).

### Addressing

14. **Agents are addressed `name@role`**, for example `leader@planning` or `worker1@engineering` ([AssemblyAI#9](https://github.com/talvor/AssemblyAI/issues/9)).
15. **Worker numbers** start at the lowest free number and are reused once a worker ends, so durable records (the journal, Lavish pages and reports) identify a worker by its address together with its assignment ID ([AssemblyAI#9](https://github.com/talvor/AssemblyAI/issues/9)).
16. **A bare role name** is a typing shortcut for its leader (`asmai attach planning` means `leader@planning`), and everything AsmAI prints uses the full form ([AssemblyAI#9](https://github.com/talvor/AssemblyAI/issues/9)).
17. **Jobs are addressed by number** ([AssemblyAI#9](https://github.com/talvor/AssemblyAI/issues/9)).

### Remote hosts

18. **`--host`.** `--host <ssh-destination>`, or `ASMAI_HOST`, runs any command on a remote host through the user's SSH configuration. For the conversation and attach, it also forwards the remote Lavish port ([AssemblyAI#9](https://github.com/talvor/AssemblyAI/issues/9)).
19. **Plain SSH works too.** `ssh -t host asmai` always works ([AssemblyAI#9](https://github.com/talvor/AssemblyAI/issues/9)).
20. **No host registry.** There is no registry of hosts and no combined view across hosts ([AssemblyAI#9](https://github.com/talvor/AssemblyAI/issues/9)).

### `asmai init` and `asmai doctor`

21. **`asmai init`** is an interactive walkthrough, and every question it asks can also be answered by a flag, for a setup without prompts on a remote host ([AssemblyAI#9](https://github.com/talvor/AssemblyAI/issues/9)). Its steps:
    1. Platform certification: an uncertified platform is refused with what to do ([AssemblyAI#7](https://github.com/talvor/AssemblyAI/issues/7)).
    2. The pinned providers, installed after the user confirms ([03](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/03-provider-sessions-and-terminals.md)).
    3. Sign-in: each pinned CLI's own status check reports the sign-in method only; an API-key or unknown method fails, and AsmAI prints the native command for the user to run and never starts a sign-in ([03](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/03-provider-sessions-and-terminals.md)).
    4. Codex's hook trust review ([03](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/03-provider-sessions-and-terminals.md)).
    5. Role staffing, and each provider's default model ([07](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/07-limits-holds-and-visibility.md)).
    6. An offer to run `asmai service install`, and a suggestion to run `asmai repo add`.
22. **`asmai doctor`** re-runs the same checks without changing anything ([AssemblyAI#9](https://github.com/talvor/AssemblyAI/issues/9)). It also shows:
    - the qualification record and its known limitations, and a short read-only self-check of this host ([AssemblyAI#12](https://github.com/talvor/AssemblyAI/issues/12), [11](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/11-qualification-and-proving.md));
    - a newer AsmAI release, with its kind ([AssemblyAI#20](https://github.com/talvor/AssemblyAI/issues/20));
    - a newer upstream skill release, what changed in the skills after an upgrade, what a provider version cannot hide, and added and repository skills marked unqualified ([08](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/08-skills-and-agent-instructions.md));
    - that terminals other than Ghostty are best effort ([03](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/03-provider-sessions-and-terminals.md));
    - renamed and retired settings, with their replacements (rule 30);
    - a store that `asmai start` cannot use: the case, the version that last wrote it, and the newest backups ([10](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/10-release-install-and-upgrade.md)).
23. **`asmai start`** runs the same checks and names any step that fails ([AssemblyAI#9](https://github.com/talvor/AssemblyAI/issues/9), [02](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/02-daemon-and-store.md)).
24. **No `asmai qualify`.** There is no command for qualification ([AssemblyAI#12](https://github.com/talvor/AssemblyAI/issues/12), [11](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/11-qualification-and-proving.md)).

### The configuration file

25. **One TOML file** at `~/.config/asmai/config.toml`, with state in `~/.local/state/asmai`, on Linux and macOS. Commands edit the same file the user can edit by hand ([AssemblyAI#9](https://github.com/talvor/AssemblyAI/issues/9)).
26. **Only the user changes it.** Agents never change the configuration; Coordination gives the user the command or the change to make ([AssemblyAI#9](https://github.com/talvor/AssemblyAI/issues/9), [06](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/06-validation-and-delivery.md)).
27. **`asmai config check`** validates the file, **`show`** prints the effective configuration with every default, and **`edit`** opens the file for editing ([AssemblyAI#9](https://github.com/talvor/AssemblyAI/issues/9), [AssemblyAI#14](https://github.com/talvor/AssemblyAI/issues/14)).
28. **`asmai config apply`** validates the file, shows the change and which running agents it affects, and asks for confirmation ([AssemblyAI#9](https://github.com/talvor/AssemblyAI/issues/9)):
    - a change that affects no running agent applies immediately;
    - a change for a running agent applies at that agent's next start;
    - confirming a provider change for an agent that already has work dispatched is the user's decision to replace its provider, which still goes through reconciliation and keeps the assignment's context ([07](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/07-limits-holds-and-visibility.md));
    - it shows which agents pick up added skills ([08](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/08-skills-and-agent-instructions.md));
    - removing a repository with open jobs is refused ([05](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/05-repositories-and-job-branches.md)).
29. **Journaled.** Each applied configuration is journaled ([AssemblyAI#9](https://github.com/talvor/AssemblyAI/issues/9)).
30. **Across releases.** An upgrade never rewrites the file. Within v1 a new setting has a default, and a renamed or retired setting keeps working, with a warning in `asmai doctor` and `asmai config check` naming its replacement. Only a setting that can no longer be honoured makes `asmai start` refuse, naming the line and the fix ([AssemblyAI#20](https://github.com/talvor/AssemblyAI/issues/20), [10](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/10-release-install-and-upgrade.md)).
31. **`asmai role list|set`** lists each role's staffing and skill lists and sets them, editing the same file ([AssemblyAI#9](https://github.com/talvor/AssemblyAI/issues/9)).
32. **`asmai repo add`** writes the repository's entry into the file, and **`asmai repo remove`** removes it ([AssemblyAI#9](https://github.com/talvor/AssemblyAI/issues/9), [05](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/05-repositories-and-job-branches.md)).

### The schema

33. **Every field**, with its type, default and meaning. Durations are written like `"30s"`, `"10m"` or `"14d"` and sizes like `"5GB"`. The names and layout were confirmed in review of this document ([AssemblyAI#27](https://github.com/talvor/AssemblyAI/issues/27), [answers](https://github.com/talvor/AssemblyAI/blob/main/.lavish/spec-doc-09-answers.json)).

**`[limits]`**: factory-wide operating limits ([AssemblyAI#14](https://github.com/talvor/AssemblyAI/issues/14), [AssemblyAI#18](https://github.com/talvor/AssemblyAI/issues/18)).

| Field | Type | Default | Meaning |
| --- | --- | --- | --- |
| `leader_idle_grace` | duration | `"10m"` | How long a leader with no open work stays before the daemon stops it ([02](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/02-daemon-and-store.md) rule 52) |
| `leader_restarts` | integer | `3` | Restarts of a crashed leader within `leader_restart_window` before its role holds ([02](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/02-daemon-and-store.md) rule 56) |
| `leader_restart_window` | duration | `"15m"` | The window `leader_restarts` counts in |
| `silence_timeout` | duration | `"30m"` | How long a working dispatch may go without a correlated observation before it becomes unknown ([07](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/07-limits-holds-and-visibility.md) rule 31) |
| `drain_timeout` | duration | `"10m"` | How long `asmai stop` waits for running turns before interrupting them ([07](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/07-limits-holds-and-visibility.md) rule 32) |
| `side_effect_free_retries` | integer | `2` | Automatic retries of an assignment declared side-effect-free ([07](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/07-limits-holds-and-visibility.md) rule 25) |
| `provider_error_resumes` | integer | `5` | Resumes after a reported provider error before the provider is marked unavailable ([07](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/07-limits-holds-and-visibility.md) rule 18) |
| `provider_error_wait` | duration | `"30s"` | The first wait before such a resume; each later wait doubles |
| `provider_error_wait_max` | duration | `"8m"` | The longest such wait |
| `recheck_interval` | duration | `"5m"` | How often an unavailable provider or a lost sign-in is rechecked ([07](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/07-limits-holds-and-visibility.md) rules 19, 20) |
| `dispatch_limit` | integer | `5` | Counted dispatches of an assignment without acceptance before it holds ([07](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/07-limits-holds-and-visibility.md) rule 23) |
| `failed_validations` | integer | `3` | Failed validations of a job before its delivery holds ([06](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/06-validation-and-delivery.md) rule 10) |
| `first_check_wait` | duration | `"15m"` | How long to wait for a first CI check before the job holds ([06](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/06-validation-and-delivery.md) rule 32) |
| `free_space_floor` | size | `"5GB"` | Free space on the state directory's volume below which no workspace is created ([07](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/07-limits-holds-and-visibility.md) rule 41) |

**`[logs]`** ([AssemblyAI#14](https://github.com/talvor/AssemblyAI/issues/14)):

| Field | Type | Default | Meaning |
| --- | --- | --- | --- |
| `daemon_files` | integer | `5` | Rotated files of the daemon's log ([07](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/07-limits-holds-and-visibility.md) rule 42) |
| `daemon_file_size` | size | `"20MB"` | Size of each file |
| `recording_retention` | duration | `"14d"` | How long after its job ends a terminal recording is kept ([03](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/03-provider-sessions-and-terminals.md) rule 43) |

**`[providers.claude]`** and **`[providers.codex]`** ([AssemblyAI#14](https://github.com/talvor/AssemblyAI/issues/14), [07](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/07-limits-holds-and-visibility.md)):

| Field | Type | Default | Meaning |
| --- | --- | --- | --- |
| `worker_cap` | integer | `3` | Workers with a dispatch in progress on this provider (rule 5 of 07) |
| `default_model` | string | None | The model used when work falls back to this provider; with none, this provider is not available for fallback (rule 10 of 07) |

**`[roles.<role>]`**, one table for each of `coordination`, `planning`, `research`, `engineering` and `quality` ([AssemblyAI#9](https://github.com/talvor/AssemblyAI/issues/9), [AssemblyAI#15](https://github.com/talvor/AssemblyAI/issues/15), [AssemblyAI#17](https://github.com/talvor/AssemblyAI/issues/17)):

| Field | Type | Default | Meaning |
| --- | --- | --- | --- |
| `leader_provider` | `"claude"` or `"codex"` | None; set by `asmai init` | The provider the role's leader runs on |
| `leader_model` | string | None; set by `asmai init` | The model the role's leader uses |
| `worker_provider` | `"claude"` or `"codex"` | None; set by `asmai init` | The default provider of the role's workers, which an assignment may override |
| `worker_model` | string | None; set by `asmai init` | The default model of the role's workers |
| `leader_skills` | list of skill names | The role's leader list ([08](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/08-skills-and-agent-instructions.md) rule 16) | The shipped skills on the leader's list |
| `worker_skills` | list of skill names | The role's worker list ([08](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/08-skills-and-agent-instructions.md) rule 16) | The shipped skills on the workers' list; optional skills are added here by name |
| `leader_added_skills` | list of directories | `[]` | Added skills for the leader, copied at its start; one with a shipped skill's name replaces it ([08](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/08-skills-and-agent-instructions.md) rules 23, 24) |
| `worker_added_skills` | list of directories | `[]` | Added skills for the workers |

**`[repositories.<name>]`**, one table for each registered repository ([AssemblyAI#9](https://github.com/talvor/AssemblyAI/issues/9), [AssemblyAI#11](https://github.com/talvor/AssemblyAI/issues/11), [AssemblyAI#17](https://github.com/talvor/AssemblyAI/issues/17), [AssemblyAI#18](https://github.com/talvor/AssemblyAI/issues/18)):

| Field | Type | Default | Meaning |
| --- | --- | --- | --- |
| `location` | path | Recorded by `asmai repo add` | Where the user's own checkout is; never used for work ([05](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/05-repositories-and-job-branches.md) rule 5) |
| `origin` | string | Recorded by `asmai repo add` | The origin remote |
| `default_branch` | string | Recorded by `asmai repo add` | The branch jobs start from unless the user names another |
| `notes` | string | `""` | The user's notes, which count as repository instructions ([05](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/05-repositories-and-job-branches.md) rule 34) |
| `checks_one_at_a_time` | boolean | `false` | The repository's checks cannot run side by side; agents run them through `asmai turn` ([05](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/05-repositories-and-job-branches.md) rule 11) |
| `no_ci` | boolean | `false` | The repository has no CI; Quality's checks stand in ([06](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/06-validation-and-delivery.md) rule 30) |
| `commit_trailers` | boolean | `true` | Commits carry the `AsmAI-Job`, `AsmAI-Agent` and `AsmAI-Dispatch` trailers ([05](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/05-repositories-and-job-branches.md) rule 39) |
| `repository_skills` | list of role names | `[]` | The roles for which the repository's own skills are switched on in its jobs ([08](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/08-skills-and-agent-instructions.md) rule 25) |

34. **An example** with the defaults written out, for one role and one repository:

```toml
[limits]
leader_idle_grace = "10m"
leader_restarts = 3
leader_restart_window = "15m"
silence_timeout = "30m"
drain_timeout = "10m"
side_effect_free_retries = 2
provider_error_resumes = 5
provider_error_wait = "30s"
provider_error_wait_max = "8m"
recheck_interval = "5m"
dispatch_limit = 5
failed_validations = 3
first_check_wait = "15m"
free_space_floor = "5GB"

[logs]
daemon_files = 5
daemon_file_size = "20MB"
recording_retention = "14d"

[providers.claude]
worker_cap = 3
default_model = "<a model you choose>"

[providers.codex]
worker_cap = 3
default_model = "<a model you choose>"

[roles.engineering]
leader_provider = "claude"
leader_model = "<a model you choose>"
worker_provider = "codex"
worker_model = "<a model you choose>"
leader_skills = ["pr"]
worker_skills = ["implement", "tdd", "diagnosing-bugs", "prototype", "codebase-design", "improve-codebase-architecture", "pr", "wizard", "writing-for-agents"]
leader_added_skills = []
worker_added_skills = []

[repositories.otman]
location = "/home/me/src/otman"
origin = "git@github.com:me/otman.git"
default_branch = "main"
notes = ""
checks_one_at_a_time = false
no_ci = false
commit_trailers = true
repository_skills = []
```

### Environment

35. **Variables AsmAI reads or sets:** `ASMAI_HOST`, the remote host for any command (rule 18); `ASMAI_SLOT` and `TMPDIR`, set in each worker's session ([05](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/05-repositories-and-job-branches.md)); `ASMAI_INSTALL_DIR`, read by the install script ([10](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/10-release-install-and-upgrade.md)); and the per-session credential, whose name is left to implementation. Agent sessions start without provider API-key variables ([03](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/03-provider-sessions-and-terminals.md)).

## Interfaces

The commands are in rules 7 and 10, the configuration file in rules 25 to 34, and the environment variables in rule 35.

### Files

- **`~/.config/asmai/config.toml`**, the configuration (rule 25).
- **`~/.local/state/asmai`**, the state directory ([02](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/02-daemon-and-store.md)).

### Store records

- **Applied configuration**: each applied configuration, journaled (rule 29).

## Settings and defaults

The schema in rule 33 is the complete list of settings.

## Failure handling

| Failure | Handling |
| --- | --- |
| An agent runs a command it may not | Refused; a factory-changing command prints the command for the user (rule 8) |
| A call from a superseded generation, or for an assignment the caller does not own | Refused ([02](https://github.com/talvor/AssemblyAI/blob/main/docs/spec/02-daemon-and-store.md)) |
| A command from another version than the running daemon | Only `stop`, `status` and `doctor` run (rule 6) |
| An invalid configuration | `config check` and `config apply` say what is wrong; nothing is applied |
| A renamed or retired setting | Works, with a warning naming its replacement (rule 30) |
| A setting that can no longer be honoured | `asmai start` refuses, naming the line and the fix (rule 30) |
| A failing setup step | `asmai start` and `asmai doctor` name it (rules 22, 23) |

## Qualification cases and proving scenarios

- **C1**: platform certification on Linux and on macOS; an uncertified platform refuses to start agents and says what to do (rule 21 step 1).
- **C47**: remote use over SSH: `--host`, Lavish through port forwarding, and plain `ssh -t host asmai` (rules 18, 19).
- **S9**: a job on a remote host driven with `asmai --host`.
- **S1** to **S9** use the commands and settings here throughout.

## Sources

- [Choose factory hosting and lifecycle](https://github.com/talvor/AssemblyAI/issues/7#issuecomment-5976506834) (AssemblyAI#7)
- [Define work state and coordination contracts](https://github.com/talvor/AssemblyAI/issues/8#issuecomment-5976668034) (AssemblyAI#8)
- [Define CLI setup and management experience](https://github.com/talvor/AssemblyAI/issues/9#issuecomment-5979143255) (AssemblyAI#9)
- [Define concurrent repository work and integration](https://github.com/talvor/AssemblyAI/issues/11#issuecomment-5990301132) (AssemblyAI#11)
- [Define v1 acceptance scenarios and evidence](https://github.com/talvor/AssemblyAI/issues/12#issuecomment-5993314453) (AssemblyAI#12)
- [Choose the AsmAI product name](https://github.com/talvor/AssemblyAI/issues/13#issuecomment-5968140448) (AssemblyAI#13)
- [Define operating limits and visibility](https://github.com/talvor/AssemblyAI/issues/14#issuecomment-5991304507) (AssemblyAI#14)
- [Choose runtime adapters and authentication](https://github.com/talvor/AssemblyAI/issues/15#issuecomment-5968867443) (AssemblyAI#15)
- [Choose skill bundles and update policy](https://github.com/talvor/AssemblyAI/issues/17#issuecomment-5992055697) (AssemblyAI#17)
- [Choose validation and delivery ownership](https://github.com/talvor/AssemblyAI/issues/18#issuecomment-5992792804) (AssemblyAI#18)
- [Choose license, release packaging and upgrade migration](https://github.com/talvor/AssemblyAI/issues/20#issuecomment-6004145724) (AssemblyAI#20)
- [Choose the specification's structure and implementation sequence](https://github.com/talvor/AssemblyAI/issues/27#issuecomment-6004852593) (AssemblyAI#27)
- [ADR 0002](https://github.com/talvor/AssemblyAI/blob/main/docs/adr/0002-agents-coordinate-through-asmai-cli.md), [ADR 0003](https://github.com/talvor/AssemblyAI/blob/main/docs/adr/0003-go-executable-runs-pinned-providers.md) and the [glossary](https://github.com/talvor/AssemblyAI/blob/main/GLOSSARY.md): Registered repository, Conversation.
- The review of this document: [questions](https://github.com/talvor/AssemblyAI/blob/main/.lavish/spec-doc-09-round1-questions.json) and [answers](https://github.com/talvor/AssemblyAI/blob/main/.lavish/spec-doc-09-answers.json).
