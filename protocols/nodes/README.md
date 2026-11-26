# nodes

The `nodes` protocol manages encrypted links and multiplexed sessions between Astral nodes. It exposes operations for inspecting and managing links, resolving and registering known endpoints, and migrating sessions between links.

## Link admission

A node decides which identities it holds links with. Modules of the node
register admission rules; a rule refuses an identity or admits it. A node
without a rule that refuses an identity admits that identity, so apps, other
users' nodes, relays and unknown nodes link as before.

* A request for a link to a refused identity fails at once, without a dial. A
  query to a refused identity that no existing link carries answers route not
  found, and the node routes it through no relay.
* The node refuses an inbound connection from a refused identity right after the
  [Handshake](../../topics/link-mux.md#handshake): it closes the connection
  before [Negotiation](../../topics/link-mux.md#negotiation).
* The node checks every link before it adds the link to its links, and closes a
  link to a refused identity instead of adding it.
* When a rule starts to refuse an identity, the node closes every link it holds
  with that identity.

The [user](../user/README.md) module refuses nodes its user has expelled.

## Endpoint exchange in the local swarm

A node learns the endpoints of a member of its
[Local Swarm](../../core-definitions/local-swarm.md) by calling
[`nodes.resolve_endpoints`](ops/nodes.resolve_endpoints.md) on a linked member
and storing every returned endpoint with its TTL. A pull is a call of
`nodes.resolve_endpoints` on a member, the resolver, about a member, the
subject.

* When a new link is the node's only link to a member of its local swarm, the
  node pulls the endpoints of that member from that member, then forwards the
  [first-hand notice](#first-hand-notice) of that member.
* When one of the node's links to a member of its local swarm closes and
  another link to that member remains, the node pulls the endpoints of that
  member from that member over a remaining link.
* Every 35 minutes, shifted by a random share of at most 10% of the period in
  either direction, the node runs a periodic pull. Each run pulls, from that
  member over an existing link, the endpoints of every member of its local
  swarm, other than itself, it holds a link with and holds an unexpired
  `mod.tcp.endpoint` or `mod.kcp.endpoint` row of on a non-public address.
  The first run comes one such period after the node starts.
* The first run at least 24 h, shifted by a random share of at most 10% in
  either direction, after the node started or after the previous such run
  pulls every member of its local swarm, other than itself, it holds a link
  with.
* A periodic pull never dials. It stores the returned endpoints with their
  TTLs, so a row of a member that stays linked gets a new expiry and does not
  lapse. A member the node holds no link with is not pulled, so its rows on
  non-public addresses lapse within their 2 h TTL.
* The node runs one pull per member at a time for the link close and the
  periodic triggers together; a request during a pull starts at most one more
  pull after it. Each of these pulls is bounded to 20 s. A failed pull is logged and not
  retried before its next trigger.
* When the node's local swarm lists a member for the first time, as when its
  membership arrives through [SwarmState](#swarmstate), the node learns that
  member's endpoints. When it holds a link with the member, it makes a
  first-hand pull and forwards the [first-hand notice](#first-hand-notice).
  Otherwise it pulls the member's endpoints from the members it holds a link
  with, one at a time, each pull bounded to 20 s, until a pull stores a new row.
  It then emits a
  [`mod.nodes.endpoints_updated_event`](types/mod.nodes.endpoints_updated_event.md)
  naming the member. A membership reaches the members only through SwarmState,
  and both the first-link pull and the joiner's first announcement come before
  the members list the joiner.
* When a node's own set of advertised endpoints changes, the node announces the
  change to its linked members. A member that receives the announcement pulls
  the endpoints of the announcing node.

### First-hand notice

* A first-hand pull is a pull of a member's endpoints from that member itself.
  A node starts one on its first link to a member and when its local swarm
  lists a linked member for the first time through
  [SwarmState](#swarmstate).
* After a first-hand pull ends, the node forwards one
  [`mod.nodes.endpoints_changed_message`](types/mod.nodes.endpoints_changed_message.md)
  with `Subject` set to that member, as in step 4 of
  [Receiving an announcement](#receiving-an-announcement): to every member of the
  node's local swarm the node holds a link with, except that member, each push
  bounded to 15 s. A failed push is not retried.
* A member accepts the message only for a subject its local swarm lists.
* The node forwards whether or not the pull stored a new row, because a member
  that linked to the subject first already holds its rows and its own siblings
  still need the notice.
* A member that receives the forwarded message pulls the endpoints of `Subject`
  from the sender and never forwards it, so the notice travels one hop.

### Announcing a change

* Each of these starts a 5 s wait, unless a wait is already running. A trigger
  during the wait joins that wait and starts no second one:
  * a [`mod.ip.events.network_address_changed`](../ip/types/mod.ip.events.network_address_changed.md)
    event;
  * a link of the node created or closed, whichever identity it holds a link
    with;
  * the start of the node, once, when the node's scheduler is ready;
  * each run of the periodic pull of the members' endpoints, once per run,
    whatever the number of members, so a change without an event, such as an
    onion address that became available, is announced within about 40 minutes.
* An event whose `Added` and `Removed` hold only IPv6 link-local addresses
  starts no wait. A node never advertises an IPv6 link-local address.
* When the wait ends, the node computes the fingerprint of its advertised
  endpoint set: the SHA-256 of the sorted, deduplicated strings
  `<network>:<address>` of every endpoint that
  [`nodes.resolve_endpoints`](ops/nodes.resolve_endpoints.md) returns for the
  node's own identity. TTLs and the order of the endpoints do not enter the
  fingerprint.
* The node pushes only when the fingerprint differs from the one it announced
  last. The first fingerprint after the node starts always differs, so the node
  pushes once then, whatever the set holds. A wait that ends with an unchanged fingerprint pushes
  nothing.
* The node stores the fingerprint before it pushes. A push that reaches no
  member, because the node holds no link with one, still counts as announced;
  a member that links later pulls the endpoints on its first link.
* To push, the node sends one
  [`mod.nodes.endpoints_changed_message`](types/mod.nodes.endpoints_changed_message.md)
  with `Subject` set to its own identity to every member of its local swarm it
  holds a link with. Each push is bounded to 15 s. A failed push is not retried.
* The message carries no endpoints. Endpoints travel only through
  `nodes.resolve_endpoints`, which answers a holder of
  [`mod.auth.admin_network_action`](../auth/types/mod.auth.admin_network_action.md)
  and a member of the local swarm asking about a member
  ([Swarm only](ops/nodes.resolve_endpoints.md#swarm-only)).

### Receiving an announcement

A node accepts a pushed `mod.nodes.endpoints_changed_message` only when every
check passes:

* The sender is not the zero identity and is not the node itself.
* The node holds a link with the sender.
* The sender is a member of the node's local swarm.
* `Subject` is not the zero identity, is not the node itself, and is a member of
  the node's local swarm.

The node rejects any other `mod.nodes.endpoints_changed_message`, and the push
answers `false`. After accepting the message, the node:

1. Pulls the endpoints of `Subject` from the sender. The pull is bounded to 20 s.
   A failed pull is logged and not retried.
2. Counts the new rows. A row is new when the node held no unexpired endpoint of
   `Subject` with the same network and address before the pull. A row the pull
   refreshes is not new.
3. Emits a local
   [`mod.nodes.endpoints_updated_event`](types/mod.nodes.endpoints_updated_event.md)
   naming `Subject` when the pull stored at least one new row.
4. Forwards the message unchanged when the sender is `Subject`. The forward goes
   to every member of the node's local swarm the node holds a link with, except
   the sender and `Subject`, after the pull ends, with each push bounded to
   15 s. A message whose sender is not `Subject` is never forwarded, so a
   message travels at most one hop past the announcing node.

The [user](../user/README.md) module wakes the link to `Subject` on a
`mod.nodes.endpoints_updated_event`: a node that is not linked to `Subject`
dials at once instead of waiting out its backoff of up to 15 minutes.

An announcement carries no endpoints and withdraws none itself. The pull from
the announcing node that follows it withdraws the endpoints that node no longer
lists, as [Withdrawn endpoints](#withdrawn-endpoints) states.

### Withdrawn endpoints

A pull is first-hand when the resolver is the subject. After a first-hand pull
whose answer holds at least one endpoint, the node caps the expiry of some
stored rows of the subject at 1 hour from the pull:

* A row is capped when its network appears in the answer and its address does
  not.
* A row that expires earlier, and a row of a network the answer does not list,
  keep their expiry.
* A row that [`nodes.add_endpoint`](ops/nodes.add_endpoint.md) wrote keeps its
  expiry.
* A row without an expiry gets one 1 hour from the pull.

A pull that is not first-hand, and a first-hand pull with an empty answer,
cap no row. The node never deletes a row because a dial of it failed.

A row the answer lists is stored with the expiry its TTL gives, with two
exceptions that keep a later expiry:

* A pull that is not first-hand never moves the expiry of a stored row
  earlier.
* No pull moves the expiry of a row that `nodes.add_endpoint` wrote earlier.

## Dial order

The node keeps a health record per subject, network, address and scope. The
record holds two kinds of fact.

Claim facts say how consistently the subject lists the endpoint:

* the time of the first and of the last first-hand pull that listed it;
* the number of UTC days on which such a pull listed it.

Each first-hand pull counts the day for every endpoint its answer lists, once
per UTC day however many pulls come that day. A pull that is not first-hand
changes no claim fact. A claim fact never extends the expiry of an endpoint
row, and the node writes it under the scope `""`.

Dial facts say how the node's dials of the endpoint went:

* the time of the last success and of the last failure;
* the number of failures since the last success;
* a decaying success rate: each success moves it a share of 0.3 towards 1 and
  each failure a share of 0.3 towards 0; it starts from 0.5 before the first
  dial;
* a decaying dial and handshake time of the successes, which each success
  moves a share of 0.3 towards that success and the first success sets.

The node records the outcome of every dial of a known endpoint by the basic,
tor and nat strategies. A handshake that reaches another identity is a failure.
A dial that ends because its round was cancelled, as when another dial of the
round linked or every caller of the round left, is not recorded. A dial that
the round's budget ends is a failure. A row the round has not started to dial
when the round ends is not dialed and not recorded. The record is kept when the
endpoint row expires, and is deleted 30 days after its last update.

The node writes the dial facts of a `mod.tcp.endpoint` or `mod.kcp.endpoint` on
a non-public address under the scope of the network it dials from, the network
fingerprint, and the dial facts of every other endpoint under the scope `""`.
The network fingerprint is the first 8 bytes, in hexadecimal, of the SHA-256 of
the node's non-loopback interface subnets, each as network address and mask in
CIDR form, sorted, without repeats and joined by newlines. It is stable while
the node's subnets stay the same and changes when one changes. The node
recomputes it when it observes a change of its interface addresses. The node
sends it to no peer. When the node cannot read its interfaces, every endpoint
keeps its dial facts under the scope `""`.

The basic strategy waits up to 150 ms for the subject's rows, then reads the
subject's records under the scopes `""` and the current fingerprint and dials
the rows in two tiers:

1. Every row not in tier 2.
2. Rows with 3 or more failures since the last success, and `mod.tcp.endpoint`
   or `mod.kcp.endpoint` rows on a non-public, non-loopback address outside
   every subnet of the node's interfaces that have no recent success.

Within a tier the node dials rows by descending score, and keeps the order of
rows with equal scores; in tier 2 it dials every row with fewer than 3 failures
since the last success before any row with 3 or more. The score of a row is the sum of:

* 0.01 for each point of the row's network rank: `tcp` 50, `kcp` 40, `gw` 20,
  `tor` 10, any other network 0;
* the success rate of the row's dial facts under the scope the node dials the
  row from, or 0.5 for a row with no dial recorded under that scope;
* minus 0.2 times the dial and handshake time divided by 5 s, at most 0.2, for
  a row with a recorded success;
* 0.1 for a row whose subject listed it on 3 or more UTC days.

The node dials a tier 2 row once every earlier row's dial has returned, or
500 ms after the earlier rows started, whichever comes first. A tier 2 row on an
address outside every subnet of the node's interfaces dials under a 1 s budget.
When the node cannot read the subnets of its interfaces, no row counts as
outside them. A row that arrives after the 150 ms wait dials after the ordered
rows. Every row is dialed; the order never skips one.

## SwarmState

The `nodes` module keeps this node's copy of SwarmState, the grow-only set of
signed entries of the user's swarm
([user, SwarmState entries](../user/README.md#swarmstate-entries)). The copy
lives in the node's own [VFS](../vfs/README.md), owned by the node identity,
under `swarmstate/<kind>/<object id>`. `/swarmhead` holds the number of stored
entries in decimal; it only grows and is never synced. A merge is a union:
nothing is overwritten or deleted. The `user` module checks every entry before
it is stored: an entry it drops is neither stored nor passed on, and an entry
that waits for what it needs (a signer's membership, the request an answer
names) is held, at most 1024 at once, and checked again after the next
accepted merge.

Three operations exchange the set between nodes:

* [`nodes.swarm_digest`](ops/nodes.swarm_digest.md) answers the entry IDs this
  node stores;
* [`nodes.swarm_fetch`](ops/nodes.swarm_fetch.md) answers the stored entries
  among the IDs it receives;
* [`nodes.swarm_push`](ops/nodes.swarm_push.md) offers one entry.

`nodes.swarm_digest` and `nodes.swarm_fetch` serve this node, the user, and
every identity whose membership holds here. `nodes.swarm_push` serves every
identified caller, since the check decides what enters. A node pulls (digest,
then fetch of what it lacks, at most 256 IDs per fetch) from every linked swarm
member every 15 seconds. On a first link of a claimed node it first offers the
peer its own membership, so the peer admits its pull, and then pulls. When the
node stores its own membership, as at a claim, it does the same with every
peer it holds a link with. A node claimed while already linked therefore needs
no new link. Every entry this node stores is pushed to its linked swarm
members. Each member gets its own push, in the order the entries were stored,
and each push is bounded to 15 s. The write that stored the entries does not
wait for these pushes. A failed push is not retried: the member's pull repairs
it.
