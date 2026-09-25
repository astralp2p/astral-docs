# messaging.delete_identity

Withdraw this node's hosting of a participant's mailbox: revoke every
[`apphost`](../../apphost/README.md) access token the identity holds, expired
ones included, withdraw every node-local grant it holds, unset its alias, remove
its mailbox index entry, and delete the mail it owns on this node — both boxes,
archived or not. A correspondent's copy of the same message is owned by the
correspondent and stays. Local-only — queries from the network are rejected, and
so are queries carrying the `mcp` origin.

The caller must hold
[`mod.auth.admin_manage_apps_action`](../../auth/types/mod.auth.admin_manage_apps_action.md).
The query is rejected before the participant is resolved when the caller is not
authorized, and a refused caller receives no bytes. A query from the network or
carrying the `mcp` origin is rejected before the action is submitted.

**The withdrawal is local and not a revocation.** The signed hosting contract
and the signed relay contract are left as they are: each stays valid until its
expiry, wherever a copy is held. This node stops hosting the mailbox because its
mailbox index no longer names it. See [Hosting](../README.md#hosting).

**A failure keeps the index entry.** A token or a grant left standing keeps
authorizing whoever presents the identity, and the index entry is the record
that names it, so a call that fails part-way can be repeated and the repeat
finishes the removal. The index entry and the mail the identity owns are removed
together, in one write.

An [`mcp`](../../mcp/README.md) agent is removed with
[`mcp.delete_agent`](../../mcp/ops/mcp.delete_agent.md), which removes the
agent record as well.

## Arguments

* identity (string8, required) – The participant, given as a hex public key or a
  name resolved via the directory.

## Returned objects

The operation returns one of:
* An `error_message` object reading `unknown identity` if `identity` resolves to
  no identity.
* An `error_message` object reading `identity not found` if the identity
  resolves but this node's mailbox index has no entry for it.
* An `error_message` object if revoking a token or a grant, unsetting the
  alias, or deleting the index entry and its mail failed.
* An `ack` object if the participant was removed.

## Examples

```shellsession
$ astral-query messaging.delete_identity -identity scout -out json
{"Type":"ack","Object":null}
```
