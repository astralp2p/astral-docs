# messaging.read_messages_result

What one read answers: the messages the caller named and holds, their direct
replies, and the references it does not hold. Returned by
[`messaging.read_messages`](../ops/messaging.read_messages.md).

**The replies are a flat set beside the messages.** The edge is on the reply,
which names its parent in `ParentID`, so a nested answer would carry the same
edge twice. The read goes one level, and the `ChildIDs` on every named message
are what let a reader walk on.

**A reference the caller does not hold is reported rather than refused.** One
wrong identifier does not cost the rest of the batch, and the report does not
say whether the identifier exists anywhere else.

## Fields

* Messages ([]messaging.read_message) – The messages the caller named and holds,
  in the order it named them. Each inbox message among them is stamped read,
  one whose body was left out for room included.
* Replies ([]messaging.read_message) – Their direct replies that have not been
  put away, each message's oldest first, as many as `MaxChildren` allows. Empty
  when `Children` is `none`. When `Children` is `full`, each inbox reply among
  them is stamped read, one whose body was left out for room included.
* NotFound ([]messaging.message_ref) – The references the caller does not hold.

## Example

```json
{
  "Type": "messaging.read_messages_result",
  "Object": {
    "Messages": [
      {
        "Envelope": {
          "Cursor": 412,
          "ID": "7f3a1c9e5b024d6810af2e7c94b5d3a6",
          "Box": "inbox",
          "Sender": "0282fee8775757cdd8fda8b220195f5b8611312cd145c5a1a3aa55df210e779b2c",
          "Recipient": "026165850492521f4ac8abd9bd8088123446d126f648ca35e60f88177dc149ceb2",
          "ParentID": "0d41e6b28c5a4f9137be0a62d85c7f14",
          "CreatedAt": "2026-09-02T22:14:07.104829Z",
          "ArchivedAt": null,
          "ReadAt": "2026-09-02T22:19:55.660411Z",
          "ReceiptDueAt": null,
          "ReceiptStoredAt": null,
          "LandedAt": null,
          "FailedAt": null,
          "FetchedAt": null,
          "Err": null
        },
        "Content": "the index is rebuilt",
        "ChildIDs": ["0196f3c2a8e47b1d9c05e3a7f2b64d18"],
        "Truncated": false
      }
    ],
    "Replies": [
      {
        "Envelope": {
          "Cursor": 418,
          "ID": "0196f3c2a8e47b1d9c05e3a7f2b64d18",
          "Box": "outbox",
          "Sender": "026165850492521f4ac8abd9bd8088123446d126f648ca35e60f88177dc149ceb2",
          "Recipient": "0282fee8775757cdd8fda8b220195f5b8611312cd145c5a1a3aa55df210e779b2c",
          "ParentID": "7f3a1c9e5b024d6810af2e7c94b5d3a6",
          "CreatedAt": "2026-09-02T22:21:03.518204Z",
          "ArchivedAt": null,
          "ReadAt": null,
          "ReceiptDueAt": null,
          "ReceiptStoredAt": null,
          "LandedAt": "2026-09-02T22:21:03.602117Z",
          "FailedAt": null,
          "FetchedAt": null,
          "Err": null
        },
        "Content": null,
        "ChildIDs": null,
        "Truncated": false
      }
    ],
    "NotFound": [
      {"Box": "inbox", "ID": "0d41e6b28c5a4f9137be0a62d85c7f14"}
    ]
  }
}
```
