# object_id.sha256

An object ID consisting of a `Size` (uint64) and a `Hash` (SHA-256, 32 bytes).

* For a `Typed Object` the `Size` and `Hash` cover the object's `Canonical Form` — the [`Stamp`](../core-definitions/stamp.md), then the object type as a [`string8`](string8.md), then the payload (see [Codec](../topics/codec.md)).
* For an `Untyped Object` the `Size` and `Hash` cover the raw payload.
* The `Size` is the length in bytes of that byte sequence.
* The `Hash` is the SHA-256 hash of that byte sequence.
* A `Size` of 0 in an object ID given to a lookup means the size is absent, in every encoding, the binary one included.
* A repository lookup matches an object ID whose `Size` is 0 by `Hash` alone. Such an object ID is a [`Partial Object ID`](../core-definitions/object-id.md).
* A repository lookup given a nonzero `Size` matches only an object with that `Size` and that `Hash`.

## Binary Encoding

40 bytes: the `Size` as a big-endian uint64 (8 bytes) followed by the 32-byte SHA-256 hash.

A `Partial Object ID` is 8 zero bytes followed by the 32-byte SHA-256 hash.

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

An encoder always emits the `data1` form, for a `Size` of 0 as well. A decoder
accepts the `data1` form and the `data0` form.

The `data0` form carries the `Hash` alone and decodes to a `Size` of 0. The
encoding has three steps:

* encode 8 zero bytes followed by the 32-byte hash with the zBase32 alphabet
  `ybndrfg8ejkmcpqxot1uwisza345h769`;
* remove the first 12 characters, which are always `y`, and no other
  character;
* prefix `data0`.

The body after the prefix is 52 characters. Its first character encodes the
last four `Size` bits, which are 0, and the first `Hash` bit, so it is `y` or
`b`.

A decoder accepts a `data0` body only when:

* it is exactly 52 characters;
* every character is one of the 32 characters of the zBase32 alphabet
  `ybndrfg8ejkmcpqxot1uwisza345h769`, so an uppercase letter is rejected;
* its first character is `y` or `b`;
* twelve `y` characters followed by the body decode to a `Size` of 0.

A decoder rejects every other `data0` body.

A body of 52 `y` characters meets all four conditions, so a decoder accepts it.
It decodes to the `Object ID` whose `Size` is 0 and whose `Hash` is 32 zero
bytes, the same value a `data1` body of zero characters decodes to.

That `Object ID` is the zero `Object ID`: no object hashes to 32 zero bytes.
Both text forms decode to it, so an operation treats them alike. An operation
that refuses a zero `Object ID` refuses it before it refuses a
`Partial Object ID`, so the zero `Object ID` is reported as a missing argument
rather than as a `Partial Object ID`.

The `Object ID` of the `Empty Object` has a `Size` of 0, so it is also a
`Partial Object ID`. The first bit of its `Hash` is 1, so its `data1` form and
its `data0` form carry the same 52-character body. An object ID with a `Size`
of 0 and a first `Hash` bit of 0 has a `data1` body shorter than 52 characters.

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
partial  data0ym81js7f9cfdbauqoq3kash6f8o5naxfa878ejx8gbbuckjazgbr
```

The binary form is the 8-byte `Size` followed by the 32-byte `Hash`. The text
form is 57 characters here, not 69: twelve leading `y` characters were stripped
before the `data1` prefix, per the three steps above.

The `partial` row is the `data0` form of the `Partial Object ID` with the same
`Hash`. The first `Hash` bit is 0, so its body starts with `y`, and the `y`
stays.

An encoder emits this `Partial Object ID` as
`data1m81js7f9cfdbauqoq3kash6f8o5naxfa878ejx8gbbuckjazgbr`, 56 characters:
thirteen leading `y` characters were stripped, and the last of them encoded the
last four `Size` bits and the first `Hash` bit.

An `Object ID` whose `Size` is 71:

```
binary   00 00 00 00 00 00 00 47
         b8 a5 cf b9 c8 0c 61 e5 03 61 ed 92 b2 c2 d8 73
         f0 76 da 69 af c2 f1 b4 13 49 16 ae 34 db 36 44
json     "data1rxqff36hhoddbhwbsd5c1smbpoh9oq5pgum6n6g4bg1esia4psp1r"
text     data1rxqff36hhoddbhwbsd5c1smbpoh9oq5pgum6n6g4bg1esia4psp1r
partial  data0bqff36hhoddbhwbsd5c1smbpoh9oq5pgum6n6g4bg1esia4psp1r
```

The text form is 58 characters here: eleven leading `y` characters were
stripped. The first `Hash` bit is 1, so the `partial` body starts with `b`.

In both examples the `partial` form ends in the same 51 characters as the text
form. Every `data0` body character after the first encodes `Hash` bits only.
