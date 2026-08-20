# mod.auth.permit

A single capability granted by a `mod.auth.contract`. A permit names the
object type of an action and, optionally, a bundle of constraints that
narrow the grant.

## Fields

* Action (string8) – Object type of the action this permit grants
  (e.g. `mod.user.see_swarm_action`).
* Constraints (bundle) – Optional bundle of constraint objects. When the
  permitted action implements `Constrainable`, the action evaluates this
  bundle to decide whether the permit applies. Action types that do not
  implement `Constrainable` ignore the bundle and are permitted
  unconditionally.
* Delegation (uint8) – Bounds how many further hops a delegated authority
  chain may have below a link carrying this permit; `0` is non-delegable. In
  a chain, each link's permit must allow the number of hops below it, and
  constraints are evaluated at each link, so authority can only narrow.

## Example

```json
{
  "Type": "mod.auth.permit",
  "Object": {
    "Action": "mod.user.see_swarm_action"
  }
}
```
