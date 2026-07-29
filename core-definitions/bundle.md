# Bundle

* A `Bundle` is an ordered collection of unique [`Objects`](object.md) of various types.
* A `Bundle` is itself an [`Object`](object.md); its [`Object Type`](object-type.md) is `bundle`.
* An `Object` appears at most once in a `Bundle`.
* A `Bundle` preserves the order in which `Objects` were added.
* `Bundles` are used wherever a single `Object` must carry a set of others — for
  example, the constraints of a [`Permit`](permit.md).

## Binary Encoding

* A `Bundle`'s `Payload` is a [`uint32`](../primitive-types/uint32.md) count of
  members, followed by that many member blocks.
* Each member block is a [`bytes32`](../primitive-types/bytes32.md) whose
  contents are the member's `Short`-encoded form: its
  [`Object Type`](object-type.md) as a
  [`string8`](../primitive-types/string8.md), then the member's `Payload` (see
  [Codec](../topics/codec.md)).
* The length prefix covers the type tag **and** the payload together. The
  inline `Short` form used for a polymorphic field differs: there the type tag
  precedes the payload, and neither carries a length prefix. A member block is
  not interchangeable with an inline object. Reading one as the other misframes
  every member that follows.
* A `Bundle` is not encoded as a [`Slice`](../topics/binary-encoding.md#slices)
  and not as a [polymorphic
  field](../topics/binary-encoding.md#polymorphic-fields), though it resembles
  both. It shares the `uint32` count with a `Slice` but carries **no presence
  byte** before a member, and it shares the `string8` type tag with a
  polymorphic field but wraps it in a length prefix. Neither general rule
  produces a readable `Bundle`.

```
Bundle of one uint32 = 42               → 19 bytes

   00 00 00 01                count = 1 (uint32)
   00 00 00 0b                member block length = 11 (bytes32)
   06 75 69 6e 74 33 32       Object Type "uint32" (string8)
   00 00 00 2a                Payload (uint32 = 42)
```

* Members are unique by [`Object ID`](object-id.md). Two structurally identical
  `Objects` have the same `Object ID` and cannot both appear.
* A decoder must reject a `Bundle` in which an `Object ID` repeats. Such a frame
  is malformed, not merely redundant, and rejection occurs part-way through it —
  at the member that repeats. Uniqueness therefore binds the writer: it is part
  of the wire contract, not a property of the building interface.
