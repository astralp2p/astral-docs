# mod.ether.signed_broadcast

A `mod.ether.broadcast` body paired with a signature over it. `mod.ether.signed_broadcast` is the form actually sent on the broadcast network; receivers reject any datagram whose signature is absent or does not verify.

## Fields

* Broadcast (`mod.ether.broadcast`) – The embedded broadcast body: the timestamp, source identity, and announced object.
* Signature (`mod.crypto.signature`) – Signature produced with the key of the sending node, which is always the body's `Source`. The signed input is the 32-byte `Object Hash` of the embedded broadcast body: the SHA256 hash of its [`Canonical Form`](../../../topics/codec.md#canonical-form), without the `Object Size` that an [`Object ID`](../../../core-definitions/object-id.md) prepends. It covers the body only, not the signature field itself.

In JSON the embedded body's fields appear directly in the `Object` value, beside `Signature`, not under a `Broadcast` key.

## Example

```json
{
  "Type": "mod.ether.signed_broadcast",
  "Object": {
    "Timestamp": "2026-06-19T10:00:00Z",
    "Source": "02bef8840eb35ef2ae3c83c07cb5779278904f99cb4103f71e37cc69931ae5e15f",
    "Object": {
      "Type": "mod.nearby.status",
      "Object": {
        "Identity": "02bef8840eb35ef2ae3c83c07cb5779278904f99cb4103f71e37cc69931ae5e15f",
        "Attachments": {}
      }
    },
    "Signature": {
      "Scheme": "asn1",
      "Data": "MEUCIQDg+5p9aT4q2QzVKbS9N5wXYrFh3vUaQ7E2lY0bX9lSAgIgex8="
    }
  }
}
```
