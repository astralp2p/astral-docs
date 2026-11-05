# mod.nearby.stealth_hint

Identifies a Stealth node to the nodes that already know its node identity or its user identity, and to no other node. A node in mode `2` (Stealth) attaches one to its status.

## Fields

* Nonce (nonce64) – A fresh random value for each hint.
* Commitment (bytes8) – 32 bytes that let a node holding the user identity recognise the hint.
* MaskedNode (bytes8) – The node identity, 33 bytes, masked with a key derived from the user identity.
* MaskedUser (bytes8) – The user identity, 33 bytes, masked with a key derived from the node identity.

`N` and `U` are the node and user identities, each as the 33 bytes of its compressed secp256k1 public key ([identity](../../../primitive-types/identity.md)). `H(X)` is the SHA-256 hash of the 33 bytes of `X`. `Nonce` enters each hash as its 8-byte big-endian binary form ([nonce64](../../../primitive-types/nonce64.md)). Each label is its ASCII bytes, with no terminator. `‖` is concatenation, `⊕` is bytewise XOR, and `[0:33]` takes the first 33 bytes.

```
Commitment = SHA-256("astral/nearby/stealth/commit/v1"    ‖ H(U) ‖ Nonce)
MaskedNode = N ⊕ SHA-512("astral/nearby/stealth/mask-node/v1" ‖ H(U) ‖ Nonce)[0:33]
MaskedUser = U ⊕ SHA-512("astral/nearby/stealth/mask-user/v1" ‖ H(N) ‖ Nonce)[0:33]
```

* A node holding `U` opens a hint in four steps: it compares `Commitment` in constant time, unmasks `N` from `MaskedNode`, parses `N` as a public key, and checks that `MaskedUser` unmasks to `U`.
* A node holding `N` opens a hint in four steps: it unmasks `U` from `MaskedUser`, parses `U` as a public key, checks `Commitment` with `H(U)`, and checks that `MaskedNode` unmasks to `N`.
* A hint whose `Commitment` is not 32 bytes, or whose `MaskedNode` or `MaskedUser` is not 33 bytes, opens for no node.
* Each hint has its own `Nonce`, so every field changes from one hint to the next.
* SHA-512 truncated to 33 bytes masks every byte of an identity; SHA-256 yields 32 bytes and would leave the 33rd unmasked.
* Each hash has its own label, so `Commitment` reveals nothing of the mask on `N`.

## Example

A hint of node `035d6bfc7818844824354bd5ba1b7c08510139de14aa574e3f53a490814e3eab0e`, owned by user `02e8a0f652652cc090714d8fb3b26cddb33458106dd8a1edf6a9d870a9007fee55`:

```json
{
  "Type": "mod.nearby.stealth_hint",
  "Object": {
    "Nonce": "7c1a93b50f2e4d18",
    "Commitment": "gAeSwNjMYTM+6Nn7xm75ein0fmJT3K/uE5OLhsBfIN8=",
    "MaskedNode": "pjGXptNxdyi27zXgmvBRinrU2AjvNEVQpE045nAior2E",
    "MaskedUser": "wjIIDUOLppz73JVjL1FgdgUfufed+MkvngoQ859SJOEv"
  }
}
```
