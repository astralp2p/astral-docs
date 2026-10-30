# mod.apphost.grant_request

The request a grant request policy decides. A delegate set by
[`apphost.set_grant_request_policy`](../ops/apphost.set_grant_request_policy.md)
reads one from its input stream for each
[`apphost.request_grant`](../ops/apphost.request_grant.md) call.

## Fields

* Requester (identity) – The identity of the asking session's access token. It
  receives the grants.
* Origin (string8) – The session's web origin. Empty for a local IPC caller.
* Permits ([]mod.auth.permit) – The permits the session asks to hold as
  node-local grants. Each permit carries no constraints.

## Example

```json
{
  "Type": "mod.apphost.grant_request",
  "Object": {
    "Requester": "03864ef025fde8fb587d989186ce6a4a186895ee44a926bfc370e2c366597a3f8f",
    "Origin": "",
    "Permits": [
      { "Action": "mod.auth.see_objects_action" }
    ]
  }
}
```
