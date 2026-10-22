# messaging.mailbox_credential

A new mailbox identity and its apphost bearer token. Returned by
[`messaging.create_mailbox`](../ops/messaging.create_mailbox.md).

## Fields

* Identity ([identity](../../../primitive-types/identity.md)) – The
  participant's identity, minted by the node.
* Alias (string8) – The participant's alias. Empty when no alias is bound.
* Token (string8) – The access token authenticating the participant.
* ExpiresAt ([time](../../../primitive-types/time.md)) – The instant at which
  the token expires.

## Example

```json
{
  "Type": "messaging.mailbox_credential",
  "Object": {
    "Identity": "0282fee8775757cdd8fda8b220195f5b8611312cd145c5a1a3aa55df210e779b2c",
    "Alias": "scout",
    "Token": "h4d8s2w6y1b9t3n7",
    "ExpiresAt": "2027-08-20T10:00:00Z"
  }
}
```
