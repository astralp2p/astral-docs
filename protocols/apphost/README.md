# apphost

The `apphost` protocol exposes on-device APIs that let local apps access the
astral network via the node — access token issuance, query handler
registration, app contract signing, contract requests, and object holds.

A local app connects as an anonymous guest or authenticates with an access
token. An anonymous (or expired-token) guest is confined to the `Device` and
`Virtual` [`Zones`](../../core-definitions/zone.md) — the `Network` zone is
stripped from its queries, so it cannot reach other nodes (a query to another
node fails with `route_not_found`). Authenticating retains the `Network` zone
and binds the session, and the queries it makes, to the token's
[`Identity`](../../core-definitions/identity.md).

A guest arriving over the WebSocket endpoint carries its browser origin under
the `origin-web` key in the query's `Extra`; per-origin authorization is left
to the individual operations.

## Permits

An app holds no node-local grant. Every action an app takes, on its own node or
another, is authorized by its contract chain: a contract from its host that
carries out an Approval, back to the user
([user, SwarmState](../user/README.md#swarmstate-entries)). The node keeps no
grant table; a node upgraded from a release that kept one drops
`apphost__grants` at start.

`apphost.register` and `apphost.request_contract` check every permit they
receive before anything is filed. A permit that fails the check refuses the
whole call with an `error_message` reading `invalid permit: <action>:
<detail>`, and nothing is filed. The check refuses:

* a permit without an action, as `invalid permit: missing action`;
* an action the node does not know, as `invalid permit: <action>: unknown
  action`;
* an action that allows nothing unconstrained, sent without constraints, as
  `invalid permit: <action>: requires constraints`;
* a `mod.services.service_discovery_action` permit whose constraints do not
  hold exactly one `mod.services.discovery_scope`, as `invalid permit:
  mod.services.service_discovery_action: constraints must hold exactly one
  discovery scope`, or whose scope names no service, as `invalid permit:
  mod.services.service_discovery_action: discovery scope names no service`.

Constraints on an action that does not evaluate them have no effect.
[`mod.shell.shell_action`](../shell/types/mod.shell.shell_action.md) ignores
constraints, so a constrained permit of it allows the action in full. Every
other action that does not evaluate constraints refuses a constrained permit
when it authorizes ([auth](../auth/README.md)).

## Contract requests

A contract request asks the swarm for permits for an app, in place of a grant.
[`apphost.request_contract`](ops/apphost.request_contract.md) files a
[`mod.user.signed_contract_request`](../user/types/mod.user.signed_contract_request.md)
into SwarmState ([SwarmState entries](../user/README.md#swarmstate-entries)).
The app's host files and signs the request, and the request names the app.

A Privileged node answers the request with an approval or a decline. The host
carries out an approval of a request it filed: it signs a contract from itself
to the identity the request names, with exactly the request's permits and the
approval's entry ID as `ApprovalID`. The host never signs a contract on an
approval of a request another node filed, and never for another identity. An
app moved to another node files a new request there.

Registration stays local: [`apphost.register`](ops/apphost.register.md) issues
the identity and the access token at once, and files one contract request for
`mod.auth.serve_apps_action`, `mod.auth.use_blueprints_action` and the permits
the registration asks. Only the permits wait in SwarmState. The host checks
SwarmState for answers every 5 seconds, and indexes the contract it signs.

## Node states and the manager

The node's state (`fresh`, `unclaimed` or `claimed`) and its manager belong to
the [`sys`](../sys/README.md) protocol: [Node states](../sys/README.md#node-states)
and [Manager](../sys/README.md#manager). The gate reads the state from `sys`.

## Gate

apphost passes every query of an IPC, WebSocket or HTTP session through the
gate before routing it. A query to the node is a query whose target is zero or
the node's identity. The gate applies these rules:

* A session without a token sends queries to the node only, and only the
  operations `gate.tokenless` lists.
* Every query to the node, with a token or without, names an operation that the
  list of the node's state in `gate.states` holds.
* A query with a token to another identity passes the gate.
* An entry is an operation path, or `*`. The entry `*` matches every
  operation. No other entry is a pattern: `user.*` matches no operation.

The gate refuses an IPC or WebSocket query with `error_msg{denied}` and an HTTP
query with status `403`. The node's token obeys the state lists as every other
token does. A query the gate admits is then authorized by its operation.

A query from a session without a token carries a zero caller, and the node
routes a zero caller as its own identity. An operation cannot tell such a query
from the node's own. apphost routes a query with a zero caller from a session
with a token as the session's identity.

| List | Default operations |
|------|--------------------|
| `tokenless` | `.spec`, `apphost.register`, `sys.register_manager`, `user.info` |
| `states.fresh` | `.spec`, `sys.register_manager`, `user.info` |
| `states.unclaimed` | `.spec`, `user.info`, `user.derive_identity`, `user.bootstrap`, `user.join`, `apphost.register`, `apphost.bind`, `apphost.register_handler`, `apphost.cancel`, `nodes.resolve_endpoints` |
| `states.claimed` | `*` |

Under the default lists, a session without a token reaches `.spec`,
`sys.register_manager` and `user.info` on a `fresh` node, `.spec`,
`user.info` and `apphost.register` on an `unclaimed` node, and the four
`tokenless` operations on a `claimed` node. `.spec` lists the node's
operations and changes nothing, so a client discovers what it may call before
it holds a token. A node whose `apphost.yaml` supplies its own lists adds
`.spec` to them itself.

The `unclaimed` list holds [`apphost.bind`](ops/apphost.bind.md),
[`apphost.register_handler`](ops/apphost.register_handler.md) and
[`apphost.cancel`](ops/apphost.cancel.md), so an app with a token serves before the
claim. The `tokenless` list holds none of the three.

The `unclaimed` list holds
[`nodes.resolve_endpoints`](../nodes/ops/nodes.resolve_endpoints.md), so the
manager reads the node's endpoints before the claim, and another device claims
the node by address. The operation requires
[`mod.auth.admin_network_action`](../auth/types/mod.auth.admin_network_action.md)
itself. The `tokenless` list does not hold it.

* A WebSocket session is gated as an IPC session is, whatever its `Origin`
  header. Any page open in a local browser reaches what the gate admits a
  session without a token.
* A key `apphost.yaml` supplies replaces that list. An omitted key keeps its
  default.

The default configuration:

```yaml
gate:
  tokenless: [.spec, apphost.register, sys.register_manager, user.info]
  states:
    fresh: [.spec, sys.register_manager, user.info]
    unclaimed: [.spec, user.info, user.derive_identity, user.bootstrap, user.join, apphost.register,
                apphost.bind, apphost.register_handler, apphost.cancel, nodes.resolve_endpoints]
    claimed: ["*"]
```
