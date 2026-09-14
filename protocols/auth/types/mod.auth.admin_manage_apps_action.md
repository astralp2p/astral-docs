# mod.auth.admin_manage_apps_action

A [`mod.auth.action`](mod.auth.action.md) requesting permission for the actor to
administer the node's app and agent credentials and the node-local grants it
records: the [`apphost`](../../apphost/README.md) access tokens the node issues,
the [`mcp`](../../mcp/README.md) agents the node holds, and the grants that say
what an identity may do here.

The action gates nine operations — `apphost.create_token`,
`apphost.list_tokens`, `apphost.delete_token`, `apphost.grant`,
`apphost.revoke`, `apphost.list_grants`, `mcp.create_agent`,
`mcp.list_agents` and `mcp.delete_agent`. Each operation submits the action
before it reads or changes a credential or a grant, and a refused caller
receives no bytes.

Listing is administration, not a separate read tier. `apphost.list_tokens` and
`mcp.list_agents` hand out the bearer credentials they enumerate, and a bearer
of an access token acts as the identity the token authenticates.

Granting is administration on the same footing. A caller that may mint an access
token for any identity already acts as that identity, so recording a grant
confers no authority this action did not already carry.
[`apphost.grant`](../../apphost/ops/apphost.grant.md),
[`apphost.revoke`](../../apphost/ops/apphost.revoke.md) and
[`apphost.list_grants`](../../apphost/ops/apphost.list_grants.md) therefore
share the action rather than naming a tenth one.

An MCP agent's credential is an apphost access token, so one action covers both
protocols.

`apphost.delete_token`, `apphost.grant`, `apphost.revoke`,
`apphost.list_grants`, `mcp.create_agent`, `mcp.list_agents` and
`mcp.delete_agent` also reject a query that arrived over a
[`Link`](../../../core-definitions/link.md), whatever the caller holds. A grant
authorizes on one node and travels nowhere, so it is neither written nor
enumerated over a link.

A permit for this action carries no constraints. A permit whose `Constraints`
bundle is non-empty is refused rather than granted in full.

The user identity and the node's own identity hold this action by default, and
nobody else. A local caller that carries no identity acts as the node's own
identity. Any other identity holds the action through a node-local grant, which
[`apphost.grant`](../../apphost/ops/apphost.grant.md) records, or through a
[`mod.auth.signed_contract`](mod.auth.signed_contract.md) the node has indexed.
An app or an agent holds nothing by default, so neither mints nor reads another
identity's credentials.

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
