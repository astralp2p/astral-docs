# shell

The `shell` protocol provides an interactive command-line interface to the node over a raw byte stream. Opening a session requires the [`mod.shell.shell_action`](types/mod.shell.shell_action.md) authorization check. Sessions run as the caller's identity by default; the `as` argument allows impersonation gated by the `mod.auth.sudo_action` authorization check.

`shell.shell` opens an interactive session. `shell.spec` streams `routing.op_spec` objects describing the ops registered under the shell module.

The session renders its prompt, a [`mod.shell.prompt`](types/mod.shell.prompt.md), as text and exchanges no typed objects.
