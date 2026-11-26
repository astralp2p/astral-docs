# sys.register_manager

Provision a fresh App identity and appoint it the node's
[manager](../README.md#manager). The operation provisions the identity as
[`apphost.register`](../../apphost/ops/apphost.register.md) does: a new keypair, an app contract
between the new identity and the node, and an access token. The node then
records the appointment. Only a `fresh` node ([Node states](../README.md#node-states))
appoints a manager. Local-only — a query from the network is answered
`origin not allowed: network`.

After accepting the query, the operation reads one
[`mod.sys.register_manager_request`](../types/mod.sys.register_manager_request.md)
from the channel. `Name`, `GrantPermits` and `ContractPermits` mean what they
mean in a [`mod.apphost.register_request`](../../apphost/types/mod.apphost.register_request.md).
`Policies` must be empty: the five policies are requests in SwarmState, which a
node answers with [`user.answer_request`](../../user/ops/user.answer_request.md).

The operation checks the request before it changes anything:

* Every permit of both lists passes the permit check of
  [Permits](../../apphost/README.md#permits).
* The request binds no policy.

No contract request is filed: the `fresh` node is its own root and signs one
node→app contract holding
[`mod.auth.serve_apps_action`](../../auth/types/mod.auth.serve_apps_action.md),
[`mod.auth.use_blueprints_action`](../../auth/types/mod.auth.use_blueprints_action.md),
every permit of `GrantPermits` and every permit of `ContractPermits`. The
contract expires with the access token.
`ContractPermits` may hold
[`mod.auth.sudo_action`](../../auth/types/mod.auth.sudo_action.md): the node
signs it, although [`apphost.register`](../../apphost/ops/apphost.register.md)
refuses it.

The node writes the manager record at `/mod/sys/manager` last and answers
the access token. The node is then `unclaimed`. A failure before the record is
written leaves the node `fresh`.

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
* An `error_message` object reading `policies are removed: answer the requests
  in SwarmState with user.answer_request` if `Policies` is not empty.
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
