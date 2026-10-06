# Lavish deno compile check

Snapshot: 2026-10-07. This is evidence for [ADR 0010](https://github.com/talvor/AssemblyAI/blob/main/docs/adr/0010-lavish-is-a-deno-compiled-executable-built-per-pin.md) and the [Lavish and skill delivery review](https://github.com/talvor/AssemblyAI/blob/main/.lavish/lavish-delivery-answers.json), not a decision.

## Method

The published lavish-axi 0.1.83 npm package was compiled with `deno compile` on Linux x86_64, using Deno 2.9.6 and cross-checked with 2.9.7. The compiled executable then ran against an isolated Lavish state directory, a separate port and localhost only. Sources: the [npm tarball](https://www.npmjs.com/package/lavish-axi), [deno compile](https://docs.deno.com/runtime/reference/cli/compile/) and [Node and npm compatibility](https://docs.deno.com/runtime/fundamentals/node/).

## The package

- **License and runtime.** MIT, an ES module, `engines.node >= 22`. Nine runtime dependencies resolve to 92 npm packages: 84 MIT, 6 ISC, one BSD-2-Clause and one BSD-3-Clause. None is a native addon, and none has an install script.
- **Floating dependencies.** The package ships no lockfile or shrinkwrap, so an npm install re-resolves its caret ranges each time. On the check date, `axi-sdk-js ^0.1.8` resolved to 0.1.13, and `ws ^8.21.3` to 8.22.0.
- **Assets.** Static files (the review page's script and styles, daisyUI, the Tailwind browser runtime, a 7.6 MB whiteboard bundle and fonts) are read relative to `import.meta.url`. Lavish's own third-party notices list the vendored fonts under MIT and SIL OFL 1.1.
- **Child processes.** Lavish starts a detached background server with `spawn(process.execPath, [<dist/server.mjs>, "server", ...])`. It also runs `lsof` and `ps` for port diagnostics, and launches a browser through `open` unless `--no-open` or `LAVISH_AXI_NO_OPEN=1` is given.
- **Upstream releases.** Upstream publishes to npm only; its GitHub releases carry no executables. There were 81 versions from 2026-05-11 to 2026-10-06.

## Results

- **Compile.** `deno compile -A --minimum-dependency-age 0 --output lavish-axi npm:lavish-axi@0.1.83` produced a 126,220,744-byte ELF executable (43 MB gzipped) that needs glibc 2.27 or newer.
  - Without `--minimum-dependency-age 0`, Deno 2.9 refused the 6-hour-old release: its default minimum dependency age is 24 hours.
  - For comparison, the `node` binary alone is 126.6 MB.
- **Works:**
  - `--version`;
  - `server` in the foreground;
  - opening a review page;
  - every static asset, served at its exact packaged size;
  - an answer posted the way the review page posts it, returned by `poll`;
  - `reply`, `end`, the server-sent events stream;
  - refusal of a cross-origin answer (HTTP 403).
- **Breaks: self-start.** Opening a page with no server running fails. In a compiled executable, `process.execPath` is the executable itself, so the spawned child reads the script path as the HTML file to open ("Lavish Editor expects an HTML file"). A nine-line entry point restores self-start: it drops that script path and imports `dist/server.mjs`.
- **Reproducible.** With a committed `deno.json` and `deno.lock` (92 npm entries, each with an integrity hash) and `--frozen`, two builds with the same output name were byte-identical. The output name is embedded in the executable.
- **Cross-compiles.** `--target aarch64-apple-darwin` produced an 89.6 MB Mach-O executable with a code signature; Deno ad-hoc signs macOS output by default. `--target aarch64-unknown-linux-gnu` also built. The macOS executable was not run.
- **Code cache.** Each compiled executable writes a 1.8 MB V8 code cache to `$TMPDIR/deno-compile-<name>.cache`; `--no-code-cache` disables it.

## Lavish defaults that matter to the daemon

- **Bind address.** Without `LAVISH_AXI_HOST`, Lavish binds 127.0.0.1 and also the machine's Tailscale IPv4 when Tailscale runs.
- **Telemetry.** Usage telemetry goes to an Umami endpoint unless `LAVISH_AXI_TELEMETRY=off`.
- **State and port.** The defaults are `~/.lavish-axi` and port 4387, the same as the user's personal Lavish.
- **Self-stop.** The server stops itself when the last session ends with nothing connected, or after 30 idle minutes.

## The skill bundle, for comparison

Upstream skills v1.3.1's promoted set (engineering and productivity) is 220,009 bytes, or 85,001 bytes gzipped. Size gives no reason to deliver it apart from the executable, and the review kept it embedded ([ADR 0006](https://github.com/talvor/AssemblyAI/blob/main/docs/adr/0006-agents-use-only-the-pinned-skill-bundle.md)).

## Not checked

- A real browser rendering a page from the compiled executable.
- The macOS executable running.
- The Deno runtime's full license set.
- Lavish features AsmAI does not use: whiteboard edits, attachments, export, share and editor plugins.
