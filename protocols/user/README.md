# user

The `user` protocol manages the identity of the user that owns this node, the
swarm of nodes operating under that user, and the user's asset list.

A node joins a user's swarm by holding an active `mod.user.swarm_membership_action`
contract issued by that user. Once a node has an active contract it can serve
information about the user (`user.info`), enumerate the swarm
(`user.swarm_status`, `user.list_siblings`), maintain a synchronised list of
user assets (`user.assets`, `user.add_asset`, `user.remove_asset`,
`user.sync_assets`, `user.sync_with`). `user.contract` answers the active
contract to any caller that holds a direct link to the node.

Swarm membership is managed through contract ops: a user adopts a node with
`user.adopt` or lets it request membership with `user.request_membership`; a
node accepts an inbound contract with `user.accept_membership`, or activates an
already-signed contract with `user.accept_contract` (node setup and the
cold-card path). `user.bootstrap` claims a node without an active contract in one call: it
derives the user's key from BIP-39 words, signs the claim contract for both
parties, activates it and issues an access token for the user.
`user.derive_identity` answers the user that words derive and changes nothing.
`user.mnemonic` answers the words `user.bootstrap` stored, to the user or the
manager, for a later backup; `user.forget_mnemonic` deletes them.
`user.join` makes a node without an active contract request membership from a node of a swarm.
`user.introduce` pushes a claimed node's active contract to a member of its
user's swarm, which admits the node to that member's local swarm; a node claimed
with the user's words rejoins the swarm this way. A user permanently bans a node with `user.expel`, and the list
of bans is inspectable via `user.list_expelled`. Banned nodes hold a
`mod.user.signed_expulsion` and are refused new contracts.

A node emits a
[`mod.user.swarm_member_joined`](types/mod.user.swarm_member_joined.md) or
[`mod.user.swarm_member_left`](types/mod.user.swarm_member_left.md) event for
each node that enters or leaves its local swarm member set.

Three policies decide membership from outside the node. The swarm join policy
decides each `user.request_membership`, the swarm invite policy decides each
`user.accept_membership`, and the contract accept policy decides each
`user.accept_contract`. `policies.swarm_join`, `policies.swarm_invite` and
`policies.contract_accept` in `user.yaml` hold their config values, and all
three default to `reject_all`. `user.set_swarm_join_policy`,
`user.set_swarm_invite_policy` and `user.set_contract_accept_policy` delegate
each decision to an operation of another identity. A stored delegate outranks
the config value. Every setter requires
`mod.auth.configure_node_state_action`, which the node's manager holds
([sys, Manager](../sys/README.md#manager)).

```yaml
policies:
  swarm_join: reject_all
  swarm_invite: reject_all
  contract_accept: reject_all
reconcile_interval: 1h
```

Two actions gate the protocol. `mod.user.see_swarm_action` covers every read
except `user.contract` — `user.info`, `user.assets`, `user.sync_assets`,
`user.list_siblings`, `user.swarm_status` and `user.list_expelled` — and
`user.new_node_contract` when `user` is omitted on a claimed node.
`user.contract` asks for no action and answers every directly linked caller.
`user.relay_contracts` asks for no action and answers only the other members of
the local swarm.
`mod.user.admin_swarm_action` covers every change to what the swarm holds —
`user.adopt`, `user.expel`, `user.introduce`, `user.add_asset`,
`user.remove_asset` and `user.sync_with`, which applies another node's entries
to this one. A node contract issued to a management node
carries both, delegable one hop.

Each time a node gains a link to a swarm member, inbound or outbound, it
synchronises with it, in this order: it pushes the active contract, the user's
expulsions and the membership contracts of the other members, pulls the
member's alias, pushes the relay contracts of the apps the swarm's members
host, and pulls the member's asset updates. Every new link runs the
synchronisation, not only the first link to the member. The alias and asset
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
the member. A pushed app relay contract lets the member route a query addressed
to the app through the app's host. An app registered while the two nodes are
already linked reaches the member when it registers.
A member that routes a query to an app whose relay contract it does not hold
asks its linked members for it with `user.relay_contracts`, once per miss
([App Routing, Resolving the host](../../topics/app-routing.md#resolving-the-host)).

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

The active contract is validated on every application — both signatures, subject
identity match, remaining validity, and a swarm-membership permit — so a stored
value that fails validation never takes effect.
