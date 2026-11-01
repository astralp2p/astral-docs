# mod.apphost.register_request

The registration an app sends to
[`apphost.register`](../ops/apphost.register.md). The node passes it to the app
register policy as a
[`mod.apphost.app_register_request`](mod.apphost.app_register_request.md),
which adds the caller's web origin and begins `GrantPermits` with
`mod.auth.serve_apps_action` and `mod.auth.use_blueprints_action`.

## Fields

* Name (string8) – The name the app gives itself. The node does not verify it.
* GrantPermits ([]mod.auth.permit) – The permits the app asks to hold as
  node-local grants, with their constraints.
* ContractPermits ([]mod.auth.permit) – The permits the app asks to hold in a
  signed node→app contract, with their constraints.

## Example

```json
{
  "Type": "mod.apphost.register_request",
  "Object": {
    "Name": "smithd",
    "GrantPermits": [
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
    ],
    "ContractPermits": []
  }
}
```
