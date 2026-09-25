# messaging.wait_result

What one park on the caller's inbox came back with: the messages it found, the
cursor to pass back, and the window it was given beside the time it held.
Returned by [`messaging.wait`](../ops/messaging.wait.md).

**The answer names the window it was granted beside the time it spent.** The
grant is the deployment's and the ask the caller's, so a clamp reads as two
numbers rather than as a silence the caller misreads.

## Fields

* Messages ([]messaging.envelope) – The inbox messages the park matched, without
  their bodies, in the order the node wrote them. Empty when the window closed
  with nothing new.
* NextSince (uint64) – The greatest `Cursor` among `Messages`, or the `since`
  the park was given when `Messages` is empty. A caller passes it back as
  `since` to see only what was written after.
* TimedOut (bool) – The granted window closed with nothing new.
* Granted ([duration](../../../primitive-types/duration.md)) – The window this
  park was given: the caller's `timeout` or the module's `wait_default`, never
  over its `wait_max`.
* Waited ([duration](../../../primitive-types/duration.md)) – How long the node
  held the park before answering. Near zero means the answer was already
  waiting.

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
