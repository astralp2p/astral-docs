# apphost.withdraw_relay

Take back, on this node, the relay contract of an app or a mailbox: the
[`mod.nodes.relay_for_action`](../../nodes/types/mod.nodes.relay_for_action.md)
contract the identity issued to this node, its host. From the next
authorization on, this node no longer accepts a query relayed for the identity
under that contract, and no longer attaches the contract to the identity's
outgoing queries.

The withdrawal holds on this node alone. A copy of the contract on a sibling
stays, and so do the identity's access tokens
([`apphost.delete_token`](apphost.delete_token.md)).

The node refuses the query in these cases, in this order:

* The query arrived over a [`Link`](../../../core-definitions/link.md):
  answered with `origin not allowed: network`.
* The caller does not hold
  [`mod.auth.admin_manage_apps_action`](../../auth/types/mod.auth.admin_manage_apps_action.md):
  answered with `not permitted`.
* `identity` does not resolve: answered with an `error_message`.

## Arguments

* identity (string8, required) – The app or mailbox whose relay contract is
  taken back, given as a hex public key or a name resolved via the directory.
* out (string, optional) – Output encoding format. Defaults to the channel
  default.

## Returned objects

The operation returns one of:
* An `error_message` named in the cases above.
* An `error_message` reading `relay contract not found` if this node holds no
  relay contract of the identity.
* An `error_message` if the withdrawal fails.
* An `ack` once every relay contract of the identity is withdrawn.

## Examples

```shellsession
$ astral-query apphost.withdraw_relay -identity player -out json
{"Type":"ack","Object":null}
```
