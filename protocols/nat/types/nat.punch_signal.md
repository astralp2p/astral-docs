# nat.punch_signal

A control message exchanged over the signalling channel while two peers coordinate a hole-punch. The `signal` field selects one of five handshake steps, sent in order: `offer` (the initiator advertises its endpoint and opens a session), `answer` (the passive peer advertises its endpoint), `ready` (the passive peer is listening), `go` (both peers punch simultaneously), and `result` (the observed endpoint and hole nonce are confirmed).

## Fields

* signal (string8) – The handshake step: one of `offer`, `answer`, `ready`, `go`, `result`.
* session (bytes8) – Session token that binds the exchange; established by the `offer` and echoed by every later signal.
* ip (bytes8) – In `offer` and `answer`, the sender's advertised IP address. In `result`, the IP address the sender observed for the receiver. IPv4 is stored as 4 bytes, IPv6 as 16 bytes.
* port (uint16) – In `offer` and `answer`, the sender's advertised UDP port: the port the peer sends probes to. In `result`, the UDP port the sender observed for the receiver.
* bind_port (uint16) – The local UDP port of the sender's punch socket; carried by `offer`, `answer` and `result`. Behind a NAT that translates ports, `bind_port` differs from the port the peer observes.
* pair_nonce (nonce64) – The nonce assigned to the resulting hole; carried by the `result` signal.

In `offer` and `answer`, `ip` and `port` are the endpoint a reflecting node observed for the sender's punch socket ([`nat.reflect_udp`](../ops/nat.reflect_udp.md)). A sender without a reflection advertises its public IPv4 address and the socket's local port, so `port` equals `bind_port`.

## Example

```json
{
  "Type": "nat.punch_signal",
  "Object": {
    "signal": "offer",
    "session": "8fA1b2c3d4e5f6A=",
    "ip": "198.51.100.7",
    "port": 6635,
    "bind_port": 41000,
    "pair_nonce": "0"
  }
}
```
