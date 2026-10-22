# messaging.mailbox_info

A mailbox identity and alias, without credentials. Returned by
[`messaging.mailbox`](../ops/messaging.mailbox.md).

## Fields

* Identity ([identity](../../../primitive-types/identity.md)) – The
  participant's identity, minted by the node.
* Alias (string8) – The participant's alias. Empty when no alias is bound.

## Example

```json
{
  "Type": "messaging.mailbox_info",
  "Object": {
    "Identity": "0282fee8775757cdd8fda8b220195f5b8611312cd145c5a1a3aa55df210e779b2c",
    "Alias": "scout"
  }
}
```
