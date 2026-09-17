# mod.tor.digest

The onion-service identifier of a Tor node, from which its `.onion` hostname is derived.

## Fields

The type has no named struct fields. On the wire the digest is exactly 35 raw bytes with no length prefix. The text form is the digest encoded as lowercase base32 with the `.onion` suffix appended; JSON encodes the object as that same text.

A zero-value digest names no onion service. It is 35 null bytes on the wire, and its text form is `unknown` — the form [mod.tor.endpoint](mod.tor.endpoint.md) uses for the same absence. No onion service encodes to that text: a v3 address carries a checksum over its key, and no key checksums to zero.

## Example

```json
{
  "Type": "mod.tor.digest",
  "Object": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaad.onion"
}
```
