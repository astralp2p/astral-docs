# tcp

The `tcp` protocol provides TCP-based transport for astral node connectivity: dialing outbound connections, accepting inbound connections, and managing ephemeral listeners on dynamic ports.

Endpoints are represented as `mod.tcp.endpoint` objects encoding an IP address and port. The module exposes two ops: `tcp.new_ephemeral_listener` starts a listener on a given port; `tcp.close_ephemeral_listener` stops it.

## Advertising a public or forwarded endpoint

A node advertises its own TCP endpoints to the nodes of its swarm. By default
the list holds one endpoint per local interface address, at the listen port
`listen_port` in `tcp.yaml`, `1791` by default. A node behind 1:1 NAT, such as
a cloud VM with a private interface address, or behind a router that forwards
a port to its listen port, has only private interface addresses, so a sibling
that is not on its network cannot dial it. Such a node advertises the public
address with the `configEndpoints` list in `tcp.yaml`, in the node's config
directory. The key, the entry format and the behaviour below are those of
astrald at commit `463a4fea`.

```yaml
listen_port: 1791
configEndpoints:
  - 203.0.113.5:1791   # public address of the 1:1 NAT or the port forward
```

* **Key.** `configEndpoints`, in camel case, next to the snake-case
  `listen_port` and `dial_timeout`.
* **Entry.** The public IP address and the public port, `<ip>:<port>`, the
  text form of [`mod.tcp.endpoint`](types/mod.tcp.endpoint.md). A `tcp:`
  prefix is accepted and dropped. An IPv6 address is written in brackets:
  `[2001:db8::5]:1791`. The entry names a literal IP address; the node
  resolves no host name.
* **Port.** The port the router or the NAT accepts on the public address,
  which forwards to `listen_port` on the node. A router that forwards public
  port `40000` to the node's port `1791` gets `203.0.113.5:40000`.
* **Invalid entry.** The node logs `tcp module/Load invalid endpoint: <entry>`,
  skips the entry and starts.
* **Load.** The node reads the list at start only. A change takes effect at
  the next start.

The node advertises every entry with a TTL of 7 days, next to the endpoints
of its local interface addresses. A sibling stores the advertised endpoints
with that TTL each time a link between the two nodes forms while no other link
between them is open. A sibling
that receives the node's contract from another member asks that member for the
node's endpoints and stores them as well. A sibling's
[`nodes.resolve_endpoints`](../nodes/ops/nodes.resolve_endpoints.md) of the
node then lists the entry with the remaining TTL:

```shellsession
$ astral-query nodes.resolve_endpoints -identity 02f7... -out json
{"Type":"mod.nodes.endpoint_with_ttl","Object":{"Endpoint":{"Type":"mod.tcp.endpoint","Object":"203.0.113.5:1791"},"TTL":604785}}
{"Type":"eos","Object":null}
```

When the listen setting is off (`listen: false` in `tcp.yaml`, or
`/mod/tcp/settings/listen` set to `false` through the tree), the node
advertises no TCP endpoint, configured entries included. A public IPv4 or IPv6
entry is also a candidate of
[`ip.public_ip_candidates`](../ip/ops/ip.public_ip_candidates.md), which the
nat and gateway modules read.

The operator edits the entry and restarts the node when the public address or
the forwarded port changes. Until then the node keeps advertising the stale
entry. A sibling learns a changed entry only at its next store, and keeps a
row the node no longer advertises until its 7 days run out; until then it
dials the stale row along with the others.

The list covers TCP only. The node does not advertise a public address that
its peers observe for it: automatic advertisement of an observed public
address is deferred to a later iteration. An observed address serves only as
a hint for NAT traversal and the gateway.
