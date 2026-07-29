# apphost.register_handler

Register an IPC query handler for the caller's identity. The host forwards
inbound queries targeting the caller to the given endpoint. Local-only —
queries from the network are rejected.

The operation expects an IPC dial endpoint, so it is not usable over the
WebSocket transport; a WebSocket client registers through the
register-service flow in the
[WebSocket transport](../../../topics/ws-transport.md) topic.

## Arguments

* endpoint (string8, required) – IPC endpoint in `<proto>:<address>` form (e.g. `tcp:127.0.0.1:9001`, `unix:/tmp/app.sock`).
* token (nonce64, required) – Callback auth token presented to the handler on each dial.

## Returned objects

The operation returns one of:
* An `error_message` object if there was an error.
* An `ack` object if the handler was registered.

## Examples

```shellsession
$ astral-query apphost.register_handler -endpoint tcp:127.0.0.1:9001 -token a3f1c2d4e5b6f708 -out text
#[ack]
```
