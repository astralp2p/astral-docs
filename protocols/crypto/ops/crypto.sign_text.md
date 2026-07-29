# crypto.sign_text

Sign a text message with a private key held by the node. The signer key defaults to the caller's identity; pass `key` (or send a `mod.crypto.public_key` on the stream) to select a different public key whose corresponding private key the node owns.

## Arguments

* text (string) – The text to sign. If set, the text is signed immediately and the result returned.
* key (string) – Text-encoded `mod.crypto.public_key` selecting the signing key. Defaults to the caller's identity.
* scheme (string) – Signature scheme. Defaults to `bip137`.
* in (string) – Optional input stream format (e.g. `json`).
* out (string) – Optional output stream format (e.g. `json`).
* (stream) – Optionally, a `mod.crypto.public_key` to set/replace the signer key (server responds with `ack`), followed by a `string8` or `string16` containing the text to sign.

## Returned objects

An input of an unexpected type is answered with an `error_message` and the exchange continues. An explicit `eos` input is answered with a final `eos`; a stream ended by EOF is not. The operation returns one of:
* An `error_message` object if the key cannot be decoded, no signer is available for the scheme, or signing fails.
* An `ack` object acknowledging each `mod.crypto.public_key` sent on the stream.
* A `mod.crypto.signature` object for each text signed.
* An `eos` object answering an explicit `eos` input.

## Examples

```shellsession
$ astral-query crypto.sign_text -text "hello world" -out json
{"Type":"mod.crypto.signature","Object":"bip137:H3p1c1AY2W2NwO/lXh3uM9ETFt2Wp6dQjVA0kZl0ZTd5KQv0pZL5kE2c8R5Mz0qY1g6kPq3rTfM4l3a4eO1Q="}
```

```shellsession
$ echo '{"Type":"string8","Object":"hello world"}' | astral-query crypto.sign_text -scheme bip137 -in json -out json
{"Type":"mod.crypto.signature","Object":"bip137:H3p1c1AY2W2NwO/lXh3uM9ETFt2Wp6dQjVA0kZl0ZTd5KQv0pZL5kE2c8R5Mz0qY1g6kPq3rTfM4l3a4eO1Q="}
```
