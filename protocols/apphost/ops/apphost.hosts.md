# apphost.hosts

List the nodes that host an app. A host is the subject of an active
[`mod.nodes.relay_for_action`](../../nodes/types/mod.nodes.relay_for_action.md)
contract the app issued; this node is listed when it hosts the app.

The caller must hold
[`mod.user.see_swarm_action`](../../user/types/mod.user.see_swarm_action.md).
The query is rejected with code `1` when the caller is not authorized. The
operation also rejects a query that arrived over a
[`Link`](../../../core-definitions/link.md), whatever the caller holds.

A sibling node's app is known once its relay contract reached this node: at the
first link, at the app's registration, or when the app runs swarm discovery.

## Arguments

* app (string8, required) – The app whose hosts are listed, given as a hex
  public key or a name resolved via the directory.

## Returned objects

The operation returns one of:
* An `error_message` object if the relay contracts could not be read.
* An `identity` object for each host, each host listed once.
* An `eos` object terminating the stream.

An `app` that does not resolve, or an app with no known host, receives an `eos`
object alone.

## Examples

```shellsession
$ astral-query apphost.hosts -app chat -out json
{"Type":"identity","Object":"0282fee8775757cdd8fda8b220195f5b8611312cd145c5a1a3aa55df210e779b2c"}
{"Type":"identity","Object":"03a1c4e2b7f9d0581e6a3c2b4d5f6e7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f"}
{"Type":"eos","Object":null}
```
