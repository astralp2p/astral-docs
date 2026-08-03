# object_id.sha256

An object ID consisting of a `Size` (uint64) and a `Hash` (SHA-256, 32 bytes).

* For a `Typed Object` the `Size` and `Hash` cover the object's `Canonical Form` — the [`Stamp`](../core-definitions/stamp.md), then the object type as a [`string8`](string8.md), then the payload (see [Codec](../topics/codec.md)).
* For an `Untyped Object` the `Size` and `Hash` cover the raw payload.
* The `Size` is the length in bytes of that byte sequence.
* The `Hash` is the SHA-256 hash of that byte sequence.

## Binary Encoding

40 bytes: the `Size` as a big-endian uint64 (8 bytes) followed by the 32-byte SHA-256 hash.

## JSON Encoding

A zBase32-encoded string of the binary representation, prefixed with `data1`.

The encoding has three steps, and all three are required — see
[Object ID](../core-definitions/object-id.md):

* encode the 40-byte binary representation with the zBase32 alphabet
  `ybndrfg8ejkmcpqxot1uwisza345h769`;
* remove every leading `y` from the result;
* prefix `data1`.

An encoding that omits the strip is 69 characters. It is well-formed, and it
compares unequal to the same `Object ID` encoded with the strip.

## Text Encoding

As the [JSON Encoding](../topics/json-encoding.md) above.

## Example

The `Object ID` of the untyped 5-byte payload `hello`:

```
binary   00 00 00 00 00 00 00 05
         2c f2 4d ba 5f b0 a3 0e 26 e8 3b 2a c5 b9 e2 9e
         1b 16 1e 5c 1f a7 42 5e 73 04 33 62 93 8b 98 24
json     "data1km81js7f9cfdbauqoq3kash6f8o5naxfa878ejx8gbbuckjazgbr"
text     data1km81js7f9cfdbauqoq3kash6f8o5naxfa878ejx8gbbuckjazgbr
```

The binary form is the 8-byte `Size` followed by the 32-byte `Hash`. The text
form is 57 characters here, not 69: twelve leading `y` characters were stripped
before the `data1` prefix, per the three steps above.
