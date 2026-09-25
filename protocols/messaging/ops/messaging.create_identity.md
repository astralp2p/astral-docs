# messaging.create_identity

Mint a new participant: a fresh identity with a signed relay contract, a signed
hosting contract, an optional alias, and an
[`apphost`](../../apphost/README.md) access token, with an empty inbox and
outbox this node hosts. The returned object carries the token, and it is the
only response of this protocol that does. Local-only — queries from the network
are rejected, and so are queries carrying the `mcp` origin.

The caller must hold
[`mod.auth.admin_manage_apps_action`](../../auth/types/mod.auth.admin_manage_apps_action.md).
The query is rejected before an identity is minted when the caller is not
authorized, and a refused caller receives no bytes. A query from the network or
carrying the `mcp` origin is rejected before the action is submitted.

**The hosting contract is the new identity's grant to this node.** The new
identity issues it and this node is its subject. It carries one permit for
[`mod.messaging.host_mailbox_action`](../types/mod.messaging.host_mailbox_action.md),
with `Delegation` 0 and no constraints, and expires after the module's
`hosting_duration`, 87600 hours by default. The node signs it with the keys it
holds for both parties, indexes it, stores it, and records it in its mailbox
index. The relay contract is a separate contract with its own permit: see
[Hosting](../README.md#hosting).

The participant it mints receives nothing until something grants
[`mod.messaging.receive_action`](../types/mod.messaging.receive_action.md) for
it, and sends nothing until something grants
[`mod.messaging.send_action`](../types/mod.messaging.send_action.md). The node
holds no reachability of its own.

## Arguments

* alias (string) – Alias to bind to the new participant. No alias is bound when
  empty, and none is generated: an alias is node-global, so a name the caller
  did not choose contends in a namespace it does not own.
* duration (duration) – Lifetime of the access token. Zero or absent takes the
  module's `token_duration`, 8760 hours by default. It sets neither contract's
  lifetime.

## Returned objects

The operation returns one of:
* An `error_message` object if, in this order, the identity's key cannot be
  stored or indexed, a contract cannot be signed, indexed or stored, the alias
  is already taken (`alias already taken`) or cannot be bound, the token cannot
  be issued, or the mailbox index entry cannot be stored. The index entry is
  written last, so a failed call leaves no mailbox this node serves.
* A `messaging.identity_credential` object describing the new participant,
  including its token.

## Examples

```shellsession
$ astral-query messaging.create_identity -alias scout -out json
{"Type":"messaging.identity_credential","Object":{"Identity":"0282fee8775757cdd8fda8b220195f5b8611312cd145c5a1a3aa55df210e779b2c","Alias":"scout","Token":"h4d8s2w6y1b9t3n7","ExpiresAt":"2027-08-20T10:00:00Z"}}
```

```shellsession
$ astral-query messaging.create_identity -alias scout -out json
{"Type":"error_message","Object":"alias already taken"}
```
