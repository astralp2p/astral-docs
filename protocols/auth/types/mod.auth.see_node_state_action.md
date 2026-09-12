# mod.auth.see_node_state_action

A [`mod.auth.action`](mod.auth.action.md) requesting permission for the actor to
read the node's state: tree values and listings, the directory's alias map and
filters, agent metadata, and the node's log stream. Every operation the action
guards submits it before it acts, and rejects the query when it is denied,
before it reads state, walks a tree path, or subscribes the caller to the log.
A refused caller receives no bytes.

One action covers `tree.get`, `tree.list`, `dir.alias_map`, `dir.filters`,
`dir.apply_filters`, `mcp.agent` and `log.listen`.

The action includes the log stream. A holder reads other callers' logged
activity as well as node metadata.

A path under a remote mount is walked on the remote node. `tree.get` and
`tree.list` submit the action before the walk, so a refused caller makes the
node query no other node.

`mcp.agent` answers an agent's record without its access token. The action
grants agent metadata and no credential.

The action grants no change to the state it reads.

`dir.resolve` and `dir.get_alias` submit no action. Apps resolve names and
aliases under their own identity.

A permit for this action carries no constraints. A permit whose `Constraints`
bundle is non-empty is refused rather than granted in full.

The user identity and the node's own identity hold this action by default, and
nobody else. Any other identity, a swarm sibling or an app included, holds it
through a node-local grant or a signed contract.

## Fields

* Action ([`mod.auth.action`](mod.auth.action.md)) – The embedded base action carrying the Nonce and ActorID.

## Example

```json
{
  "Type": "mod.auth.see_node_state_action",
  "Object": {
    "Action": {
      "Nonce": "a1b2c3d4e5f60718",
      "ActorID": "0282fee8775757cdd8fda8b220195f5b8611312cd145c5a1a3aa55df210e779b2c"
    }
  }
}
```
