# apphost.revoke

Withdraw an identity's node-local grant for one action.

Revocation takes effect on the next authorization. It does not undo what the
identity did while it held the grant, and it does not close a connection the
identity opened under it.

A signed contract is not withdrawn here. This operation deletes a grant row
recorded by [`apphost.grant`](apphost.grant.md) or by
[`apphost.register`](apphost.register.md); an identity authorized by a
[`mod.auth.signed_contract`](../../auth/types/mod.auth.signed_contract.md)
keeps that authority.

The caller must hold
[`mod.auth.admin_manage_apps_action`](../../auth/types/mod.auth.admin_manage_apps_action.md).
The query is rejected before the grant is withdrawn when the caller is not
authorized, and a refused caller receives no bytes. The operation also rejects
a query that arrived over a [`Link`](../../../core-definitions/link.md),
whatever the caller holds.

## Arguments

* id (identity, required) – The identity whose grant is withdrawn.
* action (string8, required) – Object type of the action to withdraw.
* out (string8) – Output format.

## Returned objects

The operation returns one of:
* An `error_message` object if no grant matched, or the withdrawal failed. The
  message is `grant not found` when the identity holds no grant for the action.
* An `ack` object if the grant was withdrawn.

## Examples

```shellsession
$ astral-query apphost.revoke -id 0282fee8775757cdd8fda8b220195f5b8611312cd145c5a1a3aa55df210e779b2c -action mod.auth.admin_manage_apps_action -out json
{"Type":"ack","Object":null}
```
