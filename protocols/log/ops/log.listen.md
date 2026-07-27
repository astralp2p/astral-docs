# log.listen

Subscribe to the node's live log stream. The operation streams `astrald.log.entry` objects to the caller as log entries are produced. The stream runs until the caller disconnects or the node disconnects a stalled caller.

## Returned objects

The operation returns a continuous stream of `astrald.log.entry` objects.

Delivery is buffered and lossy under backpressure. The node buffers a bounded number of entries per subscriber (default 256). While the buffer is full, new entries for that subscriber are dropped; delivered entries keep their production order.

Dropped entries are announced in-band. Before the next delivered entry, the node inserts a drop notice: a regular `astrald.log.entry` whose `Origin` is the node identity, whose `Level` is 0, whose `Time` is the time of the first dropped entry, and whose body is a single `string32` of the form `log.listen: dropped <count> entries`.

The node disconnects a subscriber whose single write stalls longer than the send timeout (default 5 seconds) by closing the connection. The stream ends with neither `eos` nor an error object — a stalled subscriber cannot receive a terminator. The stream has no other server-side terminator; it ends when the caller closes the connection.

## Examples

```shellsession
$ astral-query log.listen -out json
{"Type":"astrald.log.entry","Object":{"Origin":"02bef8840eb35ef2ae3c83c07cb5779278904f99cb4103f71e37cc69931ae5e15f","Level":1,"Time":"2026-06-10T12:00:00Z","Objects":[{"Type":"astrald.log.tag","Object":"net"},{"Type":"string32","Object":"link established"}]}}
{"Type":"astrald.log.entry","Object":{"Origin":"02bef8840eb35ef2ae3c83c07cb5779278904f99cb4103f71e37cc69931ae5e15f","Level":2,"Time":"2026-06-10T12:00:01Z","Objects":[{"Type":"astrald.log.tag","Object":"dir"},{"Type":"string32","Object":"resolved identity"}]}}
```

A drop notice inside the stream:

```json
{"Type":"astrald.log.entry","Object":{"Origin":"02bef8840eb35ef2ae3c83c07cb5779278904f99cb4103f71e37cc69931ae5e15f","Level":0,"Time":"2026-06-10T12:00:02Z","Objects":[{"Type":"string32","Object":"log.listen: dropped 42 entries"}]}}
```
