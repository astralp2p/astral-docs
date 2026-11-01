# mod.apphost.grant

One node-local grant, as
[`apphost.list_grants`](../ops/apphost.list_grants.md) reports it. A grant
authorizes its permit on one node and travels nowhere. `ID` names the grant to
[`apphost.revoke`](../ops/apphost.revoke.md).

## Fields

* ID (uint64) – The grant's number on this node. The node never assigns the ID
  of a deleted grant to another grant.
* Permit (mod.auth.permit) – The recorded permit, with its constraints as
  written. `Delegation` is `0`: a grant is never delegable.
* ExpiresAt (optional time) – The instant the grant lapses. Absent when the
  grant lasts until revoked.

## Example

A discovery grant scoped to the `inference` service, lasting until revoked:

```json
{
  "Type": "mod.apphost.grant",
  "Object": {
    "ID": 7,
    "Permit": {
      "Action": "mod.services.service_discovery_action",
      "Constraints": [
        {
          "Type": "mod.services.discovery_scope",
          "Object": {
            "Rules": [
              { "Services": ["inference"], "Nodes": [] }
            ]
          }
        }
      ],
      "Delegation": 0
    },
    "ExpiresAt": null
  }
}
```
