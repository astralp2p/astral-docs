# messaging.wait_result

The result of [`messaging.wait`](../ops/messaging.wait.md): matching inbox
envelopes, the next cursor, and wait timing. Waiting changes no read stamps.

## Fields

* Messages ([]messaging.envelope) – Matching inbox envelopes in write order; empty on timeout.
* NextSince (uint64) – Greatest returned `Cursor`, or the input `since` when none is returned. Passed to the next wait or inbox listing.
* TimedOut (bool) – Granted window ended without a match.
* Granted ([duration](../../../primitive-types/duration.md)) – Allowed wait window, capped by `wait_max`.
* Waited ([duration](../../../primitive-types/duration.md)) – Elapsed wait time; near zero when mail was already available.

## Example

```json
{
  "Type": "messaging.wait_result",
  "Object": {
    "Messages": [
      {
        "Cursor": 413,
        "ID": "0d41e6b28c5a4f9137be0a62d85c7f14",
        "Box": "inbox",
        "Sender": "0282fee8775757cdd8fda8b220195f5b8611312cd145c5a1a3aa55df210e779b2c",
        "Recipient": "026165850492521f4ac8abd9bd8088123446d126f648ca35e60f88177dc149ceb2",
        "ParentID": "00000000000000000000000000000000",
        "CreatedAt": "2026-09-02T22:24:41.337904Z",
        "ArchivedAt": null,
        "ReadAt": null,
        "ReceiptDueAt": null,
        "ReceiptStoredAt": null,
        "LandedAt": null,
        "FailedAt": null,
        "FetchedAt": null,
        "Err": null
      }
    ],
    "NextSince": 413,
    "TimedOut": false,
    "Granted": 120000000000,
    "Waited": 41200000000
  }
}
```
