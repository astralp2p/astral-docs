# messaging.wait

Wait for matching, unarchived inbox envelopes without reading bodies or changing
stamps. Concurrent waiters can receive the same messages.

Network and `mcp` origins are rejected first. The caller must have a
[hosted mailbox](../../../topics/mailbox-hosting.md#hosting); otherwise the query
is rejected without bytes. After acceptance, the node checks hosting again,
validates `since`, resolves `from`, then waits.

The wait ends on a match, timeout, or channel close. Closing returns no answer;
other input is discarded. The inbox is rechecked on arrival, archive undo, and
every ten seconds. Hosting expiry does not interrupt an admitted wait.

## Arguments

* from (string8) – Sender to match, as a hex public key or directory name.
* since (uint64) – Match only cursors above this value; zero (default) applies no bound.
* timeout (duration) – Requested window. Zero, negative, or absent uses `wait_default` (2m); all windows are capped at `wait_max` (15m).

## Returned objects

* A [`messaging.wait_result`](../types/messaging.wait_result.md) with matching envelopes, next cursor, timeout flag, and granted/elapsed duration.
* An `error_message` reading `not a messaging participant` if hosting ended after acceptance.
* An `error_message` reading `since is a cursor a previous answer gave you, not <since>` if `since` exceeds 9223372036854775807.
* An `error_message` reading `unknown correspondent: <from>` if `from` does not resolve.
* An `error_message` if the inbox cannot be read.

## Examples

```shellsession
$ astral-query messaging.wait -since 412 -timeout 5m -out json
{"Type":"messaging.wait_result","Object":{"Messages":[{"Cursor":413,"ID":"0d41e6b28c5a4f9137be0a62d85c7f14","Box":"inbox","Sender":"0282fee8775757cdd8fda8b220195f5b8611312cd145c5a1a3aa55df210e779b2c","Recipient":"026165850492521f4ac8abd9bd8088123446d126f648ca35e60f88177dc149ceb2","ParentID":"00000000000000000000000000000000","CreatedAt":"2026-09-02T22:24:41.337904Z","ArchivedAt":null,"ReadAt":null,"ReceiptDueAt":null,"ReceiptStoredAt":null,"LandedAt":null,"FailedAt":null,"FetchedAt":null,"Err":null}],"NextSince":413,"TimedOut":false,"Granted":300000000000,"Waited":41200000000}}
```

```shellsession
$ astral-query messaging.wait -since 413 -timeout 1h -out json
{"Type":"messaging.wait_result","Object":{"Messages":[],"NextSince":413,"TimedOut":true,"Granted":900000000000,"Waited":900000631000}}
```
