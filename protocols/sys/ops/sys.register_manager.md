# sys.register_manager

Provision a fresh App identity and appoint it the node's
[manager](../README.md#manager). The operation provisions the identity as
[`apphost.register`](../../apphost/ops/apphost.register.md) does: a new keypair, an app contract
between the new identity and the node, and an access token. The node then
binds the policies the request names to the new identity and records the
appointment. Only a `fresh` node ([Node states](../README.md#node-states))
appoints a manager. Local-only — a query from the network is answered
`origin not allowed: network`.

After accepting the query, the operation reads one
[`mod.sys.register_manager_request`](../types/mod.sys.register_manager_request.md)
from the channel. `Name`, `GrantPermits` and `ContractPermits` mean what they
mean in a [`mod.apphost.register_request`](../../apphost/types/mod.apphost.register_request.md).
`Policies` lists the policies the manager decides, one
[`mod.sys.policy_binding`](../types/mod.sys.policy_binding.md) each.

The operation checks the request before it changes anything:

* Every permit of both lists passes the permit check of
  [Grants](../../apphost/README.md#grants).
* Every binding names one of `app_register`, `grant_request`, `swarm_join`,
  `swarm_invite` and `contract_accept`, and no name appears twice.
* Every binding names an operation.
* Every binding's `Timeout` lies in 0 to 10 minutes.
* A binding of `swarm_join`, `swarm_invite` or `contract_accept` requires the
  `user` module.

The app register policy is not asked. The node writes node-local grants of
[`mod.auth.serve_apps_action`](../../auth/types/mod.auth.serve_apps_action.md)
and
[`mod.auth.use_blueprints_action`](../../auth/types/mod.auth.use_blueprints_action.md),
every permit of `GrantPermits` as a node-local grant, and every permit of
`ContractPermits` in a signed node→app contract. Every grant and the contract
expire with the access token.
`ContractPermits` may hold
[`mod.auth.sudo_action`](../../auth/types/mod.auth.sudo_action.md): the node
signs it, although [`apphost.register`](../../apphost/ops/apphost.register.md)
refuses it.

For each binding, the node stores a delegate with the new identity as
`identity`, the binding's `Operation` as `operation` and its `Timeout` as
`timeout`, at the tree path of the policy
([Node Policies](../../../topics/node-policies.md#the-five-policies)).
The node clears the stored delegate of every policy the request does not name.
The grant request mode is not changed. On a node without the `user` module, the
node leaves the three `user` policies untouched.

The node writes the manager record at `/mod/sys/manager` last and answers
the access token. The node is then `unclaimed`. A failure before the record is
written leaves the node `fresh`. A repeat call binds every policy again, so it
replaces the delegates a failed call stored.

Calls run one at a time. Of two concurrent calls on a `fresh` node, one
appoints the manager and the other answers `node is not fresh`.

The default gate admits `sys.register_manager`, with a token or without,
on a `fresh` and on a `claimed` node, and refuses it on an `unclaimed` node
([Gate](../../apphost/README.md#gate)). A `claimed` node answers `node is not fresh`.

## Arguments

* in (string8) – Input format.
* out (string8) – Output format.

The request travels as the channel's single input object.

A channel that closes before the input object arrives receives no answer, and
no identity is minted. `astral-query` keeps the channel open after stdin ends
([Ending input](../../../tools/astral-query.md#ending-input)).

## Returned objects

The operation returns one of:
* An `error_message` object reading `origin not allowed: network` if the query
  arrived over a link.
* An `error_message` object reading `unexpected object: <type>` if the input
  object is not a `mod.sys.register_manager_request`, for example
  `unexpected object: eos` for an `eos`.
* An `error_message` object reading `invalid permit: <action>: <detail>`, or
  `invalid permit: missing action`, if a permit fails the check.
* An `error_message` object reading `unknown policy: <name>` if a binding names
  another policy.
* An `error_message` object reading `policy bound twice: <name>` if two
  bindings name one policy.
* An `error_message` object reading `policy <name>: no operation named` if a
  binding names no operation.
* An `error_message` object reading `policy <name>: timeout outside 0..10m0s`
  if a binding's `Timeout` is negative or above 10 minutes.
* An `error_message` object reading
  `policy <name>: the user module is not loaded` if a binding names a `user`
  policy on a node without the `user` module.
* An `error_message` object reading `node is not fresh` if the node has a
  manager, has an active contract, or has held one before.
* An `error_message` object if any later step failed. The node stays `fresh`.
* An `apphost.access_token` object containing the manager's token.

The operation checks the request before it checks the node state.

## Examples

```shellsession
$ echo '{"Type":"mod.sys.register_manager_request","Object":{"Name":"control-plane","GrantPermits":[],"ContractPermits":[],"Policies":[{"Policy":"app_register","Operation":"cp.approve_app","Timeout":0},{"Policy":"swarm_join","Operation":"cp.approve_join","Timeout":300000000000}]}}' | astral-query sys.register_manager -in json -out json
{"Type":"apphost.access_token","Object":{"Identity":"03864ef025fde8fb587d989186ce6a4a186895ee44a926bfc370e2c366597a3f8f","Token":"b9c2e1a3d4f5867a","ExpiresAt":"2036-05-25T12:00:00+02:00"}}
```

A node that is not fresh:

```shellsession
$ echo '{"Type":"mod.sys.register_manager_request","Object":{"Name":"control-plane","GrantPermits":[],"ContractPermits":[],"Policies":[]}}' | astral-query sys.register_manager -in json -out json
{"Type":"error_message","Object":"node is not fresh"}
```
