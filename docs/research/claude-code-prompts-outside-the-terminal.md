# Claude Code prompts outside the terminal

Snapshot: 2026-10-20. Evidence for the decision ticket on which native prompts may rise to the user through Coordination, not a decision. The pinned Claude Code is 2.1.292. The current release is 2.1.304 (published 2026-10-19).

## Method

Read only. Claude Code documentation (the `.md` form of each page on code.claude.com, fetched 2026-10-20), the Claude Code `CHANGELOG.md` on `anthropics/claude-code@main`, OpenAI's Codex documentation, and AsmAI's source and ADRs on `talvor/asmai@main` (3f891079aa). The prior managed-policy research ([note](https://github.com/talvor/asmai/blob/research/managed-only-policy-intent/docs/research/managed-only-policy-intent.md) at 749b0bcbbf, issues #127 to #131) is cited, not repeated. No `claude`, `asmai` or Codex binary was run, and nothing was probed on any managed machine.

Each claim carries one of these tags.

- **Documented.** A page says it. The link follows.
- **Inferred.** Follows from documented facts. The reasoning is given.
- **AsmAI source.** What AsmAI's own code or ADRs say or require.

The Claude Code docs describe the current release only. They carry no per-version snapshots. A fact is taken to hold on 2.1.292 unless a version gate or a changelog entry says otherwise (item 6). That assumption is itself listed under "Not established".

## Headlines

- The one documented outside-process route that reaches AsmAI's interactive agents is a hook. A `PermissionRequest` hook holds the call while it runs, and returns allow or deny. A `PreToolUse` hook does the same earlier, on every call.
- `PermissionRequest` does not fire in `dontAsk` mode. `PreToolUse` fires in every mode, and its `allow` does run a call that `dontAsk` would deny, apart from a short list of calls nothing approves.
- If no answer comes, the native prompt appears and waits with no timeout of its own. On the pin, Claude Code does not turn a hook failure or its own timeout into a denial. Only the hook's code can, by printing a deny before it fails or runs out of time.
- `canUseTool` and `--permission-prompt-tool` serve print-mode (`-p`) and SDK runs, not interactive terminal sessions like AsmAI's agents.
- An answer can be allow once, allow for the session, add a rule, or deny with a message. Only the `session` destination is documented as file-free. No documented destination writes managed settings.

## Findings

### 1. Holding a prompt open from an outside process

**What AsmAI has today.** **AsmAI source.** Every agent session registers one `command` hook, `asmai hook`, for `SessionStart`, `UserPromptSubmit`, `PermissionRequest` and `Stop`, with no matcher and no `timeout` ([claude.go](https://github.com/talvor/asmai/blob/main/internal/providers/claude.go)). The command reads the payload, calls the daemon over its socket, prints nothing and does not exit 2 ([main.go, `hook`](https://github.com/talvor/asmai/blob/main/cmd/asmai/main.go)). So it never returns a decision. The daemon marks a prompt as waiting on `PermissionRequest` and clears it on the next event ([prompts.go](https://github.com/talvor/asmai/blob/main/internal/daemon/prompts.go)).

**`PermissionRequest` can hold and answer.**

- **Documented.** The page opens: "Runs when Claude Code is about to ask you for permission to use a tool." It does not run for a sandboxed command's network request ([hooks, PermissionRequest](https://code.claude.com/docs/en/hooks#permissionrequest)).
- **Documented.** "By default, hooks block Claude's execution until they complete." Only `async: true` command hooks run in the background, and those "can't block or control Claude's behavior" ([hooks, background hooks](https://code.claude.com/docs/en/hooks#run-hooks-in-the-background)).
- **Documented.** A hook is a shell command, an HTTP POST, an MCP tool call, a prompt or an agent. Command and HTTP hooks get the event JSON on stdin or in the body, and the environment of Claude Code ([hooks, handler fields](https://code.claude.com/docs/en/hooks#hook-handler-fields)).
- **Inferred.** A command that waits on a daemon round trip (a user answer relayed through Coordination) holds the call for as long as it runs, up to the `timeout`. `asmai hook` already makes the daemon call. Only the wait and the printed answer are missing.

**What the hook may return.**

- **Documented, `PermissionRequest`.** `hookSpecificOutput.decision` with `behavior` `"allow"` or `"deny"`. For allow: `updatedInput` and `updatedPermissions`. For deny: `message` (tells Claude why) and `interrupt` (stops Claude). Deny and ask rules are still evaluated, so an allow does not override a matching deny rule ([PermissionRequest decision control](https://code.claude.com/docs/en/hooks#permissionrequest-decision-control)). The input also carries `session_id`, `cwd`, `permission_mode`, `tool_name`, `tool_input` and `permission_suggestions`, but no `tool_use_id`.
- **Documented, `PreToolUse`.** `permissionDecision` of `allow`, `deny`, `ask` or `defer`, plus `permissionDecisionReason`, `updatedInput`, `additionalContext`. It runs before every tool call whether or not it needs permission. Deny and ask rules are still evaluated after it. Exit 2 acts as deny with stderr as the reason ([PreToolUse decision control](https://code.claude.com/docs/en/hooks#pretooluse-decision-control)). `defer` works only with `-p` and is ignored in an interactive session ([defer](https://code.claude.com/docs/en/hooks#defer-a-tool-call-for-later)).
- **Documented.** Exit code 2 "isn't honored" on `PermissionRequest`: the flow proceeds unchanged. The answer has to be the `decision` object ([exit code 2 per event](https://code.claude.com/docs/en/hooks#exit-code-2-behavior-per-event)).

**Timeouts and no answer.**

- **Documented.** Default `timeout` is 600 seconds for `command`, `http` and `mcp_tool` hooks, set per hook in seconds ([common fields](https://code.claude.com/docs/en/hooks#common-fields)). The pages state no maximum.
- **Documented.** A hook that reaches its timeout is cancelled and its output is discarded, "so on most events a timed-out hook renders no decision." On `PreToolUse` a timed-out hook "doesn't block the tool call." The call "continues through the normal permission flow" ([timeouts](https://code.claude.com/docs/en/hooks#timeouts)).
- **Documented.** A hook that fails to start, exits with a code other than 0 or 2, or prints invalid JSON is a "non-blocking error" and the action goes ahead ([exit code output](https://code.claude.com/docs/en/hooks#exit-code-output)). **Inferred.** On `PermissionRequest` "the action goes ahead" means the normal permission flow continues, as the page says for exit 2 without a decision.
- **Inferred.** In a terminal session a no-decision outcome (timeout, daemon down, `asmai hook` exits non-zero) leaves the native prompt to be drawn and answered in the PTY. The pages say this for sessions that cannot prompt (denied) and say "the session still waits on the same request" for a background session whose hook fails ([agent view](https://code.claude.com/docs/en/agent-view)). They do not say it in those words for a terminal session.
- **Documented.** Claude Code "keeps permission prompts and `AskUserQuestion` questions open until you answer them." The page gives a deadline only to other forwarded dialogs ([Remote Control, limits](https://code.claude.com/docs/en/remote-control)). So an unanswered native prompt waits without end.
- **Documented.** `onFailure: "block"` on a `command` or `http` hook makes a failure or timeout block the action, and on `PermissionRequest` it "denies the request." It requires Claude Code 2.1.295 or later ([block the action when a hook fails](https://code.claude.com/docs/en/hooks#block-the-action-when-a-hook-fails)). The pin does not have it (item 6).
- **Inferred.** A hook that keeps its own deadline below `timeout` can print a `deny` with a `message` when nobody has answered, so the agent is told and the native prompt never shows. This uses only the documented `decision` object.

**Prompts a hook cannot answer.**

- **Documented.** No `PermissionRequest` hook runs for a sandboxed command's network-host prompt. The only signal is a `Notification` hook with the `permission_prompt` matcher, which "can't block or modify" the notification and fires after the prompt has waited about six seconds ([PermissionRequest](https://code.claude.com/docs/en/hooks#permissionrequest), [Notification](https://code.claude.com/docs/en/hooks#notification)). That signal needs 2.1.246 or later, which the pin has.
- **AsmAI source.** The folder trust dialog comes "before any hook runs", so AsmAI has the user answer it at setup ([ADR 0011](https://github.com/talvor/asmai/blob/main/docs/adr/0011-agents-rely-on-one-user-given-directory-trust.md)). **Documented.** Channel relay does not carry trust or MCP-consent dialogs either: those "only appear in the local terminal" ([channels reference](https://code.claude.com/docs/en/channels-reference#relay-permission-prompts)).

**Headless, stream-json and SDK, in one paragraph.** **Documented.** In a `-p` run a call that needs approval goes to the Agent SDK host's `canUseTool` callback or to the MCP tool named by `--permission-prompt-tool`, which the CLI reference describes as handling "permission prompts in non-interactive mode". The callback "can stay pending indefinitely", so it can wait for a person, and it returns `{behavior: "allow", updatedInput?, updatedPermissions?}` or `{behavior: "deny", message, interrupt?}` ([user input](https://code.claude.com/docs/en/agent-sdk/user-input), [TypeScript `PermissionResult`](https://code.claude.com/docs/en/agent-sdk/typescript#permissionresult), [CLI flags](https://code.claude.com/docs/en/cli-reference#cli-flags)). Hooks "run alongside your host, and whichever decides first applies". `--permission-prompts none` denies everything that would prompt unless a `PermissionRequest` hook allows it, and a bare `-p` run with no host denies the same way ([headless](https://code.claude.com/docs/en/headless#turn-off-permission-prompts-in-unattended-runs)). None of this attaches to an interactive terminal session, which is what AsmAI's agents are. **Inferred.** Using it would mean running agents as `-p` stream-json sessions in place of the terminals the daemon owns ([ADR 0001](https://github.com/talvor/asmai/blob/main/docs/adr/0001-daemon-owns-agent-terminals.md)). The `control_request` wire format for `can_use_tool` is not documented on the pages read. AsmAI's probe already sends one undocumented-on-these-pages control request, `list_permission_rules` ([ADR 0013](https://github.com/talvor/asmai/blob/main/docs/adr/0013-asmai-refuses-to-start-where-claude-code-ignores-its-permission-rules.md)).

**Other documented routes into an interactive session.**

- **Channels permission relay.** **Documented.** A two-way channel (an MCP server started with `--channels`, declaring `claude/channel/permission`) receives the same prompt "in parallel". The local dialog stays open, and Claude Code applies "whichever answer arrives first." The verdict is `allow` or `deny` with a request ID, and "neither verdict affects future calls." It covers tool-use approvals, not trust or MCP-consent dialogs. It needs claude.ai or Console authentication and is a research preview. A server off Anthropic's allowlist needs `--dangerously-load-development-channels`, which "prompts for confirmation", and `channelsEnabled` gates it on Team and Enterprise ([channels reference](https://code.claude.com/docs/en/channels-reference#relay-permission-prompts), [channels](https://code.claude.com/docs/en/channels#enterprise-controls), [CLI flags](https://code.claude.com/docs/en/cli-reference#cli-flags)). Relay was added in 2.1.81, so the pin has it.
- **Mods.** **Documented.** A mod is a plugin whose JavaScript handlers run inside Claude Code. A `tool.check` handler runs after rules and settings hooks, can answer allow, ask or deny, and a `tool.call` handler can `await` before `next(e)` ([mods events](https://code.claude.com/docs/en/plugins/mods/events#approve-or-refuse-a-tool-call-before-the-user-is-asked)). A mod "runs with your permissions" and can make network requests ([mods overview](https://code.claude.com/docs/en/plugins/mods/overview)). AsmAI already delivers a plugin with `--plugin-dir`. **Inferred.** A mod could reach the daemon. Whether that works on the pin is not established.
- **Remote Control.** **Documented.** The user can answer from claude.ai or the Claude app. It needs a subscription login and is an Anthropic-hosted path, not one through Coordination ([Remote Control](https://code.claude.com/docs/en/remote-control)).

### 2. What an answer can mean

| Answer | How a hook or host says it | Writes a settings file? |
| :- | :- | :- |
| Allow once | `PermissionRequest` allow with no `updatedPermissions`; `PreToolUse` allow; `canUseTool` allow; a channel `allow` | No |
| Allow, with the input changed | `updatedInput` (replaces the whole input and is re-checked against deny and ask rules) | No |
| Allow for the session | `updatedPermissions` entry with `destination: "session"`: `addRules`, `setMode` (for example `acceptEdits`), `addDirectories` | No. "in-memory only, discarded when the session ends" |
| Always allow, add a rule | `addRules` with `destination` `localSettings`, `projectSettings` or `userSettings` | Yes: `.claude/settings.local.json`, `.claude/settings.json`, `~/.claude/settings.json` |
| Deny with a message the agent sees | `PermissionRequest` deny + `message` (Claude is told why); `PreToolUse` deny + `permissionDecisionReason` or exit 2 stderr; `canUseTool` deny + `message` | No |
| Deny and stop the agent | `PermissionRequest` deny + `interrupt: true`; `canUseTool` deny + `interrupt` | No |

- **Documented.** The entry types are `addRules`, `replaceRules`, `removeRules`, `setMode`, `addDirectories` and `removeDirectories`. The destination table lists exactly `session`, `localSettings`, `projectSettings` and `userSettings` ([permission update entries](https://code.claude.com/docs/en/hooks#permission-update-entries)). The SDK type adds `cliArg` ([TypeScript `PermissionUpdate`](https://code.claude.com/docs/en/agent-sdk/typescript#permissionupdate)). No destination names managed settings.
- **Documented.** `setMode: bypassPermissions` is a no-op when `permissions.disableBypassPermissionsMode` disables it, and AsmAI sets that ([PermissionRequest, notes](https://code.claude.com/docs/en/hooks#permission-update-entries)). **AsmAI source.** `disableBypassPermissionsMode: "disable"` is in every session's settings.
- **Documented.** The dialog's own "Yes, and don't ask again" saves a Bash or WebFetch rule to `.claude/settings.local.json` at the root of the git repository, "resolved through worktrees to the main checkout." A file-edit approval lasts until the session ends ([permissions](https://code.claude.com/docs/en/permissions#permission-system)). The sandbox network prompt's "don't ask again" saves a rule to local settings, or to user settings while the sandbox is admin-required ([sandboxing, network isolation](https://code.claude.com/docs/en/sandboxing#network-isolation)). These are dialog answers a person gives in a terminal. A hook answer writes a file only if the hook asks for a file destination.
- **Inferred.** Because AsmAI's hook command builds the answer, AsmAI controls the destination. An answer that never names `localSettings`, `projectSettings` or `userSettings` writes no user, project or managed file.
- **Inferred.** AsmAI starts every session with an empty `--setting-sources` ([claude.go](https://github.com/talvor/asmai/blob/main/internal/providers/claude.go)), so user, project and local files are not read. A rule saved to one of them would not be read back by an AsmAI session. A durable "always allow" that AsmAI owns would have to be AsmAI's own record applied through its next `--settings`. Whether a file-destination rule applies inside the current session when its source is not loaded is not documented.

### 3. How each mode treats a request no rule allows

The request here is a call that needs approval and matches no allow rule.

| Mode | Treatment | Source |
| :- | :- | :- |
| `default` (labelled Manual) | The native prompt. Only reads run without one. `PermissionRequest` fires. | [available modes](https://code.claude.com/docs/en/permission-modes#available-modes) |
| `acceptEdits` | Edits and `mkdir`, `touch`, `rm`, `rmdir`, `mv`, `cp`, `sed` inside the working directory or `additionalDirectories` are approved. Everything else, including every other shell command and network request, prompts. | [acceptEdits](https://code.claude.com/docs/en/permission-modes#auto-approve-file-edits-with-acceptedits-mode) |
| `plan` | No edits. File edits and shell writes are not auto-approved and prompt (through `canUseTool` in the SDK). A `PreToolUse` allow has no effect on an edit (a fix from 2.1.299, see item 6). With auto mode available, classifier-approved commands also run. | [plan mode](https://code.claude.com/docs/en/permission-modes#analyze-before-you-edit-with-plan-mode), [hook approvals in plan mode](https://code.claude.com/docs/en/permissions#hook-approvals-in-plan-mode) |
| `dontAsk` | Denied, with no prompt. Reads in the working directories, read-only commands, calls matching allow rules, and "calls approved by a PreToolUse hook" still run. `canUseTool` is never called. An installed mod can still approve some denied calls. | [dontAsk](https://code.claude.com/docs/en/permission-modes#allow-only-pre-approved-tools-with-dontask-mode), [SDK permission order](https://code.claude.com/docs/en/agent-sdk/permissions#how-permissions-are-evaluated) |
| `bypassPermissions` | Approved, except the actions no mode auto-approves. Those prompt (and are denied in `-p`). AsmAI disables the mode. | [bypassPermissions](https://code.claude.com/docs/en/permission-modes#skip-all-checks-with-bypasspermissions-mode) |
| `auto` | A classifier decides. Reads and working-directory edits skip it. A block tells Claude the reason. After 3 blocks in a row or 20 in total, auto mode pauses and prompting resumes. Needs a supported model and plan, and an admin can disable it. ADR 0012 rejects it. | [how auto mode evaluates actions](https://code.claude.com/docs/en/permission-modes#how-auto-mode-evaluates-actions), [when it falls back](https://code.claude.com/docs/en/permission-modes#when-auto-mode-falls-back) |

- **Documented.** "Actions no mode auto-approves" are: calls matched by an explicit ask rule, org-`ask` connector tools, `AskUserQuestion` and MCP tools marked `requiresUserInteraction`, `rm` and `rmdir` on a critical path, cross-session messaging safeguards, and some reads outside the working directories. In `dontAsk` the first three groups are denied and so are critical-path removals and network-path reads, even if an allow rule or hook matches ([actions no mode auto-approves](https://code.claude.com/docs/en/permission-modes#actions-no-mode-auto-approves)).
- **Documented.** With 2.1.283 or later, auto mode is the built-in starting mode for interactive terminal sessions when nothing sets one ([permission modes](https://code.claude.com/docs/en/permission-modes)). **AsmAI source.** Every session sets `permissions.defaultMode` (`default` or `dontAsk`), so this does not apply.

**What the sandbox's auto-allow changes.**

- **Documented.** With the sandbox on and `autoAllowBashIfSandboxed` true, a Bash command that runs inside the sandbox is approved with no prompt, in every mode ("works independently of your permission mode setting") except plan mode, an auto-mode command with per-command domains, and server-side classifier review ([auto-allow mode](https://code.claude.com/docs/en/sandboxing#auto-allow-mode)). So for sandboxed Bash a request no rule allows is often not a prompt at all.
- **Documented.** Still routed through the regular permission flow: deny rules, content-scoped ask rules, critical-path `rm`, Monitor commands, commands that carry a variable assignment in front such as `FOO=bar npm test`, `make CC=clang`, `eval "ls"`, `excludedCommands`, and an unsandboxed retry ([auto-allow mode](https://code.claude.com/docs/en/sandboxing#auto-allow-mode)). **AsmAI source.** ADR 0012 adds a command with a brace next to a quote character, which prompts "whatever the sandbox's auto-allow and AsmAI's allow rules say".
- **Documented.** The unsandboxed retry is approved by a matching allow rule, prompts in `default` and `acceptEdits`, and is denied in `dontAsk` ([unsandboxed retry](https://code.claude.com/docs/en/sandboxing#the-unsandboxed-retry-escape-hatch)). A sandboxed command that connects to a host outside the allowed domains stays in the sandbox and waits: it prompts in `default` and `acceptEdits`, and is refused in `dontAsk` ([hosts outside your allowed domains](https://code.claude.com/docs/en/sandboxing#hosts-outside-your-allowed-domains)).

**Does a hook fire in `dontAsk` for a request that will be denied?**

- **`PermissionRequest`: no.** **Documented, by implication.** Hooks "fire when Claude Code is about to ask you for permission, or when it would otherwise auto-deny a call that can't prompt. In non-interactive mode with the `-p` flag, they still run outside `dontAsk` mode" ([hooks guide, limitations](https://code.claude.com/docs/en/hooks-guide#limitations)). **AsmAI source.** Qualification case C49 requires that a heredoc denied in `dontAsk` mode produces no `PermissionRequest` in the session's hook log, on a non-interactive run of the pinned Claude Code ([qualification-harness.md](https://github.com/talvor/asmai/blob/main/docs/qualification-harness.md), [prompts.go](https://github.com/talvor/asmai/blob/main/qualification/prompts.go)). The pages say this for `-p`. For an interactive `dontAsk` session it is **inferred**, not stated.
- **`PreToolUse`: yes.** **Documented.** "PreToolUse hooks fire before any permission-mode check, in every permission mode, including `dontAsk`" ([hooks guide, hooks and permission modes](https://code.claude.com/docs/en/hooks-guide#hooks-and-permission-modes)).
- **`PermissionDenied`: not for `dontAsk`.** **Documented.** The event table says it fires when auto mode denies a tool call, and names no other mode ([hooks](https://code.claude.com/docs/en/hooks#hook-lifecycle)).

**Can a hook's allow override a `dontAsk` denial?**

- **`PreToolUse` allow: yes, with limits.** **Documented.** The `dontAsk` page lists "calls approved by a PreToolUse hook" among what runs, and the SDK order puts hooks first. A hook `allow` does not skip deny rules or ask rules (an ask rule is denied in `dontAsk`). It cannot approve a critical-path removal, a network-path read, an MCP tool marked `requiresUserInteraction` or an org-`ask` connector tool. `AskUserQuestion` needs the allow paired with `updatedInput`, and `dontAsk` denies it even when an allow rule matches ([PreToolUse decision control](https://code.claude.com/docs/en/hooks#pretooluse-decision-control), [hooks guide, hooks and permission modes](https://code.claude.com/docs/en/hooks-guide#hooks-and-permission-modes), [dontAsk](https://code.claude.com/docs/en/permission-modes#allow-only-pre-approved-tools-with-dontask-mode)).
- **`PermissionRequest` allow: moot,** because the event does not fire in `dontAsk`.
- **Inferred.** The `PreToolUse` input has no field that says whether the rules would allow or deny the call. It carries `permission_mode`, `tool_name`, `tool_input` and `tool_use_id`. A hook that wants to act only on would-be-denied calls has to restate AsmAI's rules itself. It also runs on every tool call.
- **Not stated.** Whether a `PreToolUse` allow approves an unsandboxed retry or a write to a protected path in `dontAsk`.

### 4. `allowManagedPermissionRulesOnly`

The full scope, adjacent keys and the worst-case account are in the [prior research](https://github.com/talvor/asmai/blob/research/managed-only-policy-intent/docs/research/managed-only-policy-intent.md) (#129). What follows is only what bears on prompts rising to the user.

- **Hooks are untouched by the key.** The prior note finds that the key locks `allow`, `ask` and `deny` rules, and that hooks (including `PreToolUse` and `PermissionRequest` `allow`), permission modes, sandbox auto-allow and the SDK host are outside its scope. The settings reference agrees: its entry names rules, `--allowedTools`, the always-allow choices and saving, nothing about hooks ([settings reference](https://code.claude.com/docs/en/settings-reference#allowmanagedpermissionrulesonly)). So a hook answer still works, and the key does not stop a daemon from answering.
- **Prompts lose their rule options.** **Documented.** The key "hides the always-allow choices in permission prompts, and stops saving new rules" ([settings reference](https://code.claude.com/docs/en/settings-reference#allowmanagedpermissionrulesonly)). The `permission_suggestions` array a hook receives can still hold `addRules` entries the dialog withholds ([PermissionRequest input](https://code.claude.com/docs/en/hooks#permissionrequest-input)). What the key does to a hook's `updatedPermissions` `addRules` is not documented.
- **Allow once and deny with a message are unaffected,** as is a session `setMode` (the prior note cites anthropics/claude-code#84231 for session-scoped mode changes surviving the key).
- **`dontAsk` is untouched.** On a managed-only account AsmAI's own `--settings` allow rules are ignored, so a worker's `asmai` call is denied in `dontAsk` unless the admin lists it (ADR 0013). A `PreToolUse` `allow` would approve it. That is the "AsmAI approves calls itself" class (#131, item 3). This note does not weigh it.
- **Locks that would switch off the hook route.** The prior note finds that `allowManagedHooksOnly` and `disableAllHooks` in managed settings keep only hooks "the Agent SDK registers in process" and managed hooks. The maintainer's real policy sets neither (the prior note, read from the cached server-managed policy). The docs do not say whether hooks given with `--settings` count among the user, project and local hooks that `allowManagedHooksOnly` blocks ([settings reference](https://code.claude.com/docs/en/settings-reference#allowmanagedhooksonly)). If they do, the existing hook journal and any answering hook go dark together.
- **The channel route and MCP locks.** The prior note finds that `allowManagedMcpServersOnly` blocks MCP servers not on the managed list, and the maintainer's policy sets it with a long list. **Inferred.** A channel server is an MCP server, so on that account it would be blocked unless listed. Channels also depend on `channelsEnabled` for organization plans ([channels](https://code.claude.com/docs/en/channels#enterprise-controls)).

### 5. Codex

**Documented.** Codex has an approval policy (`on-request`, `never`, or a `granular` table that auto-rejects some prompt categories) and an `approvals_reviewer` ([approvals and security](https://learn.chatgpt.com/docs/agent-approvals-security), [config reference](https://learn.chatgpt.com/docs/config-file/config-reference)). Its `PermissionRequest` hook (hooks are on by default, non-managed ones need a trust review) runs "when Codex is about to ask for approval" and may print `allow`, `deny` with a `message`, or nothing, in which case "the normal approval flow" continues. `updatedPermissions`, `updatedInput` and `interrupt` are "reserved for future behavior and fail closed today", and the default timeout is 600 seconds ([hooks](https://learn.chatgpt.com/docs/hooks)). `notify` fires only for `agent-turn-complete`, so it is no approval channel ([advanced config](https://learn.chatgpt.com/docs/config-file/config-advanced)). The app-server sends `item/commandExecution/requestApproval` and `item/fileChange/requestApproval`, and the client answers `accept`, `acceptForSession`, `decline`, `cancel` or an execpolicy amendment ([app-server](https://learn.chatgpt.com/docs/app-server)). **Flag for the decision:** allow once and deny exist on both Codex surfaces, but allow-for-session and add-a-rule exist only in the app-server, so a decision that needs them needs its own Codex answer. Codex's current release is rust-v0.163.0 (2026-10-15); no pinned Codex version was checked.

### 6. Changelog, 2.1.292 to 2.1.304

I searched every entry from 2.1.293 to 2.1.304 for permission, hook, prompt, mode, sandbox and managed terms, and read the matches ([CHANGELOG](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md)). A change that uses other words could have been missed.

| Version | Entry | Bearing on items 1 to 3 |
| :- | :- | :- |
| 2.1.295 | Added `onFailure: "block"` for command and HTTP hooks | Item 1. A hook that cannot start, times out or exits unexpectedly can deny a `PermissionRequest` instead of letting the native prompt show. **The pin lacks it.** |
| 2.1.300 | `updatedInput` from `PreToolUse` and `PermissionRequest` hooks is validated like Claude's own input: unknown keys dropped, rejected input denies the call | Item 2. An allow with a changed input can turn into a denial. The pin does not validate it. |
| 2.1.299 | Fixed plan mode running a write that a `PreToolUse` hook or a mod's `tool.check` allowed | Item 3, plan row. The pin runs such a write. AsmAI does not use plan mode. |
| 2.1.299 | Improved enforcement of managed permission rules, managed hooks and org MCP tool names against user-installed mods | Item 4. The prior note flags that its effect is unknown. |
| 2.1.302 | `claude -p` and SDK sessions with no mode set start in `default` (Manual); before, some started in auto | The headless paragraph only. AsmAI sets a mode. |
| 2.1.304 | `decider: "person"` on a mod's `tool.check` answer; a fix for a `PreToolUse` deny reason replaced by an SDK callback hook's timeout error | Item 1, mods route only. |

No entry from 2.1.293 to 2.1.304 changes the `dontAsk` rules, the `PermissionRequest` firing rules, the PreToolUse-in-every-mode rule, or the sandbox auto-allow. Already in the pin, so relevant to what holds on 2.1.292: `--permission-prompts none` (2.1.259), the `Notification` `permission_prompt` for sandbox network requests (2.1.246), channel relay and its trust gate (2.1.81, 2.1.234, 2.1.290), a mod `tool.check` allow no longer skipping a dialog for tools that need an answer (2.1.292), `PreToolUse` approvals no longer bypassing the prompt for network-path reads (2.1.292), and strict-sandbox auto-allow for `FOO=bar python3 app.py` (2.1.292).

## What the facts enable or rule out

This lists consequences. It does not choose.

- **A `PermissionRequest` route needs the agent in `default` mode,** because the event does not fire in `dontAsk`. ADR 0012 chose `dontAsk` to remove prompts that a rule-less Edit or Write, the brace-and-quote case and unforeseen prompts would raise. Those prompts would return and each would need an answer. The hook route can answer tool-use prompts, but not the network-host prompt, the trust dialog or MCP consent.
- **A held hook stops that agent's call for up to its `timeout`,** then falls through to the native prompt. On the pin a hook that fails to start, crashes or is cancelled at Claude Code's timeout is not a denial. The hook's own code can still print a deny before its own deadline. A native prompt nobody can answer is the stall that ADR 0012 removed. The daemon's "waits at a native prompt nobody can answer" line would still show it.
- **A `PreToolUse` route works in `dontAsk`,** but it fires on every call and cannot see the rules' verdict. AsmAI would restate its rules to know which calls to ask about. It cannot override ask or deny rules, critical-path removals or network-path reads.
- **Add a rule and allow for the session are different.** The first goes through a settings file or AsmAI's own record. The second can be `session`-scoped and writes nothing. Nothing documented writes managed settings.
- **A `canUseTool` or `--permission-prompt-tool` route** would change the agents from terminal sessions into `-p` stream-json sessions, in place of the terminals the daemon owns (ADR 0001). Channels relay and a mod are the other interactive-session routes, each with its own dependencies (item 1).
- **A decision on prompts needs a Codex answer only for the parts a Codex hook cannot express,** namely allow-for-session and add-a-rule (item 5).

## Not established

- **That every documented behaviour holds on 2.1.292.** The docs describe 2.1.304. Only the version gates and changelog above separate the two. Confirming a behaviour on the pin needs the pinned binary on a scratch host, in the style of AsmAI's qualification cases.
- **`PermissionRequest` in an interactive `dontAsk` session.** Documented for `-p`, required by C49 on a non-interactive run, not stated for a terminal session.
- **Whether the native dialog is drawn in the PTY while a `PermissionRequest` hook runs, and whether a hook answer that arrives after it is drawn dismisses it.** The pages say "whichever decides first" only for a `canUseTool` or `--permission-prompt-tool` host, and say the dialog stays open beside a channel relay. They are silent for hooks in a terminal session.
- **What a timed-out or failed `PermissionRequest` hook leaves on screen** (inferred above to be the native prompt) and **how several matching `PermissionRequest` hooks resolve** (Claude Code documents precedence only for `PreToolUse`).
- **Hook `updatedPermissions` under `allowManagedPermissionRulesOnly`:** whether session `addRules` or `setMode` take effect, and where a `localSettings` write lands in a worktree with an empty `--setting-sources`.
- **`PreToolUse` `ask` in `dontAsk`** (denied, or does it reach a dialog), and whether a `PreToolUse` `allow` approves an unsandboxed retry or a protected-path write there.
- **Whether `--settings` hooks survive `allowManagedHooksOnly`.**
- **Whether any non-terminal answer exists for the sandbox network-host prompt.** The channels page names tool-use approvals only.
- **The `can_use_tool` control-request wire format** on the pages read, and whether a Go stream-json host's hooks and callback count as SDK ones under the managed locks (open in the prior note).
- **Channels and mods on the pin under AsmAI's flags** (`--strict-mcp-config`, empty `--setting-sources`, `--plugin-dir`), and whether a mod is loaded or blocked by `allowManagedHooksOnly` for a plugin that is not force-enabled.
- **A maximum value for a hook `timeout`.** None is documented.
- **Codex:** behaviour on a pinned Codex version, and whether its hook reaches a managed-policy or trust-review snag in an unattended agent.

## Sources

All accessed 2026-10-20. Claude Code pages were fetched as `.md`.

- Claude Code hooks reference: https://code.claude.com/docs/en/hooks (2026-10-20)
- Claude Code hooks guide: https://code.claude.com/docs/en/hooks-guide (2026-10-20)
- Permissions: https://code.claude.com/docs/en/permissions (2026-10-20)
- Permission modes: https://code.claude.com/docs/en/permission-modes (2026-10-20)
- Sandboxing: https://code.claude.com/docs/en/sandboxing (2026-10-20)
- Headless / programmatic: https://code.claude.com/docs/en/headless (2026-10-20)
- CLI reference: https://code.claude.com/docs/en/cli-reference (2026-10-20)
- Agent SDK permissions: https://code.claude.com/docs/en/agent-sdk/permissions (2026-10-20)
- Agent SDK user input (`canUseTool`): https://code.claude.com/docs/en/agent-sdk/user-input (2026-10-20)
- Agent SDK TypeScript reference: https://code.claude.com/docs/en/agent-sdk/typescript (2026-10-20)
- Settings reference: https://code.claude.com/docs/en/settings-reference (2026-10-20)
- Managed settings: https://code.claude.com/docs/en/managed-settings (2026-10-20)
- Channels and channels reference: https://code.claude.com/docs/en/channels, https://code.claude.com/docs/en/channels-reference (2026-10-20)
- Mods overview and events: https://code.claude.com/docs/en/plugins/mods/overview, https://code.claude.com/docs/en/plugins/mods/events (2026-10-20)
- Remote Control: https://code.claude.com/docs/en/remote-control (2026-10-20)
- Agent view: https://code.claude.com/docs/en/agent-view (2026-10-20)
- Claude Code changelog: https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md (2026-10-20)
- Current release 2.1.304: https://downloads.claude.ai/claude-code-releases/latest and https://github.com/anthropics/claude-code/releases/tag/v2.1.304 (2026-10-20)
- AsmAI Claude provider settings: https://github.com/talvor/asmai/blob/main/internal/providers/claude.go (3f891079aa, 2026-10-20)
- AsmAI probe: https://github.com/talvor/asmai/blob/main/internal/providers/permissions.go (2026-10-20)
- AsmAI hook command: https://github.com/talvor/asmai/blob/main/cmd/asmai/main.go (2026-10-20)
- AsmAI prompt tracking: https://github.com/talvor/asmai/blob/main/internal/daemon/prompts.go (2026-10-20)
- AsmAI qualification: https://github.com/talvor/asmai/blob/main/docs/qualification-harness.md, https://github.com/talvor/asmai/blob/main/qualification/prompts.go (2026-10-20)
- AsmAI ADRs 0011, 0012, 0013: https://github.com/talvor/asmai/blob/main/docs/adr/0011-agents-rely-on-one-user-given-directory-trust.md, https://github.com/talvor/asmai/blob/main/docs/adr/0012-agents-without-the-users-terminal-are-denied-instead-of-prompted.md, https://github.com/talvor/asmai/blob/main/docs/adr/0013-asmai-refuses-to-start-where-claude-code-ignores-its-permission-rules.md (2026-10-20)
- Managed-only policy research (#129): https://github.com/talvor/asmai/blob/research/managed-only-policy-intent/docs/research/managed-only-policy-intent.md (749b0bcbbf, 2026-10-20); issues https://github.com/talvor/asmai/issues/127 to https://github.com/talvor/asmai/issues/131 (2026-10-20)
- Codex hooks: https://learn.chatgpt.com/docs/hooks (also https://developers.openai.com/codex/hooks) (2026-10-20)
- Codex app-server: https://learn.chatgpt.com/docs/app-server (2026-10-20)
- Codex approvals and security: https://learn.chatgpt.com/docs/agent-approvals-security (2026-10-20)
- Codex config reference and advanced config: https://learn.chatgpt.com/docs/config-file/config-reference, https://learn.chatgpt.com/docs/config-file/config-advanced (2026-10-20)
- Codex releases: https://github.com/openai/codex/releases (rust-v0.163.0, 2026-10-20)
