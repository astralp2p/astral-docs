# HTTP Transport

HTTP transport provides a way to send [*Queries*](../core-definitions/query.md) via the local [*Node*](../core-definitions/node.md) over the *Astral Network*. Due to how HTTP works, *Queries* sent over HTTP are limited to a simple request-response flow. [*Ops*](../core-definitions/op.md) that require a more interactive dialog should be routed through the native [*Astral IPC*](astral-ipc.md) protocol or [WebSocket Transport](ws-transport.md).

* The default HTTP endpoint for all calls is `http://localhost:8624/`.
* HTTP requests are authenticated using an *Auth Token* provided as a bearer 
  token in the HTTP Authorization header.
* The [*Query String*](../core-definitions/query-string.md) is passed as the path in the HTTP request.
* The *Target* of the *Query* is set via the "X-Astral-Target" request 
  header containing the [*Identity*](../core-definitions/identity.md) of the target node (pubkey hex string).
* The default *Target* is the local *Node*.
* A *Query* to the local *Node* passes the apphost gate: its *Op* must be on
  the list of the node's state in `gate.states`. A refused *Query* answers
  status 403 ([apphost, Gate](../protocols/apphost/README.md#gate)).
* The request headers should contain "Accept: application/json" and
  "Content-Type: application/json".
* API calls respond with JSON lines containing [*Objects*](../core-definitions/object.md) using the
  [*JSON Encoding*](json-encoding.md)
* HTTP response headers will contain "X-Astral-Guest-Identity" with the 
  *Identity* authenticated via the *Auth Token*.
* HTTP response headers will contain "X-Astral-Host-Identity" with the 
  *Identity* of the host *Node*.
* `GET /.objects/<object-id>` returns the raw bytes of the object. It is 
  authenticated with the bearer token and, additionally, subject to a per-object 
  read authorization; a failed authorization returns 403.
* `/.ws` is reserved for the WebSocket upgrade (see 
  [WebSocket Transport](ws-transport.md)).
* The permissive CORS headers apply to the query and object endpoints, not to 
  `/.ws`.