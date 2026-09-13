# mod.auth.admin_manage_apps_action

A [`mod.auth.action`](mod.auth.action.md) requesting permission for the actor to
administer the node's app and agent credentials: the
[`apphost`](../../apphost/README.md) access tokens the node issues, and the
[`mcp`](../../mcp/README.md) agents the node holds.

The action gates six operations — `apphost.create_token`,
`apphost.list_tokens`, `apphost.delete_token`, `mcp.create_agent`,
`mcp.list_agents` and `mcp.delete_agent`. Each operation submits the action
before it reads or changes a credential, and a refused caller receives no
bytes.

Two further operations submit the action as an administrative override rather
than a gate. [`apphost.bind`](../../apphost/ops/apphost.bind.md) and
[`apphost.cancel`](../../apphost/ops/apphost.cancel.md) restrict a caller to the
handlers and queries its own session owns; a holder of this action reaches those
another session owns. Both submit the requesting session's authenticated
identity as the actor, never the caller the query names, so a token-less session
holds nothing here. Neither operation refuses a caller that does not hold the
action — it keeps its own records.

Listing is administration, not a separate read tier. `apphost.list_tokens` and
`mcp.list_agents` hand out the bearer credentials they enumerate, and a bearer
of an access token acts as the identity the token authenticates.

An MCP agent's credential is an apphost access token, so one action covers both
protocols.

`apphost.delete_token`, `mcp.create_agent`, `mcp.list_agents` and
`mcp.delete_agent` also reject a query that arrived over a
[`Link`](../../../core-definitions/link.md), whatever the caller holds.

A permit for this action carries no constraints. A permit whose `Constraints`
bundle is non-empty is refused rather than granted in full.

The user identity and the node's own identity hold this action by default, and
nobody else. A local caller that carries no identity acts as the node's own
identity. Any other identity holds the action through a node-local grant, or
through a [`mod.auth.signed_contract`](mod.auth.signed_contract.md) the node
has indexed. An app or an agent holds nothing by default, so neither mints nor
reads another identity's credentials.

## Fields

* Action ([`mod.auth.action`](mod.auth.action.md)) – The embedded base action carrying the Nonce and ActorID.

## Example

```json
{
  "Type": "mod.auth.admin_manage_apps_action",
  "Object": {
    "Action": {
      "Nonce": "a1b2c3d4e5f60718",
      "ActorID": "0282fee8775757cdd8fda8b220195f5b8611312cd145c5a1a3aa55df210e779b2c"
    }
  }
}
```
