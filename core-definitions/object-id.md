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
* A `Partial Object ID` is an `Object ID` whose `Object Size` is 0, except the
  `Object ID` of the `Empty Object`.
* An `Object Size` of 0 in an `Object ID` given to a lookup means the size is
  absent, except in the `Object ID` of the `Empty Object`.
* A repository lookup matches a `Partial Object ID` by its `Object Hash` alone.
* The `Object ID` of the `Empty Object` has the `Object Size` 0 and the
  `Object Hash` that is the SHA256 hash of empty input. It is a full
  `Object ID`, not a `Partial Object ID`.
* Every repository answers the `Object ID` of the `Empty Object` without
  storing the object: the repository contains it, reads it as 0 bytes in the
  device zone, and deletes it with no effect
  ([`objects`](../protocols/objects/README.md)).
* Every other `Object ID` with the `Object Size` 0 stays a
  `Partial Object ID`.
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
* The decoding rules of both text forms are in
  [`object_id.sha256`](../primitive-types/object_id.sha256.md).
