# mod.auth.configure_node_state_action

A [`mod.auth.action`](mod.auth.action.md) requesting permission for the actor to
change the node's state: the values in its tree, the remote trees mounted into
it, and the aliases in its directory.

The action gates every operation that changes that state — `tree.set`,
`tree.delete`, `tree.mount_remote`, `tree.unmount` and `dir.set_alias`. It
covers `tree.set` in single-value and streaming mode, `tree.delete` with and
without `recursive`, and `dir.set_alias` removing an alias as well as setting
one.

Each operation submits the action before it accepts the query.
`tree.mount_remote` submits it before it resolves `identity` or queries the
remote tree. A refused caller receives no bytes.

Reading the same state answers to `mod.auth.see_node_state_action`. Neither
action implies the other.

A permit for this action carries no constraints. A permit whose `Constraints`
bundle is non-empty is refused rather than granted in full.

The user identity and the node's own identity hold this action by default, and
nobody else. A node member of the node's swarm does not hold it, and holds
[`mod.auth.see_node_state_action`](mod.auth.see_node_state_action.md) alone. Any
other identity holds it through a node-local grant or a signed contract. A local
caller carrying no identity is routed as the node's own identity.

## Fields

* Action ([`mod.auth.action`](mod.auth.action.md)) – The embedded base action carrying the Nonce and ActorID.

## Example

```json
{
  "Type": "mod.auth.configure_node_state_action",
  "Object": {
    "Action": {
      "Nonce": "a1b2c3d4e5f60718",
      "ActorID": "0282fee8775757cdd8fda8b220195f5b8611312cd145c5a1a3aa55df210e779b2c"
    }
  }
}
```
