# apphost.register

Provision a fresh guest identity end-to-end: generate a new keypair, sign and
store an app contract between the new identity and the node, and issue an
access token. Used by apps/agents to bootstrap themselves on first run.

An app may ask for the actions it needs to hold, and names the record each one
is written into. A node-local grant is revocable by deleting its row and is
worthless off this node. A signed node→app contract is portable evidence
another node verifies, durable until it expires. A permit is the same clause on
either record.

Asking is not receiving: the node joins what the caller's origin is entitled to
with what the app asked for, and its register policy decides what the new
identity actually holds. The answer carries the token alone, so an app learns
what it was granted by using it.

The permits a trusted web origin is entitled to join the contract request, not
the grant request.

Every registration also asks for a node-local grant of
[`mod.auth.serve_apps_action`](../../auth/types/mod.auth.serve_apps_action.md)
for the new identity, whatever the app asked for. The register policy decides
whether the grant is written, and the default policy writes it, so a new app
can register a handler with
[`apphost.register_handler`](apphost.register_handler.md) and advertise itself
with [`services.advertise`](../../services/ops/services.advertise.md).

## Arguments

* grant_permits (string8) – Actions the app asks to hold as node-local grants,
  comma-separated (e.g. `mod.user.see_swarm_action`). An action name carries no
  comma. Omitted asks for nothing.
* contract_permits (string8) – Actions the app asks to hold in a signed node→app
  contract, comma-separated. An action name carries no comma. Omitted asks for
  nothing.
* in (string8) – Input format.
* out (string8) – Output format.

An argument the operation does not declare is skipped during binding. A caller
naming one registers successfully and holds nothing it asked for.

## Returned objects

The operation returns one of:
* An `error_message` object if any step failed.
* An `apphost.access_token` object containing the new guest's token.

The operation is rejected outright if the node's register policy refuses the
registration.

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
