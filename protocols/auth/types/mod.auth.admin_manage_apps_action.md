# mod.auth.admin_manage_apps_action

A [`mod.auth.action`](mod.auth.action.md) requesting permission for the actor to
administer the node's app, agent and participant credentials: the
[`apphost`](../../apphost/README.md) access tokens the node issues and the relay
contracts it signs, the [`mcp`](../../mcp/README.md) agents, the
[`messaging`](../../messaging/README.md) participants whose mailboxes the node
hosts, and the external authorizers the node asks.

The action gates twelve operations — `apphost.create_token`,
`apphost.list_tokens`, `apphost.delete_token`,
[`apphost.withdraw_relay`](../../apphost/ops/apphost.withdraw_relay.md),
`mcp.create_agent`, `mcp.list_agents`, `mcp.delete_agent`,
`messaging.create_mailbox`, `messaging.delete_mailbox`,
[`auth.set_authorizer`](../ops/auth.set_authorizer.md),
[`auth.list_authorizers`](../ops/auth.list_authorizers.md) and
[`auth.remove_authorizer`](../ops/auth.remove_authorizer.md). Each operation
submits the action before it reads or changes a credential or an assignment,
and answers a refused caller with an `error_message` reading `not permitted`.

Two further operations submit the action as an administrative override rather
than a gate. [`apphost.bind`](../../apphost/ops/apphost.bind.md) and
[`apphost.cancel`](../../apphost/ops/apphost.cancel.md) restrict a caller to the
handlers and queries its own session owns; a holder of this action reaches those
another session owns, and for `apphost.cancel` those no session owns. Both
submit the requesting session's authenticated identity as the actor, never the
caller the query names, so a token-less session holds nothing here. Neither
operation refuses a caller that does not hold the action — it keeps its own
records.

Listing is administration, not a separate read tier. `apphost.list_tokens` and
`mcp.list_agents` hand out the bearer credentials they enumerate, and a bearer
of an access token acts as the identity the token authenticates.

An MCP agent's credential and a messaging participant's credential are apphost
access tokens, so one action covers all three protocols.

`apphost.create_token`, `apphost.list_tokens`, `apphost.delete_token`,
`apphost.withdraw_relay`, `mcp.create_agent`, `mcp.list_agents`,
`mcp.delete_agent`, `messaging.create_mailbox`, `messaging.delete_mailbox` and
`auth.set_authorizer` also answer `origin not allowed: network` to a query
that arrived over a [`Link`](../../../core-definitions/link.md), whatever the
caller holds. A `privileged_member` node holds the action through the swarm
root, so this refusal is what keeps it from minting credentials on another
node over a link.

A permit for this action carries no constraints. A permit whose `Constraints`
bundle is non-empty is refused rather than granted in full.

## Holders

* The user identity and the node's own identity. A local caller that carries
  no identity acts as the node's own identity.
* A `privileged_member` node of the swarm, through the swarm root
  ([auth](../README.md)).
* Any other identity only through a contract chain the node has indexed, back
  to a holder: an app through a contract its host signed to carry out an
  Approval ([apphost, Contract requests](../../apphost/README.md#contract-requests)).

On a `fresh` node, any local program, or any page open in a local browser,
obtains the action by naming it in the permits of
[`sys.register_manager`](../../sys/ops/sys.register_manager.md): the fresh node
is its own root and signs the manager's contract at once. The holder then mints
or reads another identity's credentials.

## Fields

* Action ([`mod.auth.action`](mod.auth.action.md)) – The embedded base action carrying the Nonce and ActorID.

In JSON the embedded action's fields appear directly in the `Object` value, not
under an `Action` key.

## Example

```json
{
  "Type": "mod.auth.admin_manage_apps_action",
  "Object": {
    "Nonce": "a1b2c3d4e5f60718",
    "ActorID": "0282fee8775757cdd8fda8b220195f5b8611312cd145c5a1a3aa55df210e779b2c"
  }
}
```
