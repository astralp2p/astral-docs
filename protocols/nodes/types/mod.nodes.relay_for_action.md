# mod.nodes.relay_for_action

An `auth.Action` that requests permission for the actor to relay traffic on behalf of `ForID`. Used by the auth module to gate relay capability per identity.

One handler decides it ([auth, Authority in a
swarm](../../auth/README.md#authority-in-a-swarm)): it allows the actor when it
is `ForID` itself. It is not node-local, so a contract the user signs delegates
relaying as the user through the ordinary walk. A node relays as the user only
through a relay contract the user key signs: no membership grants it, a
`privileged_member` membership included, and no node-local handler allows it.

## Fields

* ForID (identity) – The identity whose traffic the actor wishes to relay.

The embedded `auth.Action` provides the standard actor/target fields. The action carries no extra constraints (`ApplyConstraints` accepts only empty bundles).

## Example

```json
{
  "Type": "mod.nodes.relay_for_action",
  "Object": {
    "ForID": "037f990e61acee8a7697966afd29dd88f3b1f8a7b14d625c4f8742bd952003a590"
  }
}
```
