# ether

The `ether` protocol carries public, connectionless messages across a local network. A node sends a small typed object to every node on its IPv4 subnets, and each receiving node hands the object to its own modules. [`nearby`](../nearby/README.md) uses ether for node presence and discovery.

Messages travel over UDP. The node binds one IPv4 UDP socket on the ether port, `udp_port` in `ether.yaml`, `8822` by default. A datagram holds exactly one [`mod.ether.envelope`](types/mod.ether.envelope.md): a version byte, `1`, and the object being sent. The envelope carries no source identity, no timestamp and no signature. A datagram is at most 1024 bytes, about twice the largest nearby status (about 510 bytes with a 255-byte alias) and below the 1472-byte UDP payload of an Ethernet frame. The node sends every datagram with IP TTL 255.

The node sends a message to the broadcast address of every local IPv4 subnet, or to the broadcast address of the one local subnet that contains a given IP. A broadcast to every subnet skips loopback interfaces and link-local addresses, and sends once to a broadcast address that several interfaces share. ether has no unicast send.

The node drops a received datagram when any of these holds:

* The datagram is larger than 1024 bytes.
* The source address is not IPv4.
* The datagram arrived with an IP TTL other than 255. A Windows node cannot read the TTL and skips this check; it still sends with TTL 255.
* The source IP is one of the node's own addresses.
* The source IP lies outside every local IPv4 subnet.
* The first byte is not `1`, the bytes do not decode as a `mod.ether.envelope`, or bytes follow the envelope.

A panic while the node handles a datagram drops that datagram. The node delivers the object of an accepted datagram only inside a [`mod.ether.events.broadcast_received`](types/mod.ether.events.broadcast_received.md), with the source IP, to its own object receivers, as the node itself. It never delivers the object as sent by a remote identity. ether authenticates nothing beyond the TTL and source address checks. A protocol that needs to know the sender carries its own proof, as `nearby` does with [`mod.nearby.status_proof`](../nearby/types/mod.nearby.status_proof.md).
