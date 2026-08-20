# mod.auth.action

The base object embedded by every action type used by the `auth` protocol.
An action identifies what is being attempted and by whom; concrete action
types embed `mod.auth.action` and add their own fields.

## Fields

* Nonce (nonce64) – Random identifier for this action instance.
* ActorID (identity) – Identity of the caller performing the action.

A concrete action type (e.g. `mod.auth.sudo_action`,
`mod.user.see_swarm_action`) carries these fields plus any of its own.
When evaluating a contract, the auth module matches a permit to an action by
object type. Action types may additionally implement `Constrainable` to
evaluate the permit's `Constraints` bundle; action types that do not are
permitted unconditionally by any permit naming their type.

## Example

```json
{
  "Type": "mod.auth.action",
  "Object": {
    "Nonce": "a1b2c3d4e5f60718",
    "ActorID": "0282fee8775757cdd8fda8b220195f5b8611312cd145c5a1a3aa55df210e779b2c"
  }
}
```
