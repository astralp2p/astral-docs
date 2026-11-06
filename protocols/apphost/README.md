# apphost

The `apphost` protocol exposes on-device APIs that let local apps access the
astral network via the node — access token issuance, query handler
registration, app contract signing, node-local grant administration, grant
requests, and object holds.

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

## Grants

A grant is a node-local record that an identity may perform an action on this
node. A grant is recorded, not signed: it authorizes on this node and travels
nowhere. [`apphost.register`](ops/apphost.register.md),
[`apphost.grant`](ops/apphost.grant.md) and
[`apphost.request_grant`](ops/apphost.request_grant.md) write grants.

Grants accumulate. A write adds its grants beside the identity's other grants
and never removes a grant. An identity can hold several grants for one action,
for example one `mod.services.service_discovery_action` grant per service. A
permit identical to a held one, with the same action and constraints, is stored
once: writing it again sets that grant's expiry to the new value, shorter or
longer.

Authorization allows an action when any unexpired grant the identity holds for
that action allows it.

Each grant has an ID. [`apphost.list_grants`](ops/apphost.list_grants.md)
reports grants as [`mod.apphost.grant`](types/mod.apphost.grant.md) objects.
[`apphost.revoke`](ops/apphost.revoke.md) withdraws one grant by `id`, or every
grant of the identity for one `action`. Narrowing a grant takes two steps:
grant the narrow permit, then revoke the wide grant by `id`. The identity holds
access throughout.

`apphost.register`, `apphost.grant` and `apphost.request_grant` check every
permit they receive before any policy is asked and before any grant is written.
A permit that fails the check refuses the whole call with an `error_message`
reading `invalid permit: <action>: <detail>`, and nothing is written. The check
refuses:

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
[`mod.auth.sudo_action`](../auth/types/mod.auth.sudo_action.md) and
[`mod.shell.shell_action`](../shell/types/mod.shell.shell_action.md) ignore
constraints, so a constrained grant of either allows the action in full. Every
other action that does not evaluate constraints refuses a constrained permit
when it authorizes ([auth](../auth/README.md)): such a grant passes the check,
is written, and allows nothing.

[`apphost.set_grant_request_policy`](ops/apphost.set_grant_request_policy.md)
selects how the node decides `apphost.request_grant`: `accept_all`,
`reject_all`, or a delegate. Unset selects `accept_all`.

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
| `states.unclaimed` | `.spec`, `user.info`, `user.derive_identity`, `user.bootstrap`, `user.join`, `apphost.register`, `apphost.bind`, `apphost.register_handler`, `apphost.cancel` |
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
claim. The manager answers the policies delegated to it only through its handler,
an invitation from the owner's other device among them. The `tokenless` list holds
none of the three.

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
                apphost.bind, apphost.register_handler, apphost.cancel]
    claimed: ["*"]
policies:
  app_register: reject_all
```

## Policies

`policies.app_register` in `apphost.yaml` holds the config value of the app
register policy: `accept_all`, `reject_all`, or a delegate mapping. The default
is `reject_all`. A delegate stored with
[`apphost.set_app_register_policy`](ops/apphost.set_app_register_policy.md)
outranks the config value.
[Node Policies](../../topics/node-policies.md#config-values) describes the
values.
