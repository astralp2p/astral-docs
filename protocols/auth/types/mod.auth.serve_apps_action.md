# mod.auth.serve_apps_action

A [`mod.auth.action`](mod.auth.action.md) requesting permission for the actor to
host on the node: install an app handler that receives queries addressed to the
actor, and publish the actor's service advertisement.

The authority is a place on the node, not access to data. It grants no right to
remove another identity's handlers or advertisements.

One action covers the two hosting operations —
[`apphost.register_handler`](../../apphost/ops/apphost.register_handler.md) and
[`services.advertise`](../../services/ops/services.advertise.md). Both
operations reject a query from the network before they submit the action, so no
permit lets a remote identity host on the node.

The same action covers the guest message `mod.apphost.register_service_msg`
([Astral IPC](../../../topics/astral-ipc.md#receiving-queries)). The host submits
the action for the identity named in the message, after its session and
`SudoAction` checks, and answers `mod.apphost.error_msg{denied}` when the
identity does not hold it.

A permit for this action carries no constraints. A permit whose `Constraints`
bundle is non-empty is refused rather than granted in full.

The user identity and the node's own identity hold this action by default.
A `privileged_member` node of the node's swarm holds it through the swarm
root ([auth, Authorization](../README.md#authorization)).
Any other identity holds it only
through a contract chain the node has indexed, such as the contract an app's
host signs to carry out an Approval.

[`apphost.register`](../../apphost/ops/apphost.register.md) files a contract
request for this action for each new app. The app holds it once the swarm
approves the request.

## Fields

* Action ([`mod.auth.action`](mod.auth.action.md)) – The embedded base action carrying the Nonce and ActorID.

In JSON the embedded action's fields appear directly in the `Object` value, not
under an `Action` key.

## Example

```json
{
  "Type": "mod.auth.serve_apps_action",
  "Object": {
    "Nonce": "a1b2c3d4e5f60718",
    "ActorID": "0282fee8775757cdd8fda8b220195f5b8611312cd145c5a1a3aa55df210e779b2c"
  }
}
```
