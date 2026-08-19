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
cold-card path). A user permanently bans a node with `user.expel`, and the list
of bans is inspectable via `user.list_expelled`. Banned nodes hold a
`mod.user.signed_expulsion` and are refused new contracts.

Two actions gate the protocol. `mod.user.see_swarm_action` covers every read —
`user.info`, `user.assets`, `user.sync_assets`, `user.list_siblings`,
`user.swarm_status` and `user.list_expelled`. `mod.user.admin_swarm_action`
covers every change to what the swarm holds — `user.adopt`, `user.expel`,
`user.add_asset` and `user.remove_asset`. A node contract issued to a management
node carries both, delegable one hop.

The active contract is validated on every application — both signatures, subject
identity match, remaining validity, and a swarm-membership permit — so a stored
value that fails validation never takes effect.
