# Codec

* The `Codec` writes and reads [`Objects`](../core-definitions/object.md) as a type tag followed by the
  `Payload`. The tag is produced by a `Type Encoder` chosen by the caller;
  the `Payload` follows the [Binary Encoding](binary-encoding.md) rules.
* The decoder resolves the [`Object Type`](../core-definitions/object-type.md) to a zero `Object` through a
  [Blueprints](blueprints.md) registry and calls `ReadFrom` on it.
* The `Codec` described here is the binary framing layer. `JSON` and
  `Text` encodings define their own framing — see
  [JSON Encoding](json-encoding.md) and [Text Encoding](text-encoding.md).

## Type Encoders

| Encoder     | Tag bytes                                                          | Notes                                                                                   |
|-------------|--------------------------------------------------------------------|-----------------------------------------------------------------------------------------|
| `Short`     | `Object Type` ([`string8`](../primitive-types/string8.md))            | The default. Used by framed channels and nested polymorphic fields.                     |
| `Canonical` | `Stamp \|\| Object Type (string8)`                                 | Used for `Object ID` hashing and out-of-band transport.                                 |
| `Indexed`   | [`uint8`](../primitive-types/uint8.md) index                          | Used by protocols with a closed type table known to both parties.                       |

* An empty `Object Type` is rejected. `Short` and `Canonical` reject it
  unconditionally. `Indexed` rejects it unless the empty name is itself an
  entry in the closed table, in which case it encodes as that entry's index.
* The zero-length type tag that denotes nil in a [polymorphic
  field](binary-encoding.md#polymorphic-fields) is not an exception. That tag is
  written by the container encoding, which emits it and returns before any
  `Type Encoder` runs. A non-nil value whose `Object Type` is empty is rejected
  there as well.

## Canonical Form

* The `Canonical Form` of a `Typed Object` is the byte sequence used to
  compute its [`Object ID`](../core-definitions/object-id.md) and to
  express it outside any framing.
* It is the `Canonical Type Encoder`'s output: [`Stamp`](../core-definitions/stamp.md) followed by the
  `Object Type` as a `string8` followed by the `Payload`.

```
   41 44 43 30                Stamp (0x41444330)
   06 75 69 6e 74 33 32       Object Type "uint32" (string8)
   00 00 00 2a                Payload (uint32 = 42)
```

## Decoding limits

* Decoding is driven entirely by the sender: the nesting depth, the frame count
  and the byte count of a payload are all chosen by whoever wrote it. A decoder
  may therefore bound the resources a single decode consumes, and refuse a
  payload that exceeds them.
* A refusal on resource grounds is reported distinguishably from a malformed
  payload. The bytes are well formed; what failed is the receiver's policy, and
  the same bytes may be accepted by a peer that budgets differently.
* **Nesting.** An implementation must accept at least **16** levels of nesting
  in a single decode. A level is any frame that carries another `Typed Object`
  inside it: a [polymorphic field](binary-encoding.md#polymorphic-fields), a
  [`Bundle`](../core-definitions/bundle.md) member, or a `Structured` field
  whose value is itself a `Typed Object`. A sender that stays within 16 levels
  is portable. Past 16, acceptance is the receiver's policy and must not be
  assumed. (The reference decoder admits 32; the deepest type in the reference
  registry nests 5.)
* **Total work.** A decoder may additionally bound the total frames and the
  total bytes one decode consumes. Neither follows from the nesting bound — a
  [`Slice`](binary-encoding.md#slices) of a million shallow elements is one
  level deep. No figure is given for either: that ceiling belongs to the
  receiver's memory, not to the wire format.
* These bounds are on what a decode *consumes*, not on what a payload may
  *declare*. The width-derived payload caps in [Binary
  Encoding](binary-encoding.md#primitives) are unchanged — a `bytes64` may
  declare a length no implementation will ever buffer, and a decoder refuses it
  for want of resources rather than because the frame is malformed.
* An implementation that bounds decoding applies the same bound when encoding.
  A writer whose limit is looser than its own reader's produces objects it
  cannot read back, and puts them on the wire for peers that will reject them.
