# nat

The `nat` protocol performs NAT traversal, letting two nodes behind separate NATs open a direct UDP path to each other by hole-punching. A caller starts a traversal with `nat.punch`, naming the peer's identity; the peer's node answers on `nat.node_punch`, and the two sides exchange `nat.punch_signal` control messages (offer, answer, ready, go, result) to punch simultaneously. A successful punch produces a `nat.hole` object pairing the active and passive `nat.endpoint` addresses, which the node keeps in a pool.

Holes in the pool are enumerated with `nat.list_holes`, which streams `nat.hole` objects and can be filtered to a single peer. A held hole is handed to a consumer with `nat.node_consume_hole`, a two-phase lock-then-take handshake carried by `nat.consume_hole_signal` messages. Participation in traversal is toggled node-wide with `nat.set_enabled`.
