# messaging.identity_credential

A participant whose mailbox the node hosts, as the `messaging` module minted it,
including the access token it authenticates with. Returned by
[`messaging.create_identity`](../ops/messaging.create_identity.md), and by no
other operation.

The token is a credential: it is an [`apphost`](../../apphost/README.md) access
token, and a bearer of it acts as the participant.
[`messaging.identity_info`](messaging.identity_info.md) is the record without
the token, and is what a caller reads when it does not hold the participant's
credentials.

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
  "Type": "messaging.identity_credential",
  "Object": {
    "Identity": "0282fee8775757cdd8fda8b220195f5b8611312cd145c5a1a3aa55df210e779b2c",
    "Alias": "scout",
    "Token": "h4d8s2w6y1b9t3n7",
    "ExpiresAt": "2027-08-20T10:00:00Z"
  }
}
```
