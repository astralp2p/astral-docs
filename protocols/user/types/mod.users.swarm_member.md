# mod.users.swarm_member

One entry in the swarm membership listing returned by `user.swarm_status`. It
describes a single node whose membership holds in SwarmState, signed by the
user or by the node that carried its join.

## Fields

* Identity (identity) – The node's identity.
* Alias (string8) – The node's alias as known to this node, or empty.
* Linked (bool) – `true` if this node has a live link to the member.

## Example

```json
{
  "Type": "mod.users.swarm_member",
  "Object": {
    "Identity": "0282fee8775757cdd8fda8b220195f5b8611312cd145c5a1a3aa55df210e779b2c",
    "Alias": "phone",
    "Linked": true
  }
}
```
