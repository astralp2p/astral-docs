# crypto.sign_hash

Sign a hash with a private key held by the node. The signer key defaults to the caller's identity; pass `key` (or send a `mod.crypto.public_key` on the stream) to select a different public key whose corresponding private key the node owns.

Signing under any key other than the caller's identity requires
[`mod.auth.sudo_action`](../../auth/types/mod.auth.sudo_action.md) for the
identity that key belongs to; without it the operation answers `cannot sign with
another identity's key`. The node's own key is never signable this way and
answers `cannot sign with the node's key`. The check runs on every frame,
because the channel loop rebinds the signer key mid-stream.

## Arguments

* hash (string) – Hex-encoded hash to sign. If set, the hash is signed immediately and the result returned.
* key (string) – Text-encoded `mod.crypto.public_key` (e.g. `secp256k1:02ab...`) selecting the signing key. Defaults to the caller's identity.
* scheme (string) – Signature scheme. Defaults to `asn1`.
* in (string) – Optional input stream format (e.g. `json`).
* out (string) – Optional output stream format (e.g. `json`).
* (stream) – Optionally, a `mod.crypto.public_key` to set/replace the signer key (server responds with `ack`), followed by a `mod.crypto.hash` to sign.

## Returned objects

An input of an unexpected type is answered with an `error_message` and the exchange continues. An explicit `eos` input is answered with a final `eos`; a stream ended by EOF is not. The operation returns one of:
* An `error_message` object if the key cannot be decoded, no signer is available for the scheme, or signing fails.
* An `ack` object acknowledging each `mod.crypto.public_key` sent on the stream.
* A `mod.crypto.signature` object for each hash signed.
* An `eos` object answering an explicit `eos` input.

## Examples

```shellsession
$ astral-query crypto.sign_hash -hash 9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08 -out json
{"Type":"mod.crypto.signature","Object":"asn1:MEUCIQDg+5...AiB7H1k="}
```

```shellsession
$ echo '{"Type":"mod.crypto.hash","Object":"9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08"}' | astral-query crypto.sign_hash -scheme asn1 -in json -out json
{"Type":"mod.crypto.signature","Object":"asn1:MEUCIQDg+5...AiB7H1k="}
```
