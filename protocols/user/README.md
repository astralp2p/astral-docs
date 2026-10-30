# user

The `user` protocol manages the identity of the user that owns this node, the
swarm of nodes operating under that user, and the user's asset list.

A node joins a user's swarm by holding an active `mod.user.swarm_membership_action`
contract issued by that user. Once a node has an active contract it can serve
information about the user (`user.info`), enumerate the swarm
(`user.swarm_status`, `user.list_siblings`), maintain a synchronised list of
user assets (`user.assets`, `user.add_asset`, `user.remove_asset`,
`user.sync_assets`, `user.sync_with`).

Swarm membership is managed through contract ops: a user adopts a node with
`user.adopt` or lets it request membership with `user.request_membership`; a
node accepts an inbound contract with `user.accept_membership`, or activates an
already-signed contract with `user.accept_contract` (node setup and the
cold-card path). `user.bootstrap` claims an unclaimed node in one call: it
derives the user's key from BIP-39 words, signs the claim contract for both
parties, activates it and issues an access token for the user.
`user.derive_identity` answers the user that words derive and changes nothing.
`user.join` makes an unclaimed node request membership from a node of a swarm. A user permanently bans a node with `user.expel`, and the list
of bans is inspectable via `user.list_expelled`. Banned nodes hold a
`mod.user.signed_expulsion` and are refused new contracts.

Three policies decide membership from outside the node. The swarm join policy
decides each `user.request_membership`, the swarm invite policy decides each
`user.accept_membership`, and the contract accept policy decides each
`user.accept_contract`. All three accept everything by default, so a node out
of the box is claimable. `user.set_swarm_join_policy`,
`user.set_swarm_invite_policy` and `user.set_contract_accept_policy` delegate
each decision to an operation of another identity. Every setter requires
`mod.auth.admin_manage_apps_action`.

Two actions gate the protocol. `mod.user.see_swarm_action` covers every read —
`user.info`, `user.assets`, `user.sync_assets`, `user.list_siblings`,
`user.swarm_status` and `user.list_expelled` — and `user.new_node_contract`
when `user` is omitted on a claimed node. `mod.user.admin_swarm_action`
covers every change to what the swarm holds — `user.adopt`, `user.expel`,
`user.add_asset`, `user.remove_asset` and `user.sync_with`, which applies
another node's entries to this one. A node contract issued to a management node
carries both, delegable one hop.

When a node first links to a swarm member it synchronises with it: it pushes
the active contract, the membership contracts of the other members, the user's
expulsions, and the relay contracts of the apps it hosts, and it pulls the
member's asset updates. A pushed app relay contract lets the member route a
query addressed to the app through this node. An app registered while the two
nodes are already linked reaches the member at the next first link.

The active contract is validated on every application — both signatures, subject
identity match, remaining validity, and a swarm-membership permit — so a stored
value that fails validation never takes effect.
