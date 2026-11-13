# mod.vfs.manage_action

A [`mod.auth.action`](../../auth/types/mod.auth.action.md) requesting permission for the actor to administer the VFSes of the node. [`vfs.volumes`](../ops/vfs.volumes.md), [`vfs.create`](../ops/vfs.create.md), [`vfs.set_quota`](../ops/vfs.set_quota.md) and [`vfs.set_evaluator`](../ops/vfs.set_evaluator.md) submit this action. `vfs.set_evaluator` also allows the VFS identity without it. An operation answers `not permitted` when the action is denied.

The action names no VFS, and the node never asks a VFS's [evaluator](../README.md#evaluator) about it. The operations that submit it act on every VFS of the node, so a query that arrives from the network is answered `not permitted` whatever the caller holds.

The node's user and the node hold this action by default. On a node without a user, the node alone holds it. Any other identity holds it through a node-local grant or a signed contract. A permit for this action carries no constraints. A permit whose `Constraints` bundle is non-empty is refused rather than granted in full, so it grants nothing.

## Fields

* Action ([`mod.auth.action`](../../auth/types/mod.auth.action.md)) – The embedded base action carrying the Nonce and ActorID.

In JSON the embedded action's fields appear directly in the `Object` value.

## Example

```json
{
  "Type": "mod.vfs.manage_action",
  "Object": {
    "Nonce": "a1b2c3d4e5f60718",
    "ActorID": "0282fee8775757cdd8fda8b220195f5b8611312cd145c5a1a3aa55df210e779b2c"
  }
}
```
