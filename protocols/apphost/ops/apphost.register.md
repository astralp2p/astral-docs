# apphost.register

Provision a fresh guest identity end-to-end: generate a new keypair, sign and
store an app contract between the new identity and the node, and issue an
access token. Used by apps/agents to bootstrap themselves on first run.
Local-only — a query from the network is answered `origin not allowed: network`.

After accepting the query, the operation reads one
[`mod.apphost.register_request`](../types/mod.apphost.register_request.md) from
the channel. The request carries the name the app gives itself and the permits
it asks to hold, with their constraints, and names the record each one is
written into. A node-local grant is revocable by deleting its row and is
worthless off this node ([Grants](../README.md#grants)). A signed node→app
contract is portable evidence another node verifies, durable until it expires.
A permit is the same clause on either record.

The operation checks every permit of both lists before the register policy is
asked ([Grants](../README.md#grants)). A permit that fails the check refuses
the registration with an `error_message` reading `invalid permit: …`, and no
identity is minted.

Asking is not receiving: the node's register policy decides which of the
asked-for permits the new identity holds. The answer carries the token
alone, so an app learns what it was granted by using it.
[`apphost.set_app_register_policy`](apphost.set_app_register_policy.md) selects
the register policy. The policy receives the request as a
[`mod.apphost.app_register_request`](../types/mod.apphost.app_register_request.md),
which adds the caller's web origin.

The default gate admits `apphost.register`, with a token or without, on an
`unclaimed` and on a `claimed` node, and refuses it on a `fresh` node
([Gate](../README.md#gate)). A `fresh` node appoints a manager first with
[`sys.register_manager`](../../sys/ops/sys.register_manager.md).

A stored delegate decides first. Without one, `policies.app_register` in
`apphost.yaml` decides ([Policies](../README.md#policies)). Its default,
`reject_all`, refuses every registration with `registration declined`. Under
`accept_all`, the policy writes every permit an app asks for,
[`mod.auth.admin_manage_apps_action`](../../auth/types/mod.auth.admin_manage_apps_action.md)
included, and any local program, or any page open in a local browser, that
registers holds what it asks for.

Every registration also asks for node-local grants of
[`mod.auth.serve_apps_action`](../../auth/types/mod.auth.serve_apps_action.md)
and
[`mod.auth.use_blueprints_action`](../../auth/types/mod.auth.use_blueprints_action.md)
for the new identity, whatever the app asked for. The register policy decides
whether the grants are written, and `accept_all` writes them, so a new
app can register a handler with
[`apphost.register_handler`](apphost.register_handler.md), advertise itself
with [`services.advertise`](../../services/ops/services.advertise.md), and sync
its blueprints with the node. Every grant written at registration expires with
the access token.

An app can ask for service discovery at registration. A
[`mod.services.service_discovery_action`](../../services/types/mod.services.service_discovery_action.md)
permit in `GrantPermits` needs constraints holding exactly one
[`mod.services.discovery_scope`](../../services/types/mod.services.discovery_scope.md)
that names a service; `accept_all` writes it as sent. An unconstrained
discovery permit is refused before the policy is asked
([Who may discover](../../../topics/services.md#who-may-discover)).

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
  `invalid permit: missing action`, if a permit fails the check. The policy is
  not asked.
* An `error_message` object reading `registration declined` if the node's
  register policy refuses the registration, cannot decide it, or returns a
  decision the node cannot apply.
* An `error_message` object if any later step failed.
* An `apphost.access_token` object containing the new guest's token.

The operation accepts the query before the register policy decides, so a
refused registration receives `registration declined` rather than a rejection.

## Examples

```shellsession
$ echo '{"Type":"mod.apphost.register_request","Object":{"Name":"","GrantPermits":[],"ContractPermits":[]}}' | astral-query apphost.register -in json -out json
{"Type":"apphost.access_token","Object":{"Identity":"03864ef025fde8fb587d989186ce6a4a186895ee44a926bfc370e2c366597a3f8f","Token":"b9c2e1a3d4f5867a","ExpiresAt":"2036-05-25T12:00:00+02:00"}}
```

Asking to hold an action as a node-local grant:

```shellsession
$ echo '{"Type":"mod.apphost.register_request","Object":{"Name":"","GrantPermits":[{"Action":"mod.user.see_swarm_action"}],"ContractPermits":[]}}' | astral-query apphost.register -in json -out json
{"Type":"apphost.access_token","Object":{"Identity":"03864ef025fde8fb587d989186ce6a4a186895ee44a926bfc370e2c366597a3f8f","Token":"b9c2e1a3d4f5867a","ExpiresAt":"2036-05-25T12:00:00+02:00"}}
```

Asking for discovery of one service:

```shellsession
$ echo '{"Type":"mod.apphost.register_request","Object":{"Name":"smithd","GrantPermits":[{"Action":"mod.services.service_discovery_action","Constraints":[{"Type":"mod.services.discovery_scope","Object":{"Rules":[{"Services":["inference"],"Nodes":[]}]}}]}],"ContractPermits":[]}}' | astral-query apphost.register -in json -out json
{"Type":"apphost.access_token","Object":{"Identity":"03864ef025fde8fb587d989186ce6a4a186895ee44a926bfc370e2c366597a3f8f","Token":"b9c2e1a3d4f5867a","ExpiresAt":"2036-05-25T12:00:00+02:00"}}
```

Naming the app, refused by a delegated register policy or by `reject_all`:

```shellsession
$ echo '{"Type":"mod.apphost.register_request","Object":{"Name":"notes","GrantPermits":[],"ContractPermits":[]}}' | astral-query apphost.register -in json -out json
{"Type":"error_message","Object":"registration declined"}
```
