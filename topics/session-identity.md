# Session Identity

A local program needs an authenticated [Identity](../core-definitions/identity.md)
for ordinary queries and handlers. Each operation checks that identity's permits;
a token establishes identity, not permission.

[`apphost.register`](../protocols/apphost/ops/apphost.register.md) creates an app
identity, grants the permits allowed by the
[registration policy](node-policies.md), and returns its token.
For a query with an empty caller, the session determines the effective identity:

```text
app token --> gate --> app identity ---------> operation's permit checks
node token -> gate --> node identity --------> operation's permit checks
no token ---> gate --> node identity --------> operation's permit checks
               |
               +-- op not listed ----------> error_msg{denied}
```

The [IPC handshake](astral-ipc.md#session-handshake) and
[WebSocket transport](ws-transport.md) define authentication and caller handling.

## What the gate admits

The [apphost gate](../protocols/apphost/README.md#gate) admits every query of an
IPC, WebSocket or HTTP session before routing. The node's state selects the
list a query to the node must appear on
([Node states](../protocols/apphost/README.md#node-states)). A session without
a token also needs the operation on `gate.tokenless`. By default:

| Node state | Without a token | With a token |
|------------|-----------------|--------------|
| `fresh` | `.spec`, [`apphost.register_manager`](../protocols/apphost/ops/apphost.register_manager.md), [`user.info`](../protocols/user/ops/user.info.md) | the same |
| `unclaimed` | `.spec`, `user.info`, [`apphost.register`](../protocols/apphost/ops/apphost.register.md) | `.spec`, `user.info`, [`user.derive_identity`](../protocols/user/ops/user.derive_identity.md), [`user.bootstrap`](../protocols/user/ops/user.bootstrap.md), [`user.join`](../protocols/user/ops/user.join.md), `apphost.register` |
| `claimed` | `.spec`, `apphost.register`, `apphost.register_manager`, `user.info` | every operation |

apphost refuses other queries to the node with `error_msg{denied}` before
routing. A session without a token reaches no other identity. A query with a
token to another identity passes the gate. apphost also strips the network
[Zone](../core-definitions/zone.md) from a session without a token, preventing
access to other nodes. [Node Setup](node-setup.md) describes the claim
operations.

These `apphost.yaml` settings control admission:

| Setting | Default | Effect |
|---------|---------|--------|
| `gate.tokenless` | `.spec`, `apphost.register`, `apphost.register_manager`, `user.info` | The operations a session without a token may call. |
| `gate.states.fresh`, `gate.states.unclaimed`, `gate.states.claimed` | the lists above | The operations a query to the node may call in each state. |

A key the file supplies replaces that list, and an omitted key keeps its
default. The entry `*` matches every operation. `allow_anonymous` and
`anonymous_allowlist` are removed, and a file that names either stops the node
at startup.

A WebSocket session follows the IPC admission rules, whatever its `Origin`
header. Any page open in a local browser reaches what a session without a token
reaches.

## The node's token

A `tokens:` entry mapping a token to `localnode` authenticates as the node.
It obeys the state lists of the gate as every other token does. It supports
[node setup](user-and-swarm.md#who-may-claim) on an `unclaimed` node, but
[`services.advertise`](../protocols/services/ops/services.advertise.md) answers
that identity `not permitted`. A service provider uses its app token and needs the advertising
permit.

## Choosing a session

| Purpose | Session |
|---------|---------|
| Appoint the manager of a `fresh` node | No token, or any token: `apphost.register_manager`. |
| Claim a node | The manager's App token, or the node's token, on an `unclaimed` node. |
| Obtain an app identity | No token: `apphost.register`, subject to the app register policy. |
| Run app queries, handlers, or [services](services.md) | The app's token, with the required permits. |
