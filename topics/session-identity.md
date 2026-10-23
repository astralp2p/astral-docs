# Session Identity

* Every [`Query`](../core-definitions/query.md) a [`Node`](../core-definitions/node.md) runs has a
  caller [`Identity`](../core-definitions/identity.md), and an [`Op`](../core-definitions/op.md)
  authorizes that `Identity`. An `Identity` is the first thing a local program needs: without one
  it reaches almost nothing.
* A local program obtains its `Identity` with
  [`apphost.register`](../protocols/apphost/ops/apphost.register.md). The `Node` mints an
  [`App`](../core-definitions/app.md) `Identity`, grants it the permits the register policy allows,
  and returns an access token. A session authenticated with that token speaks as the `App`; a
  `Query` it sends with a zero caller runs as the `App`, never as the `Node`.
* A session without a token has no `Identity` of its own. The `Node` routes its zero caller as the
  `Node` `Identity`, and an `Op` cannot tell such a `Query` from the `Node`'s own. apphost therefore
  refuses every `Op` of such a session with `error_msg{denied}` before routing it, except the few of
  the `anonymous_allowlist`.

## What a session without a token reaches

The defaults below are those of astrald. The rule, both lists and the WebSocket case are specified
in [apphost, Sessions without a token](../protocols/apphost/README.md#sessions-without-a-token).

| Node state | Ops | Purpose |
|------------|-----|---------|
| claimed | [`user.info`](../protocols/user/ops/user.info.md), [`apphost.register`](../protocols/apphost/ops/apphost.register.md) | learn the claim state; obtain an `Identity` |
| unclaimed | the claimed list, plus [`user.derive_identity`](../protocols/user/ops/user.derive_identity.md), [`user.bootstrap`](../protocols/user/ops/user.bootstrap.md), [`user.join`](../protocols/user/ops/user.join.md), `crypto.list_keys` | claim the node — see [Node Setup](node-setup.md) |

* `apphost.register` is on both lists: it is how a program without an `Identity` obtains one.
* A session without a token never reaches another `Node`: its network
  [`Zone`](../core-definitions/zone.md) is stripped.

Three `apphost.yaml` settings change this surface:

| Setting | Default | Effect |
|---------|---------|--------|
| `allow_anonymous` | `true` | `false` refuses every `Query` of a session without a token, both lists included. |
| `anonymous_allowlist` | the table above | replaces the `unclaimed` or `claimed` list. |
| `trusted_web_sources` | one test origin | while the node is unclaimed, a WebSocket session without a token is refused every `Op` unless its browser origin is listed. Each origin also names the permits an `App` registered from it is entitled to. |

## The node's token

* `tokens:` in `apphost.yaml` can map a token to `localnode`. A session authenticated with it speaks
  as the `Node` `Identity`. The step-by-step flow of
  [Node Setup](node-setup.md#who-may-set-up-a-node) runs with it.
* It is not an `App` `Identity`. [`services.advertise`](../protocols/services/ops/services.advertise.md)
  rejects the `Node` `Identity` as its caller, so a provider started with the node's token cannot
  advertise.

## Choosing a session

| The program | Session |
|-------------|---------|
| claims a node | without a token, or with the node's token — [Node Setup](node-setup.md) |
| obtains its `Identity` | without a token: `apphost.register` |
| does anything else — queries, handlers, [`Services`](services.md) | the token `apphost.register` returned |

The session handshake and caller rules are wire-level details of [Astral IPC](astral-ipc.md#session-handshake)
and the [WebSocket Transport](ws-transport.md).
