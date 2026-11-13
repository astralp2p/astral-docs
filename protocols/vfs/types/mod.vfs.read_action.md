# mod.vfs.read_action

A [`mod.auth.action`](../../auth/types/mod.auth.action.md) requesting permission for the actor to read the VFS named by `VFSID`. [`vfs.ls`](../ops/vfs.ls.md), [`vfs.stat`](../ops/vfs.stat.md), [`vfs.statfs`](../ops/vfs.statfs.md) and [`vfs.read`](../ops/vfs.read.md) submit this action before they look up the VFS. An operation answers `not permitted` when the action is denied, and [`vfs.read`](../ops/vfs.read.md) rejects the query instead.

The action is allowed for the VFS identity itself and for the node's user and the node, which hold it for every VFS. Any other identity holds it through a node-local grant or a signed contract. A VFS identity or a root caller that signs a contract for the action is honoured at every level of a contract chain, once the node has indexed the contract. A contract issued on this node is indexed when it is issued.

The `Constraints` bundle of a permit holds `identity` objects, and the permit covers exactly the VFSes it lists. A permit without constraints, or with an empty bundle, covers no VFS, and a grant or registration that carries such a permit is refused with `invalid permit: mod.vfs.read_action: requires constraints`. A bundle with a member that is not an `identity`, or whose member is the zero identity, makes the whole permit cover nothing. A permit covers a whole VFS and does not narrow to a folder or a file.

A permit for this action also allows [`objects.read`](../../objects/ops/objects.read.md), [`objects.load`](../../objects/ops/objects.load.md), [`objects.contains`](../../objects/ops/objects.contains.md) and [`objects.probe`](../../objects/ops/objects.probe.md) of the content of a file of the listed VFS by `Object ID`. See [`mod.auth.see_objects_action`](../../auth/types/mod.auth.see_objects_action.md).

## Fields

* Action ([`mod.auth.action`](../../auth/types/mod.auth.action.md)) – The embedded base action carrying the Nonce and ActorID.
* VFSID (identity) – The VFS identity the actor asks to read.

In JSON the embedded action's fields appear directly in the `Object` value, beside `VFSID`, not under an `Action` key.

## Example

```json
{
  "Type": "mod.vfs.read_action",
  "Object": {
    "Nonce": "a1b2c3d4e5f60718",
    "ActorID": "0282fee8775757cdd8fda8b220195f5b8611312cd145c5a1a3aa55df210e779b2c",
    "VFSID": "02bef8840eb35ef2ae3c83c07cb5779278904f99cb4103f71e37cc69931ae5e15f"
  }
}
```
