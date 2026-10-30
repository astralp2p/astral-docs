# Node Exposure

This page lists the surfaces a fresh astrald node opens, who reaches each
surface, and the setting that opens or closes it. The values are astrald
defaults at commit `0f7da199`, checked on a throwaway node; the rule for
settings set through the tree is from commit `5f17900d`. A setting lives in
`<name>.yaml` in the node's config directory.

## Surfaces

| Surface | Default bind | Reach | Without a token, unclaimed | Without a token, claimed | Switch |
|---|---|---|---|---|---|
| TCP links | `:1791`, all interfaces | host, LAN, internet | any identity links; see [Linked peers](#linked-peers) | same | `tcp.yaml` `listen`, `listen_port` |
| KCP links | `:1792` UDP, all interfaces | host, LAN, internet | as TCP links | as TCP links | `kcp.yaml` `listen`, `listen_port` |
| Tor onion service | off | internet through Tor | as TCP links, when on | as TCP links, when on | `tor.yaml` `listen: true`; needs a Tor control port at `control_addr` (default `127.0.0.1:9051`) |
| ether discovery | `:8822` UDP, all interfaces | LAN | carries nearby | carries nearby | `ether.yaml` `listen`, `udp_port` |
| nearby status and scan reply | over ether | LAN | node identity as the signed source; `adoptable` flag, public profile, endpoints, alias | node identity as the signed source; stealth hint | `nearby.yaml` `mode`; `0` sends nothing |
| apphost IPC | `tcp:127.0.0.1:8625`, `unix:~/.apphost.sock` | host | the unclaimed allowlist | the claimed allowlist | `apphost.yaml` `listen`, `allow_anonymous`, `anonymous_allowlist` |
| apphost HTTP | `tcp:127.0.0.1:8624` | host, and any page open in a local browser | `/.ws`: the unclaimed allowlist, any `Origin`; other paths answer `401`, except `OPTIONS` | `/.ws`: the claimed allowlist, any `Origin`; other paths answer `401`, except `OPTIONS` | `apphost.yaml` `bind_http`, `allow_anonymous`, `anonymous_allowlist`; `/.ws` answers `403` to a non-loopback client whatever `bind_http` is |
| MCP | `tcp:127.0.0.1:8626` | host | none: a request needs a bearer token | same | `mcp.yaml` `bind_mcp`; empty disables the server |
| gateway | serves no node; registers with no gateway | none | none | none | `gateway.yaml` `gateway.enabled` with a `tcp` port under `gateway.networks`, `gateways`, `visibility` |
| fwd forwards | none | per forward | each TCP client runs the `astral://` target query as the node, or as the `caller@` the target names | same | `fwd.yaml` `forwards` |

* "Without a token" means a session that presents no token, or a peer that
  holds no grant. [Session Identity](session-identity.md) lists both
  allowlists.
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
* A registering app holds the permits it asks for. The bundled register policy
  accepts every registration until
  [`apphost.set_app_register_policy`](../protocols/apphost/ops/apphost.set_app_register_policy.md)
  names a delegate.
* Any page open in a local browser reaches `/.ws`. On an unclaimed node, that
  page can claim the node. On a claimed node, that page can register an app.
* [`mod.nearby.mode`](../protocols/nearby/types/mod.nearby.mode.md) lists what
  each nearby mode discloses. An unclaimed node broadcasts in Visible unless
  its stored mode is `0` (Silent). A claimed node broadcasts in Stealth by
  default.
* The HTTP server sends `Access-Control-Allow-Origin: *` on every path except
  `/.ws`.

## Linked peers

Any identity links to the node: the node checks no peer identity before the
link. A linked peer that holds no grant reaches these operations:

* In both claim states: `apphost.whoami`, `bip137sig.derive_key`,
  `bip137sig.mnemonic`, `bip137sig.new_entropy`, `bip137sig.seed`,
  `crypto.public_key`, `crypto.verify_hash_signature`,
  `crypto.verify_text_signature`, `dir.get_alias`, `dir.resolve`,
  `gateway.node_list`, `gateway.node_unregister`, `objects.new`,
  `objects.push`, `secp256k1.new`, `shell.spec`, `.spec`, and
  `gateway.node_route` naming the node itself.
* On an unclaimed node only:
  [`user.accept_contract`](../protocols/user/ops/user.accept_contract.md),
  [`user.accept_membership`](../protocols/user/ops/user.accept_membership.md),
  and [`user.info`](../protocols/user/ops/user.info.md), which answers
  `no active contract`.
  A linked peer can claim an unclaimed node under the bundled invite policy.
* On a claimed node only:
  [`user.request_membership`](../protocols/user/ops/user.request_membership.md).
  Under the bundled join policy, the node signs the peer a swarm membership
  contract. A swarm member passes the checks that admit the user's nodes, such
  as [`mod.auth.admin_network_action`](../protocols/auth/types/mod.auth.admin_network_action.md).

Every other operation refuses a network caller, or requires an authorization
that the peer fails under the default config.

## Reset

Removing the data directory resets the node. The node gets a new identity, and
its claim, issued tokens, grants and the settings set through the tree are
removed. A node whose tor listens gets a new onion address. A token that
`tokens:` in `apphost.yaml` lists returns at the next start when its identity
resolves without the database: `localnode`, a public key or a DNS name. By
default on macOS and Windows, the data directory is the config directory, so a
reset there also removes the `<name>.yaml` settings.

No operation resets a node in place. An expulsion that names the node clears
its active contract, and the node then acts as unclaimed; its identity, tokens
and grants stay.
