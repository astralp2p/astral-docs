# Object ID

* The `Object ID` is a 320-bit value consisting of the `Object Size` (uint64) 
  followed by the `Object Hash` (SHA256).
* For a `Typed Object` the `Object Size` and `Object Hash` cover the object's
  `Canonical Form` — the [`Stamp`](stamp.md), then the object type as a
  [`string8`](../primitive-types/string8.md), then the payload (see
  [Codec](../topics/codec.md)).
* For an `Untyped Object` the `Object Size` and `Object Hash` cover the raw
  payload.
* The `Object Size` is the length in bytes of that byte sequence.
* The `Object Hash` is the SHA256 hash of that byte sequence.
* The `Object ID` is calculated by:
  * encoding the 320-bit value using zBase32 with character set 
    "ybndrfg8ejkmcpqxot1uwisza345h769"
  * removing the leading "y"s from the string
  * adding a "data1" prefix
* The `Object Hash` of an `Empty Object` is the SHA256 hash of an empty byte 
  buffer.
* A `Partial Object ID` is an `Object ID` whose `Object Size` is 0 and whose
  `Object Hash` is not the SHA256 hash of an empty byte buffer.
* An `Object Size` of 0 in a `Partial Object ID` given to a lookup means the
  size is absent.
* A repository lookup matches a `Partial Object ID` by its `Object Hash` alone.
* Every other `Object ID` is a full `Object ID`.
* The `Object ID` of an `Empty Object` has the `Object Size` 0 and the
  `Object Hash` that is the SHA256 hash of an empty byte buffer. It is a full
  `Object ID`, not a `Partial Object ID`.
* A repository stores an `Empty Object` as 0 bytes, like any other object.
* A `Partial Object ID` has the "data1" text form calculated above, and a
  second text form calculated by:
  * encoding the 320-bit value using zBase32 with character set
    "ybndrfg8ejkmcpqxot1uwisza345h769"
  * removing the first 12 characters, which are always "y", and no other
    character
  * adding a "data0" prefix
* After the "data0" prefix, the first character encodes the last four
  `Object Size` bits, which are 0, and the first `Object Hash` bit, and every
  later character encodes `Object Hash` bits only.
* The "data0" form ends in the same 51 characters as the "data1" text form of
  the `Object ID` of the object with that `Object Hash`.
* The "data0" form whose `Object Hash` is the SHA256 hash of an empty byte
  buffer decodes to the `Object ID` of an `Empty Object`, a full `Object ID`.
* The decoding rules of both text forms are in
  [`object_id.sha256`](../primitive-types/object_id.sha256.md).
