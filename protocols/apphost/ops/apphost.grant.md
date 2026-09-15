# apphost.grant

Record a node-local grant of one action for an identity that already exists.

A grant is this node's own record that an identity may perform an action here.
The grant is recorded, not signed: it authorizes on this node and travels
nowhere. Granting replaces whatever the identity held for the same action, so
re-granting a narrower permit takes authority away.

[`apphost.register`](apphost.register.md) writes a grant only for the identity
it mints. This operation writes one for an identity the node already knows, so
an app reaches a newly guarded operation without re-registering under a fresh
identity.

The caller must hold
[`mod.auth.admin_manage_apps_action`](../../auth/types/mod.auth.admin_manage_apps_action.md).
The query is rejected before the grant is written when the caller is not
authorized, and a refused caller receives no bytes. The operation also rejects
a query that arrived over a [`Link`](../../../core-definitions/link.md),
whatever the caller holds.

The recorded permit carries no constraints and no delegation. Constraints are
refused rather than granted in full, and a grant is not portable evidence, so a
hop count on it would describe authority it cannot carry.

## Arguments

* identity (string8, required) – The identity the grant is recorded for, given
  as a hex public key or a name resolved via the directory.
* action (string8, required) – Object type of the action granted (e.g.
  `mod.auth.admin_manage_apps_action`).
* duration (duration) – Lifetime of the grant. Omitted grants until the grant
  is revoked.
* out (string8) – Output format.

## Returned objects

The operation returns one of:
* An `error_message` object if `identity` does not resolve.
* An `error_message` object reading `missing identity` if `identity` resolves to
  the anonymous identity.
* An `error_message` object if the grant was not written.
* An `ack` object if the grant was recorded.

## Examples

```shellsession
$ astral-query apphost.grant -identity 0282fee8775757cdd8fda8b220195f5b8611312cd145c5a1a3aa55df210e779b2c -action mod.auth.admin_manage_apps_action -out json
{"Type":"ack","Object":null}
```

Granting for a bounded time:

```shellsession
$ astral-query apphost.grant -identity 0282fee8775757cdd8fda8b220195f5b8611312cd145c5a1a3aa55df210e779b2c -action mod.auth.see_node_state_action -duration 720h -out json
{"Type":"ack","Object":null}
```
