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
* Vfs (bool, optional) – `true` asks the node to create the
  [`VFS`](../../vfs/README.md) of the new identity, `false` registers the app
  without one. Absent means `true`.
* Evaluator (bool, optional) – `true` names the app the
  [evaluator](../../vfs/README.md#evaluator) of its own VFS, with the endpoint
  `astral://<app identity>:vfs.authorize`; `false` leaves the evaluator empty.
  Absent means `true`. Without a VFS it has no effect.

In JSON, an absent or `null` `Vfs` or `Evaluator` means `true`. The binary
encoding writes a presence flag before each of the two fields, so a binary
encoder always writes the flag, and a cleared flag means `true`.

An app that names itself the evaluator serves `vfs.authorize`. An app that
does not serve it registers with `Evaluator` false, because every read or
write the built-in rules refuse otherwise waits for the question to time out.

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
    "ContractPermits": [],
    "Vfs": true,
    "Evaluator": false
  }
}
```
