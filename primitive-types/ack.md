# ack

No payload, this object is used as a generic acknowledgement.

The documentation of the [Op](../core-definitions/op.md) that sends an `ack` sets
its meaning: completion by default, readiness where that documentation says so.
See [Op modes & composition § Control signals](../topics/op-modes.md#control-signals).

## Binary Encoding

No payload.

## JSON Encoding

No payload.

## Text Encoding

No payload.

## Example

An acknowledgement, in each encoding:

```
binary   (no payload)
json     null
text     (no payload)
```
