# shell.shell

Open an interactive shell session on the node. The connection carries a line-oriented text protocol over the raw byte stream.

The caller must hold [`mod.shell.shell_action`](../types/mod.shell.shell_action.md). The query is rejected before it is accepted when the caller is not authorized, and a refused caller receives no bytes. The `as` argument is gated by the `mod.auth.sudo_action` action: the caller must be authorized to act as the target identity.

## Arguments

* as (string8) – Identity to run the session as, given as a hex public key or alias. Defaults to the caller's identity.

## Returned objects

The op accepts the query as a raw byte stream. No typed objects are exchanged; all interaction is line-oriented text over the raw connection. The session repeats these steps:

1. It writes the prompt, a [`mod.shell.prompt`](../types/mod.shell.prompt.md) rendered as `<GuestID>@<HostID>> ` with each identity shown by its display name in the node's directory.
2. It reads one line and splits it into words with shell quoting. A line with unbalanced quotes prints `quote mismatch`, and an empty line prints nothing.
3. The first word names an op and the remaining words are its arguments as `-name value` pairs. The session routes that query to the node as the session's identity and copies the raw stream in both directions until the op's response ends.
4. It prints `ok` after the op ends, or `error: <reason>` when the query cannot be routed.

The line `exit` ends the session. The session also ends when the connection closes or EOF is reached.

## Examples

```shellsession
$ astral-query shell.shell
alice@mynode> help
```
