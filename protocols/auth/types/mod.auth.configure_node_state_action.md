# mod.auth.configure_node_state_action

A [`mod.auth.action`](mod.auth.action.md) requesting permission for the actor to
change the node's state: the values in its tree and the aliases in its
directory.

The action gates every operation that changes that state — `tree.set`,
`tree.delete` and `dir.set_alias` — and every policy setter:
`apphost.set_app_register_policy`, `apphost.set_grant_request_policy`,
`user.set_swarm_join_policy`, `user.set_swarm_invite_policy` and
`user.set_contract_accept_policy`. A policy is a tree value, so the setters
require the action that changes the tree. It covers `tree.set` in single-value and
streaming mode, `tree.delete` with and without `recursive`, and `dir.set_alias`
removing an alias as well as setting one.

Each operation submits the action before it reads input or changes state. A
refused caller is answered with an `error_message` reading `not permitted`.

Reading the same state answers to `mod.auth.see_node_state_action`. Neither
action implies the other.

A permit for this action carries no constraints. A permit whose `Constraints`
bundle is non-empty is refused rather than granted in full.

The user identity, the node's own identity and the node's
[manager](../../sys/README.md#manager) hold this action by default, and nobody
else. The manager holds it in every node state, `claimed` included. A node member of the node's swarm does not hold it, nor
[`mod.auth.see_node_state_action`](mod.auth.see_node_state_action.md). Any
other identity holds it through a node-local grant or a signed contract. A local
caller carrying no identity is routed as the node's own identity.

## Fields

* Action ([`mod.auth.action`](mod.auth.action.md)) – The embedded base action carrying the Nonce and ActorID.

In JSON the embedded action's fields appear directly in the `Object` value, not
under an `Action` key.

## Example

```json
{
  "Type": "mod.auth.configure_node_state_action",
  "Object": {
    "Nonce": "a1b2c3d4e5f60718",
    "ActorID": "0282fee8775757cdd8fda8b220195f5b8611312cd145c5a1a3aa55df210e779b2c"
  }
}
```
