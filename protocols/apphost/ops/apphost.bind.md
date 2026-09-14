# apphost.bind

Bind the lifetime of registered IPC handlers to the query session. The host
acknowledges, then waits for a `mod.apphost.bind_msg` containing the token of
the handlers to bind. Local-only — queries from the network are rejected.

When the session closes, the host removes the handlers matching both that token
and the session that bound. A handler records the guest session that registered
it, named by its authenticated
[`Identity`](../../../core-definitions/identity.md). A bind token is a label the
binding app picks for itself, so two apps can pick the same one; matching the
owner as well keeps one app's bind from removing another app's handlers.

A handler registered by a token-less session records no owner. A token-less bind
removes exactly those handlers, and neither reaches the other's.

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

The caller must then send a `mod.apphost.bind_msg` over the same channel.

## Examples

```shellsession
$ astral-query apphost.bind -out text
#[ack]
```
