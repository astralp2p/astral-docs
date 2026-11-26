# Node Exposure

This page lists the surfaces a fresh astrald node opens, who reaches each
surface, and the setting that opens or closes it. The values are astrald
defaults at commit `0f7da199`, checked on a throwaway node; the rule for
settings set through the tree is from commit `5f17900d`. The apphost gate, the
node states and the policy defaults are read from astrald source at commit
`5b4dde12`; a node checked them under the E2E overrides only. The ether and
nearby rows, `user.contract` under [Linked peers](#linked-peers) and the dials
that nearby triggers follow the ether and nearby specification, not a checked
node. A setting lives in `<name>.yaml` in the node's config directory.

## Surfaces

| Surface | Default bind | Reach | Without a token, before the claim | Without a token, claimed | Switch |
|---|---|---|---|---|---|
| TCP links | `:1791`, all interfaces | host, LAN, internet | any identity links; see [Linked peers](#linked-peers) | same | `tcp.yaml` `listen`, `listen_port` |
| KCP links | `:1792` UDP, all interfaces | host, LAN, internet | as TCP links | as TCP links | `kcp.yaml` `listen`, `listen_port` |
| Tor onion service | off | internet through Tor | as TCP links, when on | as TCP links, when on | `tor.yaml` `listen: true`; needs a Tor control port at `control_addr` (default `127.0.0.1:9051`) |
| ether discovery | `:8822` UDP, IPv4, all interfaces | LAN: a datagram from outside the local IPv4 subnets, or with an IP TTL other than 255, is dropped | carries nearby; unsigned, no source identity | same | `ether.yaml` `listen`, `udp_port` |
| nearby status and scan reply | over ether | LAN | `adoptable` flag; public profile with the node identity and alias; the `tcp` and `kcp` listen ports in plaintext when either is not its default; status proof | Stealth by default: stealth hint, the listen ports sealed to the node identity when either is not its default, and status proof with a wrapped signature. Visible: public profile with the node identity, user identity and alias; the listen ports in plaintext when either is not its default; status proof | `nearby.yaml` `mode`; `0` sends nothing |
| apphost IPC | `tcp:127.0.0.1:8625`, `unix:~/.apphost.sock` | host | the gate's `tokenless` operations on the `fresh` or `unclaimed` list | the gate's `tokenless` operations | `apphost.yaml` `listen`, `gate` |
| apphost HTTP | `tcp:127.0.0.1:8624` | host, and any page open in a local browser | `/.ws`: as apphost IPC, any `Origin`; other paths answer `401`, except `OPTIONS` | `/.ws`: as apphost IPC, any `Origin`; other paths answer `401`, except `OPTIONS` | `apphost.yaml` `bind_http`, `gate`; `/.ws` answers `403` to a non-loopback client whatever `bind_http` is; a query the gate refuses answers `403` |
| MCP | `tcp:127.0.0.1:8626` | host | none: a request needs a bearer token | same | `mcp.yaml` `bind_mcp`; empty disables the server |
| gateway | serves no node; registers with no gateway | none | none | none | `gateway.yaml` `gateway.enabled` with a `tcp` port under `gateway.networks`; `gateways` entries of `id` and `endpoints`, `visibility` ([gateway configuration](../protocols/gateway/README.md#configuration)) |
| fwd forwards | none | per forward | each TCP client runs the `astral://` target query as the node, or as the `caller@` the target names | same | `fwd.yaml` `forwards` |

* "Without a token" means a session that presents no token, or a peer that
  holds no grant. [Session Identity](session-identity.md) lists the gate's
  default lists. "Before the claim" covers the `fresh` and `unclaimed` states
  ([apphost, Node states](../protocols/sys/README.md#node-states)).
* `listen` in `tcp.yaml` and `kcp.yaml`, and `mode` in `nearby.yaml`, write
  the tree values `/mod/tcp/settings/listen`, `/mod/kcp/settings/listen` and
  `/mod/nearby/mode` at every start when the file states the key. Otherwise a
  value set through the tree persists across restarts, and an unset value
  follows the built-in default. A value the file wrote stays in the tree after
  the key is removed, so removing `mode: 1` from `nearby.yaml` leaves a claimed
  node Visible. A `tree.set` of a `nil` object returns the setting to the
  built-in default. A `tree.set -value` of an unset tcp or kcp `listen` needs
  an explicit type, for example `-type bool -value false`. The nearby mode has
  no text form, so it is set with a JSON object on the input stream.
* `listen` and `dial` in `tor.yaml`, or their built-in defaults, write
  `/mod/tor/settings/listen` and `/mod/tor/settings/dial` at every start. A
  runtime change of either lasts until the next start.
* `listen` in `ether.yaml` takes effect at the next start.
* The app register policy refuses every registration by default. A delegate
  set by
  `apphost.set_app_register_policy` (removed)
  or `policies.app_register: accept_all` admits registrations
  ([Node Policies](node-policies.md)).
* Any page open in a local browser reaches `/.ws`. On a `fresh` node, that page
  can appoint itself the manager with
  [`sys.register_manager`](../protocols/sys/ops/sys.register_manager.md)
  and then claim the node with the manager's token. On an `unclaimed` or
  `claimed` node, that page can call `apphost.register`, which the app register
  policy decides.
* [`mod.nearby.mode`](../protocols/nearby/types/mod.nearby.mode.md) lists what
  each nearby mode discloses. A node without an active contract broadcasts in Visible unless
  its stored mode is `0` (Silent). A claimed node broadcasts in Stealth by
  default.
* The HTTP server sends `Access-Control-Allow-Origin: *` on every path except
  `/.ws`.
* A query to the HTTP server from a non-loopback TCP client carries `network`
  origin, so an operation that refuses a network caller refuses it
  ([HTTP transport](http-transport.md)).

## Linked peers

Any identity links to the node: the node checks no peer identity before the
link. A linked peer that holds no grant reaches these operations:

* In every state: `apphost.whoami`, `bip137sig.derive_key`,
  `bip137sig.mnemonic`, `bip137sig.new_entropy`, `bip137sig.seed`,
  `crypto.public_key`, `crypto.verify_hash_signature`,
  `crypto.verify_text_signature`, `dir.get_alias`, `dir.resolve`,
  `gateway.node_list`, `gateway.node_unregister`, `objects.new`,
  `objects.push`, `secp256k1.new`, `shell.spec`, `.spec`,
  `gateway.node_route` naming the node itself, and
  [`user.contract`](../protocols/user/ops/user.contract.md). On a claimed node
  `user.contract` answers the active contract. The contract names the user.
  Its permits show whether the node is a management node
  ([user](../protocols/user/README.md)). Its expiry, by default 365 days after
  the contract was made, shows when the user claimed or adopted the node.
  Before the claim `user.contract` answers `no active contract`.
* On a `fresh` or `unclaimed` node only:
  [`user.accept_contract`](../protocols/user/ops/user.accept_contract.md),
  `user.accept_membership` (removed),
  and [`user.info`](../protocols/user/ops/user.info.md), which answers the
  node's `State` and `Manager`. The apphost gate does not apply to a linked
  peer.
  The default swarm invite policy, `reject_all`, declines an invitation from a
  linked peer ([Node Policies](node-policies.md#before-the-claim)).
* On a claimed node only:
  `user.request_membership` (removed).
  The default swarm join policy, `reject_all`, declines the peer. Under
  `accept_all`, the node signs the peer a swarm membership contract. A swarm member passes the checks that admit the user's nodes, such
  as [`mod.auth.admin_network_action`](../protocols/auth/types/mod.auth.admin_network_action.md).

Every other operation refuses a network caller, or requires an authorization
that the peer fails under the default config.
[`nodes.resolve_endpoints`](../protocols/nodes/ops/nodes.resolve_endpoints.md)
is one of them: a linked peer outside the swarm learns no endpoint of the node
([Endpoint exchange](#endpoint-exchange)).

A claimed node dials out when nearby verifies a node of its own user
([user](../protocols/user/README.md)). It links to the peer's source IP on the
TCP or KCP port the peer's status carries, `1791` and `1792` when the status
carries no ports ([nearby](../protocols/nearby/README.md)), reads the peer's
contract with `user.contract`, and pushes its own contract only when the peer's
contract passes the check. It dials no unowned node and no node of another user. A node
in mode `0` (Silent) dials as well, unless `silent_listen` in `nearby.yaml` is
`false`.

## Endpoint exchange

A node's endpoints, and the endpoints it stores for other nodes, are private
to its user's swarm. This section is read from astrald source at commit
`5b64abb0`.
[`nodes.resolve_endpoints`](../protocols/nodes/ops/nodes.resolve_endpoints.md)
answers only a holder of
[`mod.auth.admin_network_action`](../protocols/auth/types/mod.auth.admin_network_action.md):
the user identity, the node itself, a current node member of the swarm, or an
identity the action is delegated to. A node pulls a peer's endpoints when the
first link with the peer forms only when the peer is a member of its own
swarm. A link with a node outside the swarm, such as a node of another user, a
gateway the user never adopted or a hosting node, therefore stores no
endpoints on either side.

Three operator paths make a node outside the swarm reachable:

* **A manual row.**
  [`nodes.add_endpoint`](../protocols/nodes/ops/nodes.add_endpoint.md), on
  each node that dials the outsider, stores one endpoint of the outsider for
  90 days (`7776000` seconds). Nothing renews the row: the operator adds it
  again before it lapses and after the outsider's address changes. The node
  gives no notice before the row lapses, and a lapsed row resolves to no
  endpoint.
* **A delegated `mod.auth.admin_network_action`.** A contract chain from the
  user that grants the action to the outsider's identity
  ([Holders](../protocols/auth/types/mod.auth.admin_network_action.md#holders))
  admits the outsider to `nodes.resolve_endpoints` on a node that holds the
  chain. The outsider reads the node's endpoints and stores them on its own
  side with `nodes.add_endpoint`; nothing pulls them for it.
  **Warning:** the permit grants every operation the action gates, not only
  endpoint reads. The outsider can list the node's links and sessions, open
  and close links, migrate sessions, add endpoints, punch NAT holes, open and
  close ephemeral listeners, and switch NAT traversal off. A permit for the action
  carries no constraints that narrow it.
* **Visible nearby on a shared LAN.** A node in nearby mode `1` (Visible)
  broadcasts its node identity in a public profile. A node of any user on the
  same IPv4 link verifies the status and resolves the node at the status's
  source IP, `tcp` and `kcp` on the listen ports the status carries (`1791`
  and `1792` when it carries none), until the cache
  entry expires 5 minutes after the last status
  ([nearby](../protocols/nearby/README.md)). A claimed node broadcasts in
  Stealth by default; a node of another user caches its status as an
  unrecognised node and resolves no endpoint for it. `mode: 1` in
  `nearby.yaml` sets Visible.

## Reset

Removing the data directory resets the node. The node gets a new identity, and
its claim, issued tokens, grants and the settings set through the tree are
removed. A node whose tor listens gets a new onion address. A token that
`tokens:` in `apphost.yaml` lists returns at the next start when its identity
resolves without the database: `localnode`, a public key or a DNS name. By
default on macOS and Windows, the data directory is the config directory, so a
reset there also removes the `<name>.yaml` settings.

No operation resets a node in place. An expulsion that names the node clears
its active contract, and the node is `unclaimed` again; its identity, tokens,
grants and manager stay.
