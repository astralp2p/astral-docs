# apphost.register

Provision a fresh guest identity end-to-end: generate a new keypair, sign and
store an app contract between the new identity and the node, and issue an
access token. Used by apps/agents to bootstrap themselves on first run.
Local-only — a query from the network is answered `origin not allowed: network`.

After accepting the query, the operation reads one
[`mod.apphost.register_request`](../types/mod.apphost.register_request.md) from
the channel. The request carries the name the app gives itself and the permits
it asks to hold, with their constraints, in `GrantPermits` and
`ContractPermits`. Both lists mean the same: no node-local grant exists
([Permits](../README.md#permits)).

The operation checks every permit of both lists first
([Permits](../README.md#permits)). A permit that fails the check refuses the
registration with an `error_message` reading `invalid permit: …`, and no
identity is minted. A registration that asks for a
[`mod.auth.sudo_action`](../../auth/types/mod.auth.sudo_action.md) or a
[`mod.nodes.relay_for_action`](../../nodes/types/mod.nodes.relay_for_action.md)
permit is refused with an `error_message` reading `a registration names
<action>`, and no identity is minted.

Registration is never declined: the node issues the identity and the access
token at once. Asking is
not receiving. The node files one
[`mod.user.signed_contract_request`](../../user/types/mod.user.signed_contract_request.md)
in SwarmState for the new identity, asking for
[`mod.auth.serve_apps_action`](../../auth/types/mod.auth.serve_apps_action.md),
[`mod.auth.use_blueprints_action`](../../auth/types/mod.auth.use_blueprints_action.md)
and every permit the registration asks for. A Privileged node answers it with
[`user.answer_request`](../../user/ops/user.answer_request.md) with an offer;
the host co-signs the offer and signs the app's contract
([Contract requests](../README.md#contract-requests)). Until then the app holds
no permit, so it registers no handler. The app waits for the outcome with
[`apphost.request_contract`](apphost.request_contract.md) and the same
permits, which finds the filed request instead of filing another. A node that
cannot file the request (no `user` module, or the rate limit) still answers the
token and logs the failure.

The default gate admits `apphost.register`, with a token or without, on an
`unclaimed` and on a `claimed` node, and refuses it on a `fresh` node
([Gate](../README.md#gate)). A `fresh` node appoints a manager first with
[`sys.register_manager`](../../sys/ops/sys.register_manager.md).

After the access token is minted, the operation creates the
[`VFS`](../../vfs/README.md) of the new identity with the default quotas: the
`byte_limit` and `inode_limit` of the `vfs` module configuration, `1073741824`
bytes and `1000000` inodes by default. The VFS names the app its
[evaluator](../../vfs/README.md#evaluator), with the endpoint
`astral://<app identity>:vfs.authorize`, so the node asks the app about a read
or a write of the VFS that the built-in rules refuse. Two fields of the
request turn this off, and both are on when absent:

* `Vfs` false creates no VFS, and `Evaluator` then has no effect.
* `Evaluator` false creates the VFS with an empty evaluator.

Creating the VFS and naming its evaluator need no permit. A
failure to create the VFS or to name its evaluator answers an `error_message`
and no token, though the identity, its contract and its token exist by then. An app registered with
the defaults serves `vfs.authorize`; an app that does not registers with
`Evaluator` false.
[`sys.register_manager`](../../sys/ops/sys.register_manager.md) provisions the
manager app without a VFS.

An app can ask for service discovery at registration. A
[`mod.services.service_discovery_action`](../../services/types/mod.services.service_discovery_action.md)
permit needs constraints holding exactly one
[`mod.services.discovery_scope`](../../services/types/mod.services.discovery_scope.md)
that names a service; the request asks for it as sent. An unconstrained
discovery permit is refused before anything is filed
([Who sees an offering](../../../topics/services.md#who-sees-an-offering)).

## Arguments

* in (string8) – Input format.
* out (string8) – Output format.

The registration travels as the channel's single input object. The arguments
`name`, `grant_permits` and `contract_permits` are removed. A query that names
one is answered `unknown argument: <name>`, and no identity is minted.

A channel that closes before the input object arrives receives no answer, and
no identity is minted. `astral-query` keeps the channel open after stdin ends
([Ending input](../../../tools/astral-query.md#ending-input)).

## Returned objects

The operation returns one of:
* An `error_message` object reading `origin not allowed: network` if the query
  arrived over a link.
* An `error_message` object reading `unknown argument: <name>` if the query
  names `name`, `grant_permits` or `contract_permits`.
* An `error_message` object reading `unexpected object: <type>` if the input
  object is not a `mod.apphost.register_request`, for example
  `unexpected object: eos` for an `eos`.
* An `error_message` object reading `invalid permit: <action>: <detail>`, or
  `invalid permit: missing action`, if a permit fails the check.
* An `error_message` object reading `a registration names <action>` if a
  permit asks for `mod.auth.sudo_action` or `mod.nodes.relay_for_action`.
* An `error_message` object if any later step failed.
* An `apphost.access_token` object containing the new guest's token.

## Examples

```shellsession
$ echo '{"Type":"mod.apphost.register_request","Object":{"Name":"","GrantPermits":[],"ContractPermits":[]}}' | astral-query apphost.register -in json -out json
{"Type":"apphost.access_token","Object":{"Identity":"03864ef025fde8fb587d989186ce6a4a186895ee44a926bfc370e2c366597a3f8f","Token":"b9c2e1a3d4f5867a","ExpiresAt":"2036-05-25T12:00:00+02:00"}}
```

Asking to hold an action (filed as a contract request):

```shellsession
$ echo '{"Type":"mod.apphost.register_request","Object":{"Name":"","GrantPermits":[{"Action":"mod.user.see_swarm_action"}],"ContractPermits":[]}}' | astral-query apphost.register -in json -out json
{"Type":"apphost.access_token","Object":{"Identity":"03864ef025fde8fb587d989186ce6a4a186895ee44a926bfc370e2c366597a3f8f","Token":"b9c2e1a3d4f5867a","ExpiresAt":"2036-05-25T12:00:00+02:00"}}
```

Asking for discovery of one service:

```shellsession
$ echo '{"Type":"mod.apphost.register_request","Object":{"Name":"smithd","GrantPermits":[{"Action":"mod.services.service_discovery_action","Constraints":[{"Type":"mod.services.discovery_scope","Object":{"Rules":[{"Services":["inference"],"Nodes":[]}]}}]}],"ContractPermits":[]}}' | astral-query apphost.register -in json -out json
{"Type":"apphost.access_token","Object":{"Identity":"03864ef025fde8fb587d989186ce6a4a186895ee44a926bfc370e2c366597a3f8f","Token":"b9c2e1a3d4f5867a","ExpiresAt":"2036-05-25T12:00:00+02:00"}}
```

Registering without the evaluator, so the new VFS asks no one:

```shellsession
$ echo '{"Type":"mod.apphost.register_request","Object":{"Name":"notes","GrantPermits":[],"ContractPermits":[],"Evaluator":false}}' | astral-query apphost.register -in json -out json
{"Type":"apphost.access_token","Object":{"Identity":"03864ef025fde8fb587d989186ce6a4a186895ee44a926bfc370e2c366597a3f8f","Token":"b9c2e1a3d4f5867a","ExpiresAt":"2036-05-25T12:00:00+02:00"}}
```
