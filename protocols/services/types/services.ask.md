# services.ask

A node's request on a [`services.advertise`](../ops/services.advertise.md)
binding to evaluate one registered service for `CallerID`. The provider returns
a complete [`services.answer`](services.answer.md); its `Update.Name` must equal
`Service`, or the binding fails.

At most one ask is outstanding per binding and caller. `CallerID` is the
validated discovery identity. `RequestID` is random, nonzero, and never reused
on the binding; it correlates the answer and grants no permission.

## Fields

* RequestID (nonce64) – Correlation value the answer echoes.
* CallerID (identity) – The caller whose offering the provider evaluates.
* Service (string8) – The registered service to evaluate.

## Example

```json
{
  "Type": "services.ask",
  "Object": {
    "RequestID": "9f2c41aa07d3e815",
    "CallerID": "0282fee8775757cdd8fda8b220195f5b8611312cd145c5a1a3aa55df210e779b2c",
    "Service": "player"
  }
}
```
