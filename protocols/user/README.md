# user

The `user` protocol manages the identity of the user that owns this node, the
swarm of nodes operating under that user, and the user's asset list.

A node joins a user's swarm by holding a membership: a
[`mod.auth.signed_contract`](../auth/types/mod.auth.signed_contract.md) with one
tier permit (`member`, `trusted` or `privileged_member`) whose link holds in
SwarmState ([SwarmState entries](#swarmstate-entries)). The swarm's members are
the identities whose membership holds there. Once a node has an active contract
it can serve information about the user (`user.info`), enumerate the swarm
(`user.swarm_status`, `user.list_siblings`), maintain a synchronised list of
user assets (`user.assets`, `user.add_asset`, `user.remove_asset`,
`user.sync_assets`, `user.sync_with`). `user.contract` answers the active
contract to any caller that holds a direct link to the node.

The user key signs every `privileged_member` membership in a ceremony.
`user.bootstrap` claims a node without an active contract in one call: it
derives the user's key from BIP-39 words, signs the node's privileged
membership for both parties, activates it and issues an access token for the
user. `user.accept_contract` activates a privileged membership already signed
by the user key and by this node (node setup and the cold-card path).
`user.derive_identity` answers the user that words derive and changes nothing.
`user.mnemonic` answers the words `user.bootstrap` stored, to the user or the
manager, for a later backup; `user.forget_mnemonic` deletes them.
[`user.join`](ops/user.join.md) makes a node without an active contract ask to
join through a `trusted` or `privileged_member` node, its carrier, with a join
request; the carrier writes it into SwarmState with
[`user.carry_join`](ops/user.carry_join.md) and hands over the membership once
the request is answered. `user.introduce` pushes a claimed node's active
contract to a member of its user's swarm. Only the user expels: `user.expel`
needs `mod.user.expel_action`, signs the ban with the user key and adds it to
SwarmState; the list of bans is inspectable via `user.list_expelled`. Banned
nodes hold a `mod.user.signed_expulsion`.

The user module applies no admission policy. A join, an invitation and an app's
permits are requests in SwarmState that a node with the right tier answers
([SwarmState entries](#swarmstate-entries)).

A node emits a
[`mod.user.swarm_member_joined`](types/mod.user.swarm_member_joined.md) or
[`mod.user.swarm_member_left`](types/mod.user.swarm_member_left.md) event for
each node that enters or leaves its local swarm member set.

```yaml
reconcile_interval: 1h
sibling_sync_interval: 6h
sibling_sync_disabled: false
```

Two actions gate the protocol. `mod.user.see_swarm_action` covers every read
except `user.contract` — `user.info`, `user.assets`, `user.sync_assets`,
`user.list_siblings`, `user.swarm_status` and `user.list_expelled` — and
`user.new_node_contract` when `user` is omitted on a claimed node.
`user.contract` asks for no action and answers every directly linked caller.
`user.relay_contracts` and `user.relay_digest` ask for no action and answer only
the other members of the local swarm.
`mod.user.admin_swarm_action` covers every change to what the swarm holds —
`user.introduce`, `user.add_asset`, `user.remove_asset`, `user.sync_with`, which
applies another node's entries to this one, and `user.answer_request`.
`mod.user.expel_action` covers `user.expel`. The user holds every action; a
`privileged_member` node holds every action but these two and
`mod.user.expel_action` through the swarm root
([auth](../auth/README.md)).

Each time a node gains a link to a swarm member, inbound or outbound, it
synchronises with it, in this order: it pushes the active contract, the user's
expulsions and the membership contracts of the other members, pulls the
member's alias, pushes the relay contracts of the apps the swarm's members
host that the member lacks, and pulls the member's asset updates. Every new
link runs the synchronisation, not only the first link to the member. The alias and asset
pulls query the member as the user, and the member admits them only once it
holds this node's contract. A node also synchronises with a linked node when a
pushed membership contract admits that node to its local swarm, because the
link to that node preceded the contract. A node also synchronises with a
member when one of its links to the member closes and another link to the
member remains. A new link to a member makes the node probe its older links to
that member ([Link Mux, Keepalive](../../topics/link-mux.md#keepalive)), so a
dead older link closes within its ping timeout and the synchronisation runs
over a remaining link. The node runs one such synchronisation per member at a
time; closes during it start at most one more after it. The relay contracts
it pushes are those it holds that pass the admission rule of
[App Routing](../../topics/app-routing.md#reach), except those whose subject is
the member and except those the member holds. Before it pushes, the node asks
the member which relay contracts it holds with
[`user.relay_digest`](ops/user.relay_digest.md), as itself, within 10 seconds,
and skips each relay contract whose object ID the member lists. A node pushes
no relay contract when the member lists all of them. A relay contract the member
refused or never received is absent from its digest, so the node pushes it on
the next synchronisation. A digest that fails, whether by error, refusal,
unknown operation, an unfinished stream or the 10 seconds, leaves the node
pushing every relay contract it would push without a digest. The digest changes
no admission: the member admits each pushed relay contract by the same rule as
any other. A pushed app relay contract lets the member route a query addressed
to the app through the app's host. An app registered while the two nodes are
already linked reaches the member when it registers: the node pushes the
registered app's relay contract to every linked member at once, and pushes it
again to a member the push did not reach, up to 3 times, after 10 seconds, after
1 minute and after 5 minutes. A member's retries stop at its first answer,
whether the member accepts the contract or refuses it, when the member is no
longer a linked member, and when the node stops. A member that refuses the
contract receives it again from a later synchronisation, once its local swarm
lists the node.
A member that routes a query to an app whose relay contract it does not hold
asks its linked members for it with `user.relay_contracts`, once per miss
([App Routing, Resolving the host](../../topics/app-routing.md#resolving-the-host)).

A node synchronises with every linked member again every `sibling_sync_interval`
(`user.yaml`, default 6 hours), in the order and by the rules of a new link's
synchronisation, so a member that missed a relay contract for any reason holds it
within one interval. Each wait lasts the interval plus a random delay of up to
10 % of it. A zero `sibling_sync_interval` selects the default; a negative one,
or `sibling_sync_disabled: true`, turns the periodic synchronisation off. The
periodic synchronisation reaches linked members only. It starts one
synchronisation per linked member, concurrently, and skips a member whose
previous periodic synchronisation has not finished. A link-triggered
synchronisation with the member is unaffected and runs when its link event
fires.

A node wakes its link to a member of its local swarm when a
[`mod.nodes.endpoints_updated_event`](../nodes/types/mod.nodes.endpoints_updated_event.md)
names the member: a node that is not linked to the member dials at once instead
of waiting out the link's backoff of up to 15 minutes
([Endpoint exchange in the local swarm](../nodes/README.md#endpoint-exchange-in-the-local-swarm)).

A node redelivers the user's expulsions. Each time a node gains a link to a
node its user has expelled, it pushes the user's expulsions to that node, the
expelled node's own expulsion included, and synchronises nothing else with it.
Every `reconcile_interval` (`user.yaml`, default 1 hour) a node pushes the
user's expulsions to every linked swarm member and to every linked node its
user has expelled. A zero or negative `reconcile_interval` selects the default.
A node that receives an expulsion it already holds stores nothing new and closes
its links to the expelled node again. A node that receives its own expulsion
leaves the swarm: it stops maintaining its links to the members, closes them and
clears its active contract.

A node refuses links with a node its user has expelled once the expelled node
has answered a push of its own expulsion from this node, by accepting it or by
rejecting it ([Link admission](../nodes/README.md#link-admission)). Until that
answer the node admits the expelled node's links, so the expelled node can
receive its expulsion over them. When the answer arrives, the node closes its
links with the expelled node, and it neither dials the expelled node nor
accepts its connections again. The node keeps the answers in memory only: after
a restart it admits the expelled node until the expelled node answers again. A
node without an active contract refuses no node. On the node that issues the
expulsion, the answer ends the direct push of the expulsion to the expelled
node, so that push completes before the node closes its links with it.

A node contacts the nodes [`nearby`](../nearby/README.md) finds on the local
network only when the peer's `mod.nearby.peer_seen` names the node's own user.
It links at once to such a peer that is a member of its local swarm and is not
linked, instead of waiting out the link's backoff of up to 15 minutes. It
contacts any other such peer at most once a minute, and at most once an hour
after the peer's contract failed the check. A failed link or query holds the next
attempt for a minute only. The node keeps these limits for at most 512 peers; when
it holds 512, it forgets the peer whose next attempt comes first. It links to the peer at the
endpoints nearby resolves, reads the peer's contract with `user.contract`, and
checks it: a node contract issued by the node's user to the peer, both
signatures valid, not expired, and the peer not expelled. Only when the check
passes does the node introduce itself as `user.introduce` does: it pushes its
active contract, and the two synchronise. A failed check sends nothing of the
node's own. Unowned nodes and nodes of other users are listed, never contacted.
A `user.introduce` call is unaffected.

The active contract is validated on every application — the issuer's signature,
the subject's when present, subject identity match, remaining validity, and one
tier permit — so a stored value that fails validation never takes effect. A node
a carrier admitted stores the user identity beside it, since its membership's
issuer is the carrier.

## SwarmState entries

The `user` protocol defines the entry types of SwarmState, the signed record of
who belongs to a user's swarm and what its members asked for and were given.
The `nodes` module stores each node's copy in the node's own VFS and syncs it
([nodes, SwarmState](../nodes/README.md#swarmstate)); the `user` module decides
what an entry means and checks every entry before it is stored.
[`user.swarm_requests`](ops/user.swarm_requests.md) lists the stored requests
with their status, and [`user.answer_request`](ops/user.answer_request.md)
answers one with an approval or a decline signed by the node.
[`user.confirm_join`](ops/user.confirm_join.md) is the user's confirmation of a
join request at tier `privileged_member` when the user key is a software key
held on the node; it is accepted only from a local query by the user.

An entry is a signed object, stored as `swarmstate/<kind>/<object id>`, where
the kind is a [`mod.user.entry_kind`](types/mod.user.entry_kind.md):

| Kind | Entry | Signed by |
|------|-------|-----------|
| `requests` | [`mod.user.signed_contract_request`](types/mod.user.signed_contract_request.md) | the filing node |
| `requests` | [`mod.user.signed_join_request`](types/mod.user.signed_join_request.md) | the joining node |
| `requests` | [`mod.user.signed_expel_request`](types/mod.user.signed_expel_request.md) | the filing member |
| `approvals` | [`mod.user.signed_approval`](types/mod.user.signed_approval.md) | the answering member or the user key |
| `declines` | [`mod.user.signed_decline`](types/mod.user.signed_decline.md) | the answering member or the user key |
| `contracts` | [`mod.auth.signed_contract`](../auth/types/mod.auth.signed_contract.md), memberships included | issuer, and subject when present |
| `expels` | [`mod.user.signed_expulsion`](types/mod.user.signed_expulsion.md) | the user key |

An entry's ID is the object ID of the signed form exactly as stored, signatures
included. Every reference holds that ID: an answer's `RequestID` and a
contract's `ApprovalID`. It differs from the ID of the unsigned body, which the
signatures commit to.

A request stays answerable for at most 1 hour: its `Timeout` is after its
`FiledAt` and at most 1 hour after it, and a new request defaults to exactly 1
hour. Its status is a [`mod.user.request_status`](types/mod.user.request_status.md),
derived from the stored answers and never stored. A decline beats every
approval of the same request. Who may answer a request depends on the
answerer's [tier](types/mod.user.tier.md), as
[`mod.user.approval`](types/mod.user.approval.md) lists. The merge check decides
each offered entry with a
[`mod.user.entry_verdict`](types/mod.user.entry_verdict.md).

Each signed body's signable text is one ASCII line of at most 240 bytes, the
signer's commitment included, so a Coldcard can sign it
([coldcard](../coldcard/README.md)).

### Memberships

A membership is a [`mod.auth.contract`](../auth/types/mod.auth.contract.md) by
which the issuer admits the subject at a [tier](types/mod.user.tier.md). There
is no separate membership wire type: SwarmState stores a membership as a
`mod.auth.signed_contract` in `contracts`.

A contract is a membership when it carries exactly one tier permit, one of
[`mod.user.member_action`](types/mod.user.member_action.md),
[`mod.user.trusted_action`](types/mod.user.trusted_action.md) and
[`mod.user.privileged_member_action`](types/mod.user.privileged_member_action.md);
that permit names its tier. A contract with no tier permit, or with more than
one, is not a membership. Reading a contract as a membership checks neither its
signatures, its expiry, its approval nor the user's expels.

A new membership carries that one tier permit, with no constraints and no
delegation, and an expiry. Its `ApprovalID` names the approval it carries out,
or is `null` when the user key signs it directly. The permit puts the tier in
the contract's signable text, so a Coldcard shows it, for example:

```
<issuer> grants <subject> privileged_member permits (1) until 2027-11-25 10:00:00
```
