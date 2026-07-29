# Text Encoding

* The `Text Encoding` is an encoding that is used by the `Astral
  Network`.
* The `Text Encoding` encodes its payload using Base64 with the standard
  alphabet (`A`–`Z`, `a`–`z`, `0`–`9`, `+`, `/`) and `=` padding to a
  multiple of four characters.
* The URL-safe alphabet (`-` and `_` in place of `+` and `/`) and the
  unpadded form are never used. Either produces output the receiver
  misreads or rejects. The variant is part of the wire contract.
* The `Text Encoding` can have a type-specific encoding of the payload,
  which must be specified in the documentation of the [`Object Type`](../core-definitions/object-type.md).
* The `Text Encoding` can be used to encode objects as
  [`Query`](../core-definitions/query-string.md) parameters.
* The `Text Encoding` is done by concatenating the following:
    * A string with the format "#[{OBJECT_TYPE}]", for example "#[uint32]".
    * A single character indicating the encoding type. A sender writes `:` for
      Base64 or a space for the type-specific encoding. A receiver accepts two
      spellings of each: `:` or `=` for Base64, a space or a TAB for the
      type-specific encoding. Any other byte in this position is a decode
      error.
    * The encoded payload.
* The `Text Encoding` of an `Untyped Object` is "#[]:" followed by the
  Base64-encoded `Payload`.
* A `Typed Object` with no payload is encoded as `#[{OBJECT_TYPE}]`.


