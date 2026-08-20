# crypto

The `crypto` protocol provides cryptographic operations for signing and verifying hashes and text messages, and for deriving public keys from private keys.

The signer key defaults to the caller's identity. Signing under any other key
requires [`mod.auth.sudo_action`](../auth/types/mod.auth.sudo_action.md) for the
identity that key belongs to: an [`Identity`](../../core-definitions/identity.md)
is a public key, so signing under another party's key is that party acting. The
node's own key is never signable this way.
