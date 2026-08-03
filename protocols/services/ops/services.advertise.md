# services.advertise

Advertise a named service on behalf of the caller and keep it available for as
long as the channel stays open. Closing the channel withdraws the
advertisement, so an app that exits or disconnects leaves nothing behind.
Local-only — queries from the network are rejected.

The provider is the caller. There is no argument for it, so an app can
advertise nothing but itself.

Objects sent on the channel after the `ack` replace the advertised `Info`. The
service stays available across such a change: a consumer following
[`services.discover`](services.discover.md) sees the advertisement amended,
not withdrawn and raised again.

By convention the `Name` is the operation namespace the provider serves, so a
consumer that discovers `contacts` calls `contacts.*` without being told a
second name.

## Arguments

* name (string8, required) – The service name to advertise.
* in (string8) – Input format.
* out (string8) – Output format.

## Returned objects

The operation returns one of:
* An `error_message` object if the name is missing, the caller identity is
  missing or zero, or the caller is the node itself.
* An `ack` object once the advertisement stands, followed by the channel
  staying open for the lifetime of the advertisement.

## Examples

```shellsession
$ astral-query services.advertise -name contacts -out text
#[ack]
```

The advertisement stands until the channel closes; the caller keeps the query
open for as long as it serves the service.
