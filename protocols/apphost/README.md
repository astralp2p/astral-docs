# apphost

The `apphost` protocol exposes on-device APIs that let local apps access the
astral network via the node — access token issuance, query handler
registration, app contract signing, node-local grant administration, and object
holds.

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

## Sessions without a token

A query from a session without a token carries a zero caller, and the node
routes a zero caller as its own identity. An operation cannot tell such a query
from the node's own. apphost therefore confines every session without a token,
IPC and WebSocket alike, to the operations of `anonymous_allowlist` in the
apphost configuration. The node's claim state selects the list: `unclaimed`
while the node has no active contract, `claimed` afterwards. apphost refuses an
operation absent from the active list with `error_msg{denied}` before routing
it.

| List | Default operations |
|------|--------------------|
| `unclaimed` | `user.info`, `user.derive_identity`, `user.bootstrap`, `user.join`, `apphost.register`, `.spec` |
| `claimed` | `user.info`, `apphost.register`, `.spec` |

* While the node is unclaimed, a WebSocket session without a token is refused
  every operation unless its browser origin is a key of `trusted_web_sources`.
  A WebSocket client that sends no `Origin` header is confined as an IPC
  session is.
* `.spec` lists the node's operations and changes nothing. A session without a
  token learns the operations before it holds a token.
* `allow_anonymous: false` refuses every query of a session without a token.
* A session with a token is not confined by the lists. apphost routes a query
  with a zero caller from such a session as the session's identity.
* `apphost.yaml` replaces either list. A replacing list admits `.spec` only if
  it names `.spec`:

```yaml
anonymous_allowlist:
  unclaimed: [user.info, user.derive_identity, user.bootstrap, user.join, apphost.register, .spec]
  claimed: [user.info, apphost.register, .spec]
```
