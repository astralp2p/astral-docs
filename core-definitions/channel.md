# Channel

* A `Channel` is used to exchange [`Objects`](object.md) between two parties.
* A `Channel` can be closed by either party at any time.
* A `Channel` uses the [`Binary Encoding`](../topics/binary-encoding.md) by default.
* A `Channel` can use any encoding as long as both parties support it. For
  example, an [`Operation`](op.md) can take `Operation Parameters` to specify the
  encoding.

## Format tokens

An [`Operation`](op.md) selects the encoding with the `in` and `out`
`Operation Parameters`. Tokens are case-sensitive. An absent value means `bin`.

| Token       | Direction  | Framing per object                                                     |
|-------------|------------|------------------------------------------------------------------------|
| `bin`       | in, out    | `String8(ObjectType) ++ Bytes32(Payload)` — the default                 |
| `json`      | in, out    | one JSON envelope per newline-terminated line                           |
| `text`      | in, out    | one text-encoded object per newline-terminated line                     |
| `canonical` | in, out    | a bare sequence of `Canonical Forms`, no per-object framing             |
| `base64`    | **out** only | `#[type]:<base64 payload>` per line, never the type-specific text form |
| `render`    | **out** only | human-readable text, no type tag; not decodable                       |

* The two directions accept **different sets**. `base64` and `render` are
  output-only; supplying either to `in` fails exactly as an unrecognised token
  does.
* An unrecognised token is not refused. The channel produces zero bytes and
  reports no error, so an empty result — not a diagnostic — is the symptom of a
  mistyped token.

### Canonical framing

* A `canonical` channel is a bare concatenation of `Canonical Forms` (see
  [Codec](../topics/codec.md)) with **no per-object length prefix**.
* A reader cannot locate the next object without fully decoding the current one
  against its schema, and cannot resynchronize after a decode error: once a
  [`Stamp`](stamp.md) has been consumed the stream position is indeterminate, so the first
  failed read ends the channel.

## Binary Encoding

Objects are sent over the channel by writing their type encoded as [`string8`](../primitive-types/string8.md) 
followed by their payload encoded as `bytes32`. An empty type means a binary
untyped blob.

```
String8(ObjectType) ++ Bytes32(Payload)`
```

## JSON Encoding

A JSON channel carries one JSON envelope per newline-terminated line. See the
[`JSON Encoding`](../topics/json-encoding.md).

## Text Encoding

A text channel carries one text-encoded object per newline-terminated line. See
the [`Text Encoding`](../topics/text-encoding.md).
