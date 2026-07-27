# log

The `log` protocol exposes the node's live log stream to remote callers. Each log entry is delivered as an `astrald.log.entry` object carrying an origin identity, severity level, timestamp, and an ordered list of typed message objects.

The single operation `log.listen` subscribes the caller to the stream. Entries are buffered per subscriber and forwarded as the subscriber drains them; entries are dropped under backpressure and drops are announced in-band. The stream runs until the caller disconnects or the node disconnects a stalled caller.
