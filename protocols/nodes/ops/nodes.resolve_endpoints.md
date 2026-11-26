# nodes.resolve_endpoints

Resolve all known endpoints for an identity by querying every registered endpoint resolver.

The caller must hold
[`mod.auth.admin_network_action`](../../auth/types/mod.auth.admin_network_action.md),
or be a current member of this node's local swarm asking about a current member
or about this node. A caller that neither holds the action nor is a member gets
an `error_message` reading `not permitted` before the identity is resolved. A
member that asks about a node outside the swarm gets `not permitted` after the
identity is resolved.

## Swarm only

The endpoints a node advertises, and the endpoints it stores for other nodes,
are private to its user's swarm. The holders of
`mod.auth.admin_network_action` are the user identity, the node itself and a
Privileged member, plus an identity the action is delegated to
([Holders](../../auth/types/mod.auth.admin_network_action.md#holders)). Any
other current member of the swarm reads the endpoints of the members and of
this node, and nothing else: every member links to every other member, and
endpoints travel only through this operation. Expelled nodes are not members. A node
of another user, a gateway the user never adopted, a hosting node and any other
linked peer outside the swarm receive `not permitted`. A link with such a peer
stores no endpoints on either side: a node pulls endpoints when a link forms
only from a member of its own swarm.
[Node Exposure, Endpoint exchange](../../../topics/node-exposure.md#endpoint-exchange)
lists the operator paths that make a node outside the swarm reachable.

## Arguments

* identity (string8, required) – The identity whose endpoints are resolved, given as a hex public key or a name resolved via the directory.
* out (string) – Output format hint for the channel (e.g. `json`).

## Returned objects

The operation returns a stream of `mod.nodes.endpoint_with_ttl` objects, terminated by `eos`. If `identity` does not resolve the operation answers an `error_message` reading `unknown identity`, and `zero identity` if it resolves to the anonymous identity; if resolver lookup fails internally the operation answers the error.

Each object carries the TTL its resolver assigns, in seconds:

* The node's own identity: a `mod.tcp.endpoint` and a `mod.kcp.endpoint` at
  each local interface address while the module listens, with `604800`
  (7 days) on a public address and `7200` (2 hours) on any other address;
  each [`configEndpoints`](../../tcp/README.md#advertising-a-public-or-forwarded-endpoint) entry of `tcp.yaml`, with
  `604800` (7 days); the `mod.tor.endpoint` of the onion service while tor
  listens, with `7776000` (90 days); and a `mod.gateway.endpoint` for each
  gateway the node uses ([gateway](../../gateway/README.md)).
* Any other identity: each stored row with its remaining TTL. A row that
  [`nodes.add_endpoint`](nodes.add_endpoint.md) wrote starts at `7776000`
  (90 days); a row stored from a swarm member's answer starts at the TTL of
  that answer, except where
  [Withdrawn endpoints](../README.md#withdrawn-endpoints) keeps a later expiry. A verified [`nearby`](../../nearby/README.md) peer adds a
  `mod.tcp.endpoint` and a `mod.kcp.endpoint` at its source IP on the ports
  its status carries, `1791` and `1792` when it carries none, with the
  remaining life of its cache entry, at most `300`.

## Examples

On a node whose tcp and kcp listen on `192.168.1.10` and whose onion service
is up, a caller that holds the action resolves the node's own identity:

```shellsession
$ astral-query nodes.resolve_endpoints -identity 037f990e61acee8a7697966afd29dd88f3b1f8a7b14d625c4f8742bd952003a590 -out json
{"Type":"mod.nodes.endpoint_with_ttl","Object":{"Endpoint":{"Type":"mod.kcp.endpoint","Object":"192.168.1.10:1792"},"TTL":7200}}
{"Type":"mod.nodes.endpoint_with_ttl","Object":{"Endpoint":{"Type":"mod.tcp.endpoint","Object":"192.168.1.10:1791"},"TTL":7200}}
{"Type":"mod.nodes.endpoint_with_ttl","Object":{"Endpoint":{"Type":"mod.tor.endpoint","Object":"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaad.onion:1791"},"TTL":7776000}}
{"Type":"eos","Object":null}
```

A caller outside the swarm that holds no delegation of the action is refused:

```shellsession
$ astral-query nodes.resolve_endpoints -identity 037f990e61acee8a7697966afd29dd88f3b1f8a7b14d625c4f8742bd952003a590 -out json
{"Type":"error_message","Object":"not permitted"}
```
