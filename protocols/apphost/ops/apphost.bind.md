# apphost.bind

Bind the lifetime of registered IPC handlers to the query session. The host
acknowledges, then waits for a `mod.apphost.bind_msg` containing the token of
the handlers to bind. Local-only — a query from the network is answered
`origin not allowed: network`.

When the session closes, the host removes the handlers matching both that token
and the session that bound. A handler records the guest session that registered
it, named by its authenticated
[`Identity`](../../../core-definitions/identity.md). A bind token is a label the
binding app picks for itself, so two apps can pick the same one; matching the
owner as well keeps one app's bind from removing another app's handlers.

A handler registered by a token-less session records no owner. A token-less bind
removes exactly those handlers, and neither reaches the other's.

The host also ends a session itself. When a dial of a handler's endpoint fails,
the host removes that handler and ends the session that bound the handler's
token for the handler's recorded owner. Ending the session removes every
handler that session bound, then closes the session's channel, so an app that
reconnects on a closed bind channel registers its handlers again. The host ends
at most one session per owner in any 30 s window. A dial failure inside the
window ends the session when the window closes. When no session of the owner
holds the token, the end applies to the next session of that owner that binds
the token within 30 s, because an app can register a handler before it binds
the handler's token. A failed dial of a handler that another query already
removed ends no session. A handler that records no owner has no session to
end, and its failed dial removes only that handler.

A session holding
[`mod.auth.admin_manage_apps_action`](../../auth/types/mod.auth.admin_manage_apps_action.md)
removes by token alone, whatever owner the handlers record. The action is
submitted once, when the session binds, carrying the session's authenticated
identity as its actor. A token-less session never reaches this path.

## Arguments

This operation takes no arguments.

## Returned objects

The operation streams:
* An `ack` object once the session is bound.
* An `error_message` object if the bind message could not be processed.

The caller must then send a `mod.apphost.bind_msg` over the same channel. The
`ack` is a readiness `ack` — see
[Op modes & composition § Control signals](../../../topics/op-modes.md#control-signals).

## Examples

```shellsession
$ astral-query apphost.bind -out text
#[ack]
```
