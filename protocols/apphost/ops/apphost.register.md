# apphost.register

Provision a fresh guest identity end-to-end: generate a new keypair, sign and
store an app contract between the new identity and the node, and issue an
access token. Used by apps/agents to bootstrap themselves on first run.
Local-only — a query from the network is answered `origin not allowed: network`.

An app may ask for the actions it needs to hold, and names the record each one
is written into. A node-local grant is revocable by deleting its row and is
worthless off this node. A signed node→app contract is portable evidence
another node verifies, durable until it expires. A permit is the same clause on
either record.

Asking is not receiving: the node's register policy decides what the new
identity actually holds of what the app asked for. The answer carries the token
alone, so an app learns what it was granted by using it.
[`apphost.set_app_register_policy`](apphost.set_app_register_policy.md) selects
the register policy. The policy receives the request as a
[`mod.apphost.app_register_request`](../types/mod.apphost.app_register_request.md).

A session without a token reaches `apphost.register` on an unclaimed and on a
claimed node ([Sessions without a token](../README.md#sessions-without-a-token)).
Until `apphost.set_app_register_policy` names a delegate, the default policy
writes every permit an app asks for,
[`mod.auth.admin_manage_apps_action`](../../auth/types/mod.auth.admin_manage_apps_action.md)
included. Any local program, or any page open in a local browser, that
registers before a delegate is set holds what it asks for.

Every registration also asks for node-local grants of
[`mod.auth.serve_apps_action`](../../auth/types/mod.auth.serve_apps_action.md)
and
[`mod.auth.use_blueprints_action`](../../auth/types/mod.auth.use_blueprints_action.md)
for the new identity, whatever the app asked for. The register policy decides
whether the grants are written, and the default policy writes them, so a new
app can register a handler with
[`apphost.register_handler`](apphost.register_handler.md), advertise itself
with [`services.advertise`](../../services/ops/services.advertise.md), and sync
its blueprints with the node.

What an app asks for at registration grants no service discovery.
`grant_permits` and `contract_permits` carry no constraints, and an
unconstrained [`mod.services.service_discovery_action`](../../services/types/mod.services.service_discovery_action.md)
permit allows nothing. Only a delegated register policy that returns a
constrained permit, or a later [`apphost.grant`](apphost.grant.md), grants it:
the action `mod.services.service_discovery_action` with `-constrained true` and
a bundle holding one
[`mod.services.discovery_scope`](../../services/types/mod.services.discovery_scope.md)
([Who may discover](../../../topics/services.md#who-may-discover)).

## Arguments

* grant_permits (string8) – Actions the app asks to hold as node-local grants,
  comma-separated (e.g. `mod.user.see_swarm_action`). An action name carries no
  comma. Omitted asks for nothing.
* contract_permits (string8) – Actions the app asks to hold in a signed node→app
  contract, comma-separated. An action name carries no comma. Omitted asks for
  nothing.
* name (string8) – The name the app gives itself, shown to a delegated register
  policy. The node does not verify it. Omitted sends an empty name.
* in (string8) – Input format.
* out (string8) – Output format.

An argument the operation does not declare is skipped during binding. A caller
naming one registers successfully and holds nothing it asked for.

## Returned objects

The operation returns one of:
* An `error_message` object reading `origin not allowed: network` if the query
  arrived over a link.
* An `error_message` object reading `registration declined` if the node's
  register policy refuses the registration, cannot decide it, or returns a
  decision the node cannot apply.
* An `error_message` object if any later step failed.
* An `apphost.access_token` object containing the new guest's token.

The operation accepts the query before the register policy decides, so a
refused registration receives `registration declined` rather than a rejection.

## Examples

```shellsession
$ astral-query apphost.register -out json
{"Type":"apphost.access_token","Object":{"Identity":"03864ef025fde8fb587d989186ce6a4a186895ee44a926bfc370e2c366597a3f8f","Token":"b9c2e1a3d4f5867a","ExpiresAt":"2036-05-25T12:00:00+02:00"}}
```

Asking to hold an action as a node-local grant:

```shellsession
$ astral-query apphost.register -grant_permits mod.user.see_swarm_action -out json
{"Type":"apphost.access_token","Object":{"Identity":"03864ef025fde8fb587d989186ce6a4a186895ee44a926bfc370e2c366597a3f8f","Token":"b9c2e1a3d4f5867a","ExpiresAt":"2036-05-25T12:00:00+02:00"}}
```

Naming the app, refused by a delegated register policy:

```shellsession
$ astral-query apphost.register -name notes -out json
{"Type":"error_message","Object":"registration declined"}
```
