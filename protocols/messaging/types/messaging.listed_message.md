# messaging.listed_message

One row of a page or a change read: its envelope and its revision. Carried by
[`messaging.message_page`](messaging.message_page.md) and
[`messaging.message_changes`](messaging.message_changes.md).

**The revision is beside the envelope, not in it.**
[`messaging.envelope`](messaging.envelope.md) is what
[`messaging.list_messages`](../ops/messaging.list_messages.md) and
[`messaging.wait`](../ops/messaging.wait.md) answer, and its encoding stays as
it is.

## Fields

* Rev (uint64) – The row's position in the node's order of changes. Every write
  that changes a field of the envelope gives the row a new, greater one. Opaque:
  only its order is a fact.
* Envelope ([messaging.envelope](messaging.envelope.md)) – The row without its
  body.

## Example

```json
{
  "Type": "messaging.listed_message",
  "Object": {
    "Rev": 918,
    "Envelope": {
      "Cursor": 415,
      "ID": "0d41e6b28c5a4f9137be0a62d85c7f14",
      "Box": "inbox",
      "Sender": "0282fee8775757cdd8fda8b220195f5b8611312cd145c5a1a3aa55df210e779b2c",
      "Recipient": "026165850492521f4ac8abd9bd8088123446d126f648ca35e60f88177dc149ceb2",
      "ParentID": "7f3a1c9e5b024d6810af2e7c94b5d3a6",
      "CreatedAt": "2026-09-02T22:16:40.215004Z",
      "ArchivedAt": null,
      "ReadAt": null,
      "ReceiptDueAt": null,
      "ReceiptStoredAt": null,
      "LandedAt": null,
      "FailedAt": null,
      "FetchedAt": null,
      "Err": null
    }
  }
}
```
