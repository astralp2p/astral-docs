# nat.reflect_udp

Report the source endpoint of one UDP datagram, so the caller learns the external endpoint its NAT maps a UDP socket to. A punch side calls this operation on a node it dialed at a public IPv4 address, sends the token from its punch socket, and advertises the reflected endpoint in its `offer` or `answer` (see [`nat.punch_signal`](../types/nat.punch_signal.md)).

The operation binds a fresh UDP socket on an IPv4 port the node chooses, and answers a [`nat.reflect_udp_offer`](../types/nat.reflect_udp_offer.md) carrying that port and a fresh 16-byte random token. It then reads the socket for at most 2 s. The first datagram whose payload equals the token ends the read, and the operation answers a [`nat.endpoint`](../types/nat.endpoint.md) holding that datagram's source IP address and port. An IPv4 source is carried as 4 bytes. Datagrams with any other payload are ignored. The socket is closed when the operation ends.

The operation never sends UDP. The observed endpoint travels only over the query channel, so a forged source address receives nothing.

The caller must hold
[`mod.auth.admin_network_action`](../../auth/types/mod.auth.admin_network_action.md).
The operation answers an `error_message` reading `not permitted` before any
socket is opened when the caller is not authorized. An authorized caller
receives an `error_message` reading `nat disabled`, and nothing else, when this
node does not traverse NAT.

## Arguments

This operation takes no arguments beyond the implicit output format hint.

* out (string8) – Output format.

## Returned objects

The operation returns, in order:
* A `nat.reflect_udp_offer` object naming the UDP port and the token.
* One of:
  * A `nat.endpoint` object holding the source of the first datagram carrying the token.
  * An `error_message` object reading `no reflected datagram` if no such datagram arrives within 2 s.

The operation returns only an `error_message` object, reading `not permitted` or `nat disabled`, when it refuses the caller.

## Examples

```shellsession
$ astral-query nat.reflect_udp -out json
{"Type":"nat.reflect_udp_offer","Object":{"Port":47001,"Token":"q83vEjRWeJCrze8SNFZ4kA=="}}
{"Type":"nat.endpoint","Object":{"IP":"212.105.131.237","Port":6635}}
```
