# mod.nearby.status_proof

Proves that a status was made with the key of the node it names, at a stated time, and was not changed. nearby appends one as the last attachment of every status it sends. A composer never attaches one.

## Fields

* Nonce (nonce64) – A fresh random value for each status.
* Timestamp (time) – The sender's clock when it made the status.
* Sig (bytes8) – The node key's signature over `H`, 8 to 72 bytes. Wrapped in mode `2` (Stealth).

`Sig` is a DER-encoded ECDSA secp256k1 signature, the `asn1` scheme of [`mod.crypto.signature`](../../crypto/types/mod.crypto.signature.md), over the 32-byte hash `H`:

```
H = SHA-256("astral/nearby/status/v1" ‖ B ‖ Nonce ‖ Timestamp)
```

* `B` is the binary `Payload` of a [`Bundle`](../../../core-definitions/bundle.md) that holds every other attachment of the status, in status order: a `uint32` count, then each attachment as a `bytes32` block of its `Object Type` (`string8`) and its `Payload`.
* `Nonce` is its 8-byte big-endian binary form ([nonce64](../../../primitive-types/nonce64.md)).
* `Timestamp` is its 8-byte binary form ([time](../../../primitive-types/time.md)).
* The label is its ASCII bytes, with no terminator, and `‖` is concatenation.

In mode `2` (Stealth) the sender wraps the signature. A receiver unwraps it with the same function:

```
K       = SHA-256("astral/nearby/proof-key/v1" ‖ H(N) ‖ Nonce)
wrapped = Sig ⊕ ChaCha20(K)
```

* `H(N)` is the SHA-256 hash of the 33 bytes of the node identity `N`, and `Nonce` is this proof's `Nonce`.
* `ChaCha20(K)` is the ChaCha20 keystream (RFC 8439) under the key `K`, with a 12-byte all-zero nonce and block counter `0`, as long as `Sig`. `⊕` is bytewise XOR.
* A plain ECDSA signature over a hash anyone can compute reveals the signer's public key. Only a node that knows `N` unwraps the signature.

A receiver caches the sender as identified, and acts on the status, only when all of these hold:

* The proof is the last attachment, and no other attachment is a `mod.nearby.status_proof`.
* `Sig` is 8 to 72 bytes.
* `Timestamp` is at most 5 minutes before or after the receiver's clock.
* The receiver did not see `Nonce` from the same node in the last 5 minutes.
* `Sig`, unwrapped in Stealth, verifies against the key of the identified node.

A receiver checks the first three before it identifies the sender, and drops a status that fails one of them. A Stealth status that no recognizer matches is cached with its source IP only, as an unrecognised node, without the nonce and signature checks ([nearby](../README.md)).

## Example

The proof of a Visible status whose other attachments are a `mod.nearby.flag` reading `adoptable` and a `mod.nearby.public_profile` of node `035d6bfc7818844824354bd5ba1b7c08510139de14aa574e3f53a490814e3eab0e` with no user and the alias `living-room`:

```json
{
  "Type": "mod.nearby.status_proof",
  "Object": {
    "Nonce": "3f9c2a7d11e4b605",
    "Timestamp": "2026-11-05T17:00:00Z",
    "Sig": "MEUCIQDrGjfIXhaxCzTaW42UztGuFdKoPVPe0LDlT+EUc9reXAIgAZ8y4LXgMO4WMYAwLOQ0ZtOk6To/hBflNDXtE8Zpfr0="
  }
}
```
