# services.ask

A request from a node to a provider app, sent on an open
[`services.advertise`](../ops/services.advertise.md) binding: evaluate one
registered service for one caller and return the complete offering in a
[`services.answer`](services.answer.md).

The node sends at most one `services.ask` per binding and caller at a time.
`Service` names a service the binding registered. `CallerID` is the identity the
node validated for the discovering query; the provider evaluates that identity,
never the node.

`RequestID` correlates the answer. The node draws it at random, never draws
zero, and never issues the same value twice on one binding. A request ID is not
a revision and grants nothing.

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
