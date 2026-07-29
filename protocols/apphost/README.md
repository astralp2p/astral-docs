# apphost

The `apphost` protocol exposes on-device APIs that let local apps access the
astral network via the node — access token issuance, query handler
registration, app contract installation, and object holds.

A local app connects as an anonymous guest or authenticates with an access
token. An anonymous (or expired-token) guest is confined to the `Device` and
`Virtual` [`Zones`](../../core-definitions/zone.md) — the `Network` zone is
stripped from its queries, so it cannot reach other nodes (a query to another
node fails with `route_not_found`). Authenticating retains the `Network` zone
and binds the session, and the queries it makes, to the token's
[`Identity`](../../core-definitions/identity.md).

A guest arriving over the WebSocket endpoint carries its browser origin under
the `origin-web` key in the query's `Extra`; per-origin authorization is left
to the individual operations. An
unauthenticated web guest is further confined to a configured operation
allowlist selected by whether a user has claimed the node: an *unclaimed* node
(no active contract) exposes the setup-ceremony operations; a *claimed* node
exposes only the operations that let a fresh guest obtain an identity. IPC
guests and token-authenticated guests are not restricted by the allowlist. Each
query from a token-less session is tagged as anonymous so an operation can
distinguish an anonymous caller from the node's own identity, which a missing
caller otherwise resolves to.
