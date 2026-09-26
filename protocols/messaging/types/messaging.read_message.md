# messaging.read_message

One message a read answers, with what the read decided about it: the message
without its body, the body when the answer carries it, and the identifiers of
its direct replies. Carried by a
[`messaging.read_messages_result`](messaging.read_messages_result.md).

**The body is a separate field so that its absence is visible.** A body left out
is absent rather than empty, and `Truncated` says whether it was left out for
room or because the caller asked for envelopes.

## Fields

* Envelope ([messaging.envelope](messaging.envelope.md)) – The message without
  its body.
* Content (optional string32) – The body. Absent when the answer does not carry
  it: a reply answered as an envelope, or a message whose body was left out
  because the answer was already full.
* ChildIDs ([]messaging.message_id) – The identifiers of the message's direct
  replies that have not been put away, oldest first — the whole set, whatever
  the answer carries of them. Set on each message the caller named; a reply
  carries none.
* Truncated (bool) – The body was left out because the answer was already full,
  rather than because envelopes were asked for. The message read on its own
  answers its body.

## Example

```json
{
  "Type": "messaging.read_message",
  "Object": {
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
}
```
