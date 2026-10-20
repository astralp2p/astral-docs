# mod.gateway.ping

A gateway connection-control frame that keeps an idle connection alive. Pings
flow only on an idle connection between a registered node and its gateway, from
the moment the connection presents its nonce until the handoff; see
[Idle connections](../README.md#idle-connections). A frame with `Pong` set to
false is a keepalive request, and a frame with `Pong` set to true is the reply
to such a request.

Either side sends a request once 30 seconds pass without a received frame and
without a request of its own, and answers every request with a reply. A side
closes the connection after 60 seconds without receiving any frame. A missing
reply alone does not close the connection: any received frame keeps it open.

## Fields

* Pong (bool) – False marks a keepalive request; true marks the reply to a request.

## Example

```json
{
  "Type": "mod.gateway.ping",
  "Object": {
    "Pong": false
  }
}
```
