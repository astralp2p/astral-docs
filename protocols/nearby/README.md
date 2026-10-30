# nearby

The `nearby` protocol discovers and tracks nodes reachable on the local network. Nodes periodically broadcast a `mod.nearby.status_message` carrying a bundle of attached objects composed by registered `Composer` implementations; the module caches incoming broadcasts and expires them after five minutes.

Three broadcast modes are supported via `mod.nearby.mode`: `silent` sends no status, no scan reply and no scan, `visible` broadcasts the node's endpoints plus an `adoptable` flag and a `mod.nearby.public_profile` before the claim, or the active contract after it, and `stealth` broadcasts a `mod.nearby.stealth_hint` that masks the node–user association so only nodes that know the user identity can deanonymize the hint. A Stealth status with no attachments is not sent. A node with no user identity acts in `visible` mode unless its stored mode is `silent`. Every datagram names and is signed by the node identity. [`mod.nearby.mode`](types/mod.nearby.mode.md) lists what each mode discloses.

Two ops are exposed: `nearby.broadcast` triggers an immediate push of the local node's status, and `nearby.list` streams the cached `mod.nearby.status` of all currently known nearby peers.
