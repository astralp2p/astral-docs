# messaging.wait

Park until the caller's inbox holds a message it has not put away, and answer
what the park found, without the bodies. Nothing is stamped and nothing is
taken: the park and the read are separate acts, and two callers waiting at once
are answered the same messages. Local-only — queries from the network are
rejected, and so are queries carrying the `mcp` origin.

This node must host the caller's mailbox. The query is rejected before
anything is read when the caller is the zero identity or this node does not host
the caller's mailbox, as [Hosting](../README.md#hosting) defines it, and a
refused caller receives no bytes. A query from the network or carrying the `mcp`
origin is rejected before the caller is checked.

**The query is accepted before the park begins.** A park lasts minutes, so the
caller holds an open channel while the node waits for mail rather than a query
that is not yet answered. The park ends when the inbox holds a matching message,
when the granted window closes, or when the caller closes the channel. A park
the caller ended is answered nothing. The node reads and discards whatever the
caller writes after the query, so only the end of the channel ends the park
early. The node looks at the inbox again when a message lands in it or one is
put back with `undo`, and every ten seconds besides.

**The window is granted, never refused.** A caller naming no window is granted
the module's `wait_default`, 2 minutes by default. An ask over the module's
`wait_max`, 15 minutes by default, is granted `wait_max`: a refusal would make
the deployment's ceiling part of every client's configuration, where a clamp is
read off the answer's `Granted`.

## Arguments

* from (string8) – Waits only for what this correspondent writes, given as a hex
  public key or a name resolved via the directory.
* since (uint64) – Waits only for what is written after this cursor: the
  `NextSince` of an earlier answer, or the greatest `Cursor` a listing answered.
  Defaults to 0, which narrows nothing.
* timeout (duration) – The window to park for. Zero, negative or absent takes
  the module's `wait_default`, and an ask over the module's `wait_max` is
  granted `wait_max`.

## Returned objects

Once the query is accepted, the operation checks again that this node hosts
the caller's mailbox, then checks `since` and resolves `from`, in that order,
before it parks.

The operation returns one of:
* An `error_message` object reading `not a messaging participant` if this node
  stopped hosting the caller's mailbox after the query was accepted.
* An `error_message` object reading
  `since is a cursor a previous answer gave you, not <since>` if `since` is
  over 9223372036854775807.
* An `error_message` object reading `unknown correspondent: <from>` if `from`
  resolves to no identity.
* An `error_message` object if the inbox cannot be read.
* A `messaging.wait_result` object carrying the messages found, the cursor to
  pass back as `since`, whether the window closed with nothing new, the window
  granted, and the time the park was held.

## Examples

```shellsession
$ astral-query messaging.wait -since 412 -timeout 5m -out json
{"Type":"messaging.wait_result","Object":{"Messages":[{"Cursor":413,"ID":"0d41e6b28c5a4f9137be0a62d85c7f14","Box":"inbox","Sender":"0282fee8775757cdd8fda8b220195f5b8611312cd145c5a1a3aa55df210e779b2c","Recipient":"026165850492521f4ac8abd9bd8088123446d126f648ca35e60f88177dc149ceb2","ParentID":"00000000000000000000000000000000","CreatedAt":"2026-09-02T22:24:41.337904Z","ArchivedAt":null,"ReadAt":null,"ReceiptDueAt":null,"ReceiptStoredAt":null,"LandedAt":null,"FailedAt":null,"FetchedAt":null,"Err":null}],"NextSince":413,"TimedOut":false,"Granted":300000000000,"Waited":41200000000}}
```

```shellsession
$ astral-query messaging.wait -since 413 -timeout 1h -out json
{"Type":"messaging.wait_result","Object":{"Messages":[],"NextSince":413,"TimedOut":true,"Granted":900000000000,"Waited":900000631000}}
```
