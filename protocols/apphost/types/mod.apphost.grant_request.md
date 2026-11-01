# mod.apphost.grant_request

The grants a caller asks [`apphost.grant`](../ops/apphost.grant.md) to write
for one identity. Each permit becomes one node-local grant.

## Fields

* Identity (identity) – The identity that receives the grants.
* Duration (duration) – The lifetime of each grant. Zero writes grants that
  last until revoked.
* Permits ([]mod.auth.permit) – The permits to write, with their constraints.

## Example

```json
{
  "Type": "mod.apphost.grant_request",
  "Object": {
    "Identity": "0282fee8775757cdd8fda8b220195f5b8611312cd145c5a1a3aa55df210e779b2c",
    "Duration": 0,
    "Permits": [
      {
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
        ]
      }
    ]
  }
}
```
