# mod.nearby.listen_ports

The `tcp` and `kcp` ports a node listens on, which a receiver dials at the status's source IP. A node in mode `1` (Visible) attaches one after its `mod.nearby.public_profile` when either port differs from its default. A node in mode `2` (Stealth) attaches the same ports sealed, as a [`mod.nearby.sealed_ports`](mod.nearby.sealed_ports.md).

## Fields

* TCP (uint16) – The `tcp` listen port, `listen_port` in `tcp.yaml`. `0` when the node has no `tcp` transport.
* KCP (uint16) – The `kcp` listen port, `listen_port` in `kcp.yaml`. `0` when the node has no `kcp` transport.

The payload is 4 bytes: `TCP`, then `KCP`, each a big-endian [uint16](../../../primitive-types/uint16.md).

The object carries ports only, never an address. A receiver dials `tcp` and `kcp` at the source IP of the datagram that carried the status ([nearby](../README.md)). A port of `0` gives the receiver no endpoint for that transport. A status without a port object stands for `TCP` `1791` and `KCP` `1792`, the defaults, and a node on both defaults attaches none.

The [`mod.nearby.status_proof`](mod.nearby.status_proof.md) signs every other attachment, so a changed port fails the proof.

## Example

A node listening on `tcp` port `1800` and `kcp` port `1801`:

```json
{
  "Type": "mod.nearby.listen_ports",
  "Object": {
    "TCP": 1800,
    "KCP": 1801
  }
}
```
