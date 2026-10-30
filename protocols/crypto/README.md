# crypto

The `crypto` protocol provides cryptographic operations for signing and verifying hashes and text messages, and for deriving public keys from private keys.

The signer key defaults to the caller's identity. Signing under any other key
requires [`mod.auth.sudo_action`](../auth/types/mod.auth.sudo_action.md) for the
identity that key belongs to: an [`Identity`](../../core-definitions/identity.md)
is a public key, so signing under another party's key is that party acting. The
node's own key is refused to a caller that arrives as the node; a caller holding
`mod.auth.sudo_action` for the node signs under it.

## Signers

An [`App`](../../core-definitions/app.md) signs for a key the node does not hold
by holding a [`crypto.register_signer`](ops/crypto.register_signer.md) binding,
which names that key and a scheme. Every other key stays out of the app's reach.

Signing resolves in this order:

1. A local private key.
2. A binding that claims the key and scheme.

A key with neither has no signer, and signing under it fails. The signing
operations and internal signing do not differ for a key on a binding.

* [`crypto.register_signer`](ops/crypto.register_signer.md) – bind an app as the signer of a fixed set of keys
* [`mod.crypto.signer_key`](types/mod.crypto.signer_key.md) – one claimed key and scheme
* [`mod.crypto.signer_keys`](types/mod.crypto.signer_keys.md) – the fixed key set of a binding
* [`mod.crypto.sign_text_request`](types/mod.crypto.sign_text_request.md) – node to app: sign one text
* [`mod.crypto.sign_hash_request`](types/mod.crypto.sign_hash_request.md) – node to app: sign one hash
* [`mod.crypto.sign_answer`](types/mod.crypto.sign_answer.md) – app to node: the signature, or why there is none
* [`mod.crypto.sign_cancel`](types/mod.crypto.sign_cancel.md) – node to app: the node no longer waits
