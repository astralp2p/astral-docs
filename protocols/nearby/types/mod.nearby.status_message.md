# mod.nearby.status_message

The status payload broadcast by a node to nearby peers: a bundle of attached objects assembled by registered composers, followed by the `mod.nearby.status_proof` that nearby appends.

## Fields

* Attachments (bundle) – Bundle of objects representing the node's current status. It holds one `mod.nearby.public_profile` (Visible) or one `mod.nearby.stealth_hint` (Stealth), a `mod.nearby.flag` reading `adoptable` on a Visible node without an owner, and a `mod.nearby.status_proof` as the last attachment.

## Example

A Visible status of a node without an owner:

```json
{
  "Type": "mod.nearby.status_message",
  "Object": {
    "Attachments": [
      {
        "Type": "mod.nearby.flag",
        "Object": "adoptable"
      },
      {
        "Type": "mod.nearby.public_profile",
        "Object": {
          "NodeID": "035d6bfc7818844824354bd5ba1b7c08510139de14aa574e3f53a490814e3eab0e",
          "UserID": null,
          "NodeAlias": "living-room"
        }
      },
      {
        "Type": "mod.nearby.status_proof",
        "Object": {
          "Nonce": "3f9c2a7d11e4b605",
          "Timestamp": "2026-11-05T17:00:00Z",
          "Sig": "MEUCIQDrGjfIXhaxCzTaW42UztGuFdKoPVPe0LDlT+EUc9reXAIgAZ8y4LXgMO4WMYAwLOQ0ZtOk6To/hBflNDXtE8Zpfr0="
        }
      }
    ]
  }
}
```

A Stealth status of a claimed node, its signature wrapped:

```json
{
  "Type": "mod.nearby.status_message",
  "Object": {
    "Attachments": [
      {
        "Type": "mod.nearby.stealth_hint",
        "Object": {
          "Nonce": "7c1a93b50f2e4d18",
          "Commitment": "gAeSwNjMYTM+6Nn7xm75ein0fmJT3K/uE5OLhsBfIN8=",
          "MaskedNode": "pjGXptNxdyi27zXgmvBRinrU2AjvNEVQpE045nAior2E",
          "MaskedUser": "wjIIDUOLppz73JVjL1FgdgUfufed+MkvngoQ859SJOEv"
        }
      },
      {
        "Type": "mod.nearby.status_proof",
        "Object": {
          "Nonce": "2b6d90e4a15c7f38",
          "Timestamp": "2026-11-05T17:00:00Z",
          "Sig": "hXkqyX8EGVWe88f7zSD5pLkPIJy1C5UMyPQNyosLl7vnag45T9j2gCC8LBO1Qhx8LwDQgOJ+gTjk0WXvzLixluyAiHQayA=="
        }
      }
    ]
  }
}
```
