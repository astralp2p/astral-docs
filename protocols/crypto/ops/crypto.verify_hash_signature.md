# crypto.verify_hash_signature

Verify a signature over a hash. The public key defaults to the caller's identity; pass `key` (or send a `mod.crypto.public_key` on the stream) to verify against a different key.

## Arguments

* hash (string) – Hex-encoded hash that was signed.
* key (string) – Text-encoded `mod.crypto.public_key` to verify against. Defaults to the caller's identity.
* in (string) – Optional input stream format (e.g. `json`).
* out (string) – Optional output stream format (e.g. `json`).
* (stream) – Optionally a `mod.crypto.public_key` and/or a `mod.crypto.hash` (each acknowledged with `ack`), followed by a `mod.crypto.signature` that triggers verification.

## Returned objects

An input of an unexpected type is answered with an `error_message` and the exchange continues. An explicit `eos` input is answered with a final `eos`; a stream ended by EOF is not. The operation returns one of:
* An `error_message` object if the hash or key cannot be decoded, if either is missing when the signature arrives, or if verification fails.
* An `ack` object acknowledging each `mod.crypto.public_key` or `mod.crypto.hash` sent on the stream, and a final `ack` confirming a successful verification.
* An `eos` object answering an explicit `eos` input.

## Examples

```shellsession
$ echo '{"Type":"mod.crypto.signature","Object":"asn1:MEUCIQDg+5...AiB7H1k="}' | astral-query crypto.verify_hash_signature -hash 9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08 -key secp256k1:02bef8840eb35ef2ae3c83c07cb5779278904f99cb4103f71e37cc69931ae5e15f -in json -out json
{"Type":"ack","Object":null}
```
