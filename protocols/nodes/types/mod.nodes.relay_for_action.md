# mod.nodes.relay_for_action

An `auth.Action` that requests permission for the actor to relay traffic on behalf of `ForID`. Used by the auth module to gate relay capability per identity.

Two handlers decide it ([auth, Authority in a
swarm](../../auth/README.md#authority-in-a-swarm)). One allows the actor when it
is `ForID` itself; it is not node-local, so a contract the user signs may
delegate relaying as the user through the ordinary walk. The other, with the
user as `ForID`, allows a node holding a `privileged_member` membership the user
key issued; it is node-local, so a Privileged member relays as the user itself
and no contract it signs passes that on.

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
