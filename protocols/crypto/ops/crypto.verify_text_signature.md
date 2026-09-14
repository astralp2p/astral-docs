# crypto.verify_text_signature

Verify a signature over a text message. The public key defaults to the caller's identity; pass `key` (or send a `mod.crypto.public_key` on the stream) to verify against a different key.

## Arguments

* text (string) – The text that was signed.
* key (string) – Text-encoded `mod.crypto.public_key` to verify against. Defaults to the caller's identity.
* in (string) – Optional input stream format (e.g. `json`).
* out (string) – Optional output stream format (e.g. `json`).
* (stream) – Optionally a `mod.crypto.public_key`, a `string8`, or a `string16` (each acknowledged with `ack`), followed by a `mod.crypto.signature` that triggers verification.

## Returned objects

An input of an unexpected type is answered with an `error_message` and the exchange continues. An explicit `eos` input is answered with a final `eos`; a stream ended by EOF is not. The operation returns one of:
* An `error_message` object if the key cannot be decoded, if the public key or text is missing when the signature arrives, or if verification fails.
* An `ack` object acknowledging each `mod.crypto.public_key`, `string8`, or `string16` sent on the stream, and a final `ack` confirming a successful verification.
* An `eos` object answering an explicit `eos` input.

## Examples

```shellsession
$ echo '{"Type":"mod.crypto.signature","Object":{"Data":"H+d3VDEwVfpzQ6Onkq/rYV1Mz/ljt+T/DbMb3gg+iyBnOczabFybkOcypDKhDppsI8+y0jTBlItao84Qf29Rmr8=","Scheme":"bip137"}}' | astral-query crypto.verify_text_signature -text "hello world" -key secp256k1:03e55f6b3bbd37b75fcbd40291b93a9cc116903a94971b62889ab6e132b674319a -in json -out json
{"Type":"ack","Object":null}
```
