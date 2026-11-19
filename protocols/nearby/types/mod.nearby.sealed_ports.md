# mod.nearby.sealed_ports

The [`mod.nearby.listen_ports`](mod.nearby.listen_ports.md) of a node in mode `2` (Stealth), readable only by a node that knows the node identity. The node attaches one after its [`mod.nearby.stealth_hint`](mod.nearby.stealth_hint.md) when either port differs from its default.

## Fields

* Data (bytes8) – The 4-byte payload of a `mod.nearby.listen_ports`, sealed.

```
K    = SHA-256("astral/nearby/ports-key/v1" ‖ H(N) ‖ Nonce)
Data = P ⊕ ChaCha20(K)
```

* `N` is the node identity, as the 33 bytes of its compressed secp256k1 public key ([identity](../../../primitive-types/identity.md)), and `H(N)` is the SHA-256 hash of those 33 bytes.
* `Nonce` is the `Nonce` of the status's `mod.nearby.stealth_hint`, as its 8-byte big-endian binary form ([nonce64](../../../primitive-types/nonce64.md)).
* `P` is the payload of the `mod.nearby.listen_ports`: `TCP` and `KCP`, each a big-endian `uint16`.
* `ChaCha20(K)` is the ChaCha20 keystream (RFC 8439) under the key `K`, with a 12-byte all-zero nonce and block counter `0`, 4 bytes long. `⊕` is bytewise XOR.
* The label is its ASCII bytes, with no terminator, and `‖` is concatenation.

A receiver opens `Data` with the same function, after it identified `N` from the hint and the [`mod.nearby.status_proof`](mod.nearby.status_proof.md) verified under `N`. A `Data` that is not 4 bytes opens to no ports.

* Each hint has its own `Nonce`, so each status seals its ports under its own key.
* The label differs from the `mod.nearby.status_proof` wrap label, so the ports and the wrapped signature never share a keystream.
* A node that cannot identify `N` learns neither the node nor its ports. The status proof signs `Data`, so a changed `Data` fails the proof.

## Example

The ports `TCP` `1800` and `KCP` `1801` of node `035d6bfc7818844824354bd5ba1b7c08510139de14aa574e3f53a490814e3eab0e`, sealed under the `Nonce` `7c1a93b50f2e4d18` of its hint ([`mod.nearby.stealth_hint`](mod.nearby.stealth_hint.md#example)):

* `P` is `07080709`.
* `K` is `682aa798f8a7281e9040fde0e5b7bda8f695c7ae613abbede7ccec152bf1cf8d`.
* `Data` is `7773db1b`.

```json
{
  "Type": "mod.nearby.sealed_ports",
  "Object": {
    "Data": "d3PbGw=="
  }
}
```
