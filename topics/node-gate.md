# Node Gate

The gate decides which operations of a node are open at all, by whether the
caller has a token and what state the node is in. Everything past the gate is
authorization: each operation checks the caller's actions itself
([auth](../protocols/auth/README.md)). [Node Setup](node-setup.md) explains
the node states and the manager this page relies on.

## The gate

apphost passes every query of an IPC, WebSocket or HTTP session through the
gate before routing it ([apphost, Gate](../protocols/apphost/README.md#gate)).
`gate` in `apphost.yaml` holds two kinds of list:

* `gate.tokenless` – the operations a session without a token may call. Such a
  session reaches the node only, never an app: a query without a token runs
  with the node's own authority, and an app must never receive a query nobody
  authenticated.
* `gate.states.fresh`, `gate.states.unclaimed`, `gate.states.claimed` – the
  operations any query to the node may call in that state, with a token or
  without.

A session without a token needs the operation on both lists. A query with a
token to another identity, such as an app, passes the gate. An entry is an
operation path, or `*`, which matches every operation; no other entry is a
pattern. The gate refuses an IPC or WebSocket query with `error_msg{denied}`
and an HTTP query with status `403`. An operation the gate admits still checks
the caller's authorization itself.

What a session reaches under the default lists:

| State | Without a token | With a token, the node's token included |
|-------|-----------------|-----------------------------------------|
| `fresh` | `.spec`, [`sys.register_manager`](../protocols/sys/ops/sys.register_manager.md), [`user.info`](../protocols/user/ops/user.info.md) | the same |
| `unclaimed` | `.spec`, `user.info`, [`apphost.register`](../protocols/apphost/ops/apphost.register.md) | `.spec`, `user.info`, [`user.derive_identity`](../protocols/user/ops/user.derive_identity.md), [`user.bootstrap`](../protocols/user/ops/user.bootstrap.md), [`user.join`](../protocols/user/ops/user.join.md), `apphost.register`, [`apphost.bind`](../protocols/apphost/ops/apphost.bind.md), [`apphost.register_handler`](../protocols/apphost/ops/apphost.register_handler.md), [`apphost.cancel`](../protocols/apphost/ops/apphost.cancel.md), [`nodes.resolve_endpoints`](../protocols/nodes/ops/nodes.resolve_endpoints.md) |
| `claimed` | `.spec`, `apphost.register`, `sys.register_manager`, `user.info` | every operation |

A list the file supplies replaces the default list, and an omitted list keeps
its default.

## Distribution and test configuration

The defaults are the distribution configuration. A node needs no
`apphost.yaml` for it:

```yaml
# apphost.yaml
gate:
  tokenless: [.spec, apphost.register, sys.register_manager, user.info]
  states:
    fresh: [.spec, sys.register_manager, user.info]
    unclaimed: [.spec, user.info, user.derive_identity, user.bootstrap, user.join, apphost.register,
                apphost.bind, apphost.register_handler, apphost.cancel, nodes.resolve_endpoints]
    claimed: ["*"]
```

The only way forward from `fresh` is the manager appointment. The claim
operations need a token, which the manager holds after its appointment.

A test node claims without a manager. The astrald end-to-end tests run every
node with this gate:

```yaml
# apphost.yaml
gate:
  tokenless: [apphost.register, user.info, user.derive_identity, user.bootstrap, user.join]
  states:
    fresh: ["*"]
```

* A session without a token calls `user.bootstrap` or `user.join` on a `fresh`
  node and claims it in one query. `sys.register_manager` is not on the
  `tokenless` list, so a test that appoints a manager calls it with the node's
  token.
* The `unclaimed` and `claimed` lists keep their defaults.
* This configuration does not belong on a node a user owns: any local
  program claims a fresh node without a token.
