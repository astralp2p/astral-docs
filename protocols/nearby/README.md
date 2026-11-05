# nearby

The `nearby` protocol lets nodes on one local network find each other with no address configured. A node broadcasts a [`mod.nearby.status_message`](types/mod.nearby.status_message.md) over [`ether`](../ether/README.md), and every node that receives it caches the sender. A node broadcasts a [`mod.nearby.scan_message`](types/mod.nearby.scan_message.md) to ask the other nodes for their status. nearby discovers nothing beyond the local network.

[`mod.nearby.mode`](types/mod.nearby.mode.md) decides what a node sends, and lists what each mode discloses:

* `0` (Silent) sends no nearby datagram. The node still receives.
* `1` (Visible) sends a [`mod.nearby.public_profile`](types/mod.nearby.public_profile.md) with the node identity, the user identity and the node alias. A node without an owner sends a [`mod.nearby.flag`](types/mod.nearby.flag.md) reading `adoptable` before the profile, and its profile names no user.
* `2` (Stealth) sends a [`mod.nearby.stealth_hint`](types/mod.nearby.stealth_hint.md), which only a node that knows the node identity or the user identity reads. A node without an active contract sends no status in Stealth.

The node's registered `Composer` implementations build these attachments. nearby then appends a [`mod.nearby.status_proof`](types/mod.nearby.status_proof.md) as the last attachment: the node key's signature over the other attachments, a nonce and the sender's time. When the status holds a `mod.nearby.stealth_hint`, which is the Stealth mode, the signature is wrapped with a key derived from the node identity. A status carries no endpoint, no contract and no `mod.dir.alias`.

A node broadcasts its status every 85 to 95 seconds, the interval drawn uniformly at random each time. It also broadcasts its status when its mode changes, when it gains a local address, on [`nearby.broadcast`](ops/nearby.broadcast.md), and in reply to a scan. [`nearby.scan`](ops/nearby.scan.md) broadcasts a scan. A node answers a scan by broadcasting its normal status on the one local subnet that contains the scan's source IP. It answers at most once per 2-second window on each subnet. A scan inside the window schedules one broadcast at the end of the window, unless one is already scheduled. A node never answers a scan by unicast, and does not answer a scan whose source IP lies in none of its subnets.

A node processes a received status in this order. It caches the sender as identified, and acts on it, only when every step passes:

1. Shape: the attachments hold exactly one `mod.nearby.public_profile` or exactly one `mod.nearby.stealth_hint`, not both. The last attachment is a `mod.nearby.status_proof`, no other attachment is one, and its `Sig` is 8 to 72 bytes.
2. Freshness: the proof's `Timestamp` is at most 5 minutes before or after the receiver's clock.
3. Cache room: the cache holds one entry per source IP and at most 512 entries. A status from a new source IP is dropped while the cache is full.
4. Identify: the node's registered recognizers try the status in turn, and the first that recognises it names the node identity and, when known, the user identity. The `user` module recognises the node's own user, in a stealth hint and in a profile whose `UserID` is that user. When no recognizer matches, a Visible status names the node and the user through its `mod.nearby.public_profile`. A Stealth status that no recognizer matches is cached with its source IP only, as an unrecognised node, and processing stops. Such a status is dropped when its source IP holds a live verified entry; it replaces only an unrecognised or expired entry.
5. Replay: the proof's `Nonce` is not remembered for the same node identity. The receiver remembers each nonce until 5 minutes after the proof's `Timestamp`, by the same clock as the freshness check, so a status stamped ahead of its arrival is remembered for up to 10 minutes. The receiver remembers at most 32 live nonces of one node and drops a status of a node at that bound. The memory holds at most 16416 nonces, 32 for each of 513 nodes. When the memory is full, the receiver forgets the nonces of every node without a live cache entry, except the node of the status in hand.
6. Verify: the receiver unwraps the signature of a Stealth status, and the signature verifies against the key of the identified node.
7. Accept: the receiver remembers the nonce and caches the node identity, the user identity, the source IP and how the node was identified. It emits a [`mod.nearby.peer_seen`](types/mod.nearby.peer_seen.md) event when the node is new to the cache, when its source IP changed, when its user identity changed (for example, the node was claimed), or when it returns after its entry expired. A repeated status that changes none of these emits nothing.

A cache entry expires 5 minutes after it was last updated, and the node removes expired entries periodically. [`nearby.list`](ops/nearby.list.md) lists the cache.

For a verified cache entry the node resolves two endpoints of the peer: `tcp` at the source IP on port `1791`, and `kcp` at the source IP on port `1792`. Both stay valid for the rest of the entry's life. The node resolves no endpoint for an unrecognised entry. A node that listens on other ports, and a second node on the same host, cannot be reached through nearby. A later version may carry a port list. The node resolves an alias `.name` to the verified peer whose `mod.nearby.public_profile` names the alias `name`.

The [`user`](../user/README.md) module acts on a `mod.nearby.peer_seen` only when it names the node's own user. It links at once to such a peer that is a swarm member and is not linked. It links to any other such peer, reads the peer's contract with [`user.contract`](../user/ops/user.contract.md), checks it, and introduces the node to the peer only when the check passes. Unowned nodes and nodes of other users are only cached and listed.

`silent_listen` in `nearby.yaml`, the tree value `/mod/nearby/silent_listen`, decides whether a Silent node acts on what it hears. It defaults to `true`, and a Silent node then contacts peers of its own user by the same rules as in the other modes. When it is `false`, a Silent node caches and lists peers but emits no `mod.nearby.peer_seen`.

nearby needs roughly synchronised clocks. The other nodes drop the statuses of a node whose clock is more than 5 minutes off. A device with no battery-backed clock and no time server cannot be found through nearby. Such a device is adopted by its node identity.

Three ops are exposed, each gated by [`mod.auth.admin_network_action`](../auth/types/mod.auth.admin_network_action.md): `nearby.broadcast` broadcasts the node's status now, `nearby.scan` asks the local network for statuses, and `nearby.list` streams the cache.
