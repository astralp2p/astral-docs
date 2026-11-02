# apphost.revoke

Withdraw one node-local grant of an identity, or every grant it holds for one
action.

Revocation takes effect on the next authorization. It does not undo what the
identity did while it held the grant, and it does not close a connection the
identity opened under it.

An identity can hold several grants for one action
([Grants](../README.md#grants)). `id` withdraws the one grant it names and
leaves the identity's other grants for the same action in place. `action`
withdraws every grant of the identity for that action. Narrowing a grant is
granting the narrow permit, then revoking the wide grant by `id`.

A signed contract is not withdrawn here. This operation deletes grant rows
recorded by [`apphost.grant`](apphost.grant.md),
[`apphost.request_grant`](apphost.request_grant.md) or
[`apphost.register`](apphost.register.md); an identity authorized by a
[`mod.auth.signed_contract`](../../auth/types/mod.auth.signed_contract.md)
keeps that authority.

The caller must hold
[`mod.auth.admin_manage_apps_action`](../../auth/types/mod.auth.admin_manage_apps_action.md).
The operation answers an `error_message` reading `not permitted` before the
grant is withdrawn when the caller is not authorized. The operation also answers
`origin not allowed: network` to a query that arrived over a
[`Link`](../../../core-definitions/link.md), whatever the caller holds.

## Arguments

* identity (string8, required) – The identity whose grant is withdrawn, given
  as a hex public key or a name resolved via the directory.
* id (uint64) – The ID of one grant, as
  [`apphost.list_grants`](apphost.list_grants.md) reports it. The grant must
  belong to `identity`. A grant ID is not an Object ID.
* action (string8) – Object type of the action whose grants are all withdrawn.
* out (string8) – Output format.

Exactly one of `id` and `action` is given. Grant IDs start at 1, so `id` `0`
reads as absent.

## Returned objects

The operation returns one of:
* An `error_message` object if `identity` does not resolve.
* An `error_message` object reading `missing identity` if `identity` resolves to
  the anonymous identity.
* An `error_message` object reading `give id or action, not both` if both are
  given.
* An `error_message` object reading `missing id or action` if neither is given.
* An `error_message` object if no grant matched, or the withdrawal failed. The
  message is `grant not found` when `id` names no grant of `identity`, or when
  the identity holds no grant for `action`.
* An `ack` object if the grant or grants were withdrawn.

## Examples

Withdrawing one grant by its ID:

```shellsession
$ astral-query apphost.revoke -identity 0282fee8775757cdd8fda8b220195f5b8611312cd145c5a1a3aa55df210e779b2c -id 7 -out json
{"Type":"ack","Object":null}
```

Withdrawing every grant for one action:

```shellsession
$ astral-query apphost.revoke -identity 0282fee8775757cdd8fda8b220195f5b8611312cd145c5a1a3aa55df210e779b2c -action mod.auth.admin_manage_apps_action -out json
{"Type":"ack","Object":null}
```
