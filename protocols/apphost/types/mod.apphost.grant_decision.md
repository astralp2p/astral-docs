# mod.apphost.grant_decision

A grant request policy's answer to a
[`mod.apphost.grant_request`](mod.apphost.grant_request.md). A delegate set by
[`apphost.set_grant_request_policy`](../ops/apphost.set_grant_request_policy.md)
writes one to its output stream.

## Fields

* Allow (bool) – `true` grants every permit the request lists. `false` refuses
  them all.

## Example

```json
{
  "Type": "mod.apphost.grant_decision",
  "Object": {
    "Allow": true
  }
}
```
