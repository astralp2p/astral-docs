# mcp.delete_agent

Remove an agent: withdraw this node's hosting of its
[`messaging`](../../messaging/README.md) mailbox as
[`messaging.delete_identity`](../../messaging/ops/messaging.delete_identity.md)
does — every access token revoked, every node-local grant withdrawn, the alias
unset, the mailbox index entry removed, and the mail it owns on this node
deleted, both boxes, archived or not — and then delete its agent record. A
correspondent's copy of the same message is owned by the correspondent and
stays. The withdrawal is local and not a revocation: the signed hosting contract
and the signed relay contract each stay valid until their expiry. Local-only —
queries from the network are rejected.

The caller must hold
[`mod.auth.admin_manage_apps_action`](../../auth/types/mod.auth.admin_manage_apps_action.md).
The query is rejected before the agent is resolved when the caller is not
authorized, and a refused caller receives no bytes. A query from the network is
rejected before the action is submitted.

**The participant goes first, and its absence is tolerated.** The node deletes
the messaging participant, then the agent record. A participant this node's
mailbox index no longer names — removed by `messaging.delete_identity`, or by an
earlier call whose record deletion failed — is not an error: the record is
deleted all the same, and nothing else is revoked. A record already deleted at
that point is not an error either. Any other failure of the participant's
deletion keeps the agent record, so a repeated call finishes the removal.

**The record is read without the mailbox index.** The node reads the agent
record alone, so this operation reaches the record of an agent whose
participant is gone. `messaging.delete_identity` unsets the alias, so such an
agent is named by its hex public key. `mcp.list_agents` deletes that record
when it reads it, and this operation answers `agent not found` afterwards.
`mcp.agent` deletes no record.

## Arguments

* identity (string8, required) – The agent, given as a hex public key or a name
  resolved via the directory.

## Returned objects

The operation returns one of:
* An `error_message` object reading `unknown identity` if `identity` resolves to
  no identity.
* An `error_message` object reading `agent not found` if the identity resolves
  but no agent is registered under it, or the record cannot be read.
* An `error_message` object if revoking a token or a grant, unsetting the
  alias, deleting the mailbox index entry and its mail, or deleting the record
  failed.
* An `ack` object if the agent was removed.

## Examples

```shellsession
$ astral-query mcp.delete_agent -identity scout -out json
{"Type":"ack","Object":null}
```
