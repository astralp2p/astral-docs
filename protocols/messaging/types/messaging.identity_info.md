# messaging.identity_info

A participant's record without any credential: what a caller may read about a
participant whose credentials it does not hold. Returned by
[`messaging.identity`](../ops/messaging.identity.md).

The token is absent from the type rather than left empty, so a caller never
reads a withheld token as a participant that has none.

The record names no expiry either. A participant may hold any number of
[`apphost`](../../apphost/README.md) access tokens, each with its own expiry,
and [`apphost.list_tokens`](../../apphost/ops/apphost.list_tokens.md) answers
them.

## Fields

* Identity ([identity](../../../primitive-types/identity.md)) – The
  participant's identity, minted by the node.
* Alias (string8) – The participant's alias. Empty when no alias is bound.

## Example

```json
{
  "Type": "messaging.identity_info",
  "Object": {
    "Identity": "0282fee8775757cdd8fda8b220195f5b8611312cd145c5a1a3aa55df210e779b2c",
    "Alias": "scout"
  }
}
```
