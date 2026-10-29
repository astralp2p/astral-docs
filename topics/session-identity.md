# Session Identity

A local program needs an authenticated [Identity](../core-definitions/identity.md)
for ordinary queries and handlers. Each operation checks that identity's permits;
a token establishes identity, not permission.

[`apphost.register`](../protocols/apphost/ops/apphost.register.md) creates an app
identity, grants the permits allowed by registration policy, and returns its token.
For a query with an empty caller, the session determines the effective identity:

```text
app token --> app identity ------------------> operation's permit checks
node token -> node identity -----------------> operation's permit checks
no token ---> allowlist --> node identity ----> operation's permit checks
                  |
                  +-- absent op ------------> error_msg{denied}
```

The [IPC handshake](astral-ipc.md#session-handshake) and
[WebSocket transport](ws-transport.md) define authentication and caller handling.

## What a session without a token reaches

By default, astrald admits only setup, registration and `.spec` queries without
a token. `.spec` lists the node's operations and changes nothing.
The node's claim state selects the
[apphost allowlist](../protocols/apphost/README.md#sessions-without-a-token):

| Node state | Allowed operations |
|------------|--------------------|
| claimed | [`user.info`](../protocols/user/ops/user.info.md), [`apphost.register`](../protocols/apphost/ops/apphost.register.md), `.spec` |
| unclaimed | the claimed list plus [`user.derive_identity`](../protocols/user/ops/user.derive_identity.md), [`user.bootstrap`](../protocols/user/ops/user.bootstrap.md), [`user.join`](../protocols/user/ops/user.join.md) |

apphost refuses other operations with `error_msg{denied}` before routing.
It also strips the network [Zone](../core-definitions/zone.md), preventing access
to other nodes. [Node Setup](node-setup.md) describes the claim operations.

These `apphost.yaml` settings control admission:

| Setting | Default | Effect |
|---------|---------|--------|
| `allow_anonymous` | `true` | `false` refuses all queries without a token, including setup and registration. |
| `anonymous_allowlist` | the lists above | Replaces either the `unclaimed` or `claimed` list. A replacing list admits `.spec` only if it names `.spec`. |
| `trusted_web_sources` | one test origin | On an unclaimed node, a token-less WebSocket session with an `Origin` header requires a listed origin. Each origin also supplies registration permit requests. |

A WebSocket session without an `Origin` header follows the IPC admission rules.

## The node's token

A `tokens:` entry mapping a token to `localnode` authenticates as the node.
It supports [node setup](node-setup.md#who-may-set-up-a-node), but
[`services.advertise`](../protocols/services/ops/services.advertise.md) answers
that identity `not permitted`. A service provider uses its app token and needs the advertising
permit.

## Choosing a session

| Purpose | Session |
|---------|---------|
| Claim a node | No token, subject to the setup rules, or the node's token. |
| Obtain an app identity | No token: `apphost.register`. |
| Run app queries, handlers, or [services](services.md) | The app's token, with the required permits. |
