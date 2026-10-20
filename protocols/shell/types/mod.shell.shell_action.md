# mod.shell.shell_action

A [`mod.auth.action`](../../auth/types/mod.auth.action.md) requesting
permission for the actor to open an interactive shell session on the node.

The action gates [`shell.shell`](../ops/shell.shell.md). A session routes every
command to the op router of every loaded module, so admission is node-wide
administration rather than one capability. `shell.shell` submits the action for
the caller before it accepts the query. A refused caller receives no bytes.

Running the session as another identity through the `as` argument answers to
[`mod.auth.sudo_action`](../../auth/types/mod.auth.sudo_action.md) as well.
Neither action implies the other.

A shell permit is always unconstrained. The action does not evaluate a permit's
`Constraints` bundle, so a permit for it admits the holder to a full session
whatever constraints the permit carries.

The user identity and the node's own identity hold this action by default, and
nobody else. A node member of the node's swarm does not hold it. Any other
identity holds it through a node-local grant or a signed contract. A local
caller carrying no identity is routed as the node's own identity.

## Fields

* Action ([`mod.auth.action`](../../auth/types/mod.auth.action.md)) – The embedded base action carrying the Nonce and ActorID.

This action carries no extra fields of its own beyond the embedded
`mod.auth.action`. In JSON the embedded action's fields appear directly in the
`Object` value, not under an `Action` key.

## Example

```json
{
  "Type": "mod.shell.shell_action",
  "Object": {
    "Nonce": "a1b2c3d4e5f60718",
    "ActorID": "0282fee8775757cdd8fda8b220195f5b8611312cd145c5a1a3aa55df210e779b2c"
  }
}
```
