# mod.user.contract_accept_decision

A contract accept policy's answer to a
[`mod.user.contract_accept_request`](mod.user.contract_accept_request.md). A
delegate set by
[`user.set_contract_accept_policy`](../ops/user.set_contract_accept_policy.md)
writes one to its output stream.

## Fields

* Allow (bool) – `true` accepts the contract, and the node activates it.
  `false` declines it.

## Example

```json
{
  "Type": "mod.user.contract_accept_decision",
  "Object": {
    "Allow": true
  }
}
```
