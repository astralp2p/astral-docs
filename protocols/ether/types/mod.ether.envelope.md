# mod.ether.envelope

The content of one ether datagram: the envelope format version and the object being sent.

## Fields

* Version (uint8) – The envelope format. The current value is `1`.
* Object (object) – The object being sent; any astral object type, written as its `Object Type` (`string8`) followed by its `Payload`.

A datagram is exactly the envelope's `Payload`: the `Version` byte, then `Object`. No type tag precedes it. A receiver drops a datagram whose first byte is not `1`, and a datagram with bytes after `Object`. A datagram in the earlier `mod.ether.signed_broadcast` format starts with the high byte of a nanosecond timestamp, `0x17` to `0x1c` for the years 2023 to 2034, so a receiver drops it.

A receiver decodes `Object` as part of the envelope: the bounds of the envelope's decode apply to it ([Codec, Decoding limits](../../../topics/codec.md#decoding-limits)).

The envelope carries no source identity, no timestamp and no signature.

## Example

A scan from [`nearby`](../../nearby/README.md):

```json
{
  "Type": "mod.ether.envelope",
  "Object": {
    "Version": 1,
    "Object": {
      "Type": "mod.nearby.scan_message",
      "Object": {}
    }
  }
}
```

The same envelope as a datagram, 25 bytes:

```
   01                         Version = 1
   17 6d 6f 64 2e 6e 65 61    Object Type "mod.nearby.scan_message" (string8)
   72 62 79 2e 73 63 61 6e
   5f 6d 65 73 73 61 67 65
                              Payload of mod.nearby.scan_message: no bytes
```
