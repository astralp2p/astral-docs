# apphost.cancel

Cancel an en-route query by nonce. Local-only — queries from the network are
rejected.

A query records the guest session that launched it. That session cancels it,
and no other does. The record names the session's authenticated
[`Identity`](../../../core-definitions/identity.md), not its connection, so a
second connection authenticating with the same token cancels the query too. A
caller-supplied identity establishes no ownership.

A query launched by a token-less session records no owner. Such a query stays
cancellable by any local session.

A caller holding
[`mod.auth.admin_manage_apps_action`](../../auth/types/mod.auth.admin_manage_apps_action.md)
cancels a query owned by another session. The action carries the requesting
session's authenticated identity as its actor, so a token-less session never
reaches this path.

A query owned by another session is answered as a query that is not en route.
The two responses are identical, so a caller learns nothing about the nonces
other apps hold.

The record lives only while the query is en route. The host writes it before
routing the query and removes it once routing returns.

A nonce already en route keeps its first owner. A second query choosing that
nonce does not take the record over, and is uncancellable.

## Arguments

* id (nonce64, required) – Nonce of the query to cancel.
* cause (string) – Optional cause attached to the cancellation as an error.

## Returned objects

The operation returns one of:
* An `error_message` object if the query is not en route, or the caller may not
  cancel it. The two cases are indistinguishable.
* An `ack` object if the query was cancelled.

## Examples

```shellsession
$ astral-query apphost.cancel -id a3f1c2d4e5b6f708 -cause "user aborted" -out text
#[ack]
```
