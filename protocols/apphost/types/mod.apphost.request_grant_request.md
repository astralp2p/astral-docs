# mod.apphost.request_grant_request

The grants a session asks
[`apphost.request_grant`](../ops/apphost.request_grant.md) for. The grantee is
the identity of the session's access token; the request names no identity.

## Fields

* Permits ([]mod.auth.permit) – The permits the session asks to hold as
  node-local grants, with their constraints.
* Duration (duration) – The lifetime the session asks for each grant. Zero
  asks for grants that last until revoked.

## Example

```json
{
  "Type": "mod.apphost.request_grant_request",
  "Object": {
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
    ],
    "Duration": 0
  }
}
```
