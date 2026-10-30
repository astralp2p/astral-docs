# Node Exposure

This page lists the surfaces a fresh astrald node opens, who reaches each
surface, and the setting that opens or closes it. The values are astrald
defaults at commit `0f7da199`, checked on a throwaway node. A setting lives in
`<name>.yaml` in the node's config directory.

## Surfaces

| Surface | Default bind | Reach | Without a token, unclaimed | Without a token, claimed | Switch |
|---|---|---|---|---|---|
| TCP links | `:1791`, all interfaces | host, LAN, internet | any identity links; see [Linked peers](#linked-peers) | same | `tcp.yaml` `listen`, `listen_port` |
| KCP links | `:1792` UDP, all interfaces | host, LAN, internet | as TCP links | as TCP links | `kcp.yaml` `listen`, `listen_port` |
| Tor onion service | off | internet through Tor | as TCP links, when on | as TCP links, when on | `tor.yaml` `listen: true`; needs a Tor control port at `127.0.0.1:9051` |
| ether discovery | `:8822` UDP, all interfaces | LAN | carries nearby | carries nearby | `ether.yaml` `listen`, `udp_port` |
| nearby status and scan reply | over ether | LAN | `adoptable` flag, public profile, endpoints, alias | stealth hint only | `nearby.yaml` `mode`; `0` sends nothing |
| apphost IPC | `tcp:127.0.0.1:8625`, `unix:~/.apphost.sock` | host | the unclaimed allowlist | the claimed allowlist | `apphost.yaml` `listen`, `allow_anonymous`, `anonymous_allowlist` |
| apphost HTTP | `tcp:127.0.0.1:8624` | host, and any page open in a local browser | `/.ws`: the unclaimed allowlist, any `Origin`; other paths answer `401` | `/.ws`: the claimed allowlist, any `Origin`; other paths answer `401` | `apphost.yaml` `bind_http`, `allow_anonymous`, `anonymous_allowlist` |
| MCP | `tcp:127.0.0.1:8626` | host | none: a request needs a bearer token | same | `mcp.yaml` `bind_mcp`; empty disables the server |
| gateway | serves no node; registers with no gateway | none | none | none | `gateway.yaml` `gateway.enabled`, `gateways`, `visibility` |
| fwd forwards | none | per forward | each TCP client runs the `astral://` target query as the node, or as the `caller@` the target names | same | `fwd.yaml` `forwards` |

* "Without a token" means a session that presents no token, or a peer that
  holds no grant. [Session Identity](session-identity.md) lists both
  allowlists.
* `listen` in `tcp.yaml`, `kcp.yaml` and `tor.yaml`, and `mode` in
  `nearby.yaml`, write the tree values `/mod/tcp/settings/listen`,
  `/mod/kcp/settings/listen`, `/mod/tor/settings/listen` and
  `/mod/nearby/mode` at every start. A runtime change through the tree lasts
  until the next start.
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
  `objects.push`, `secp256k1.new`, `shell.spec`, `user.info`, `.spec`, and
  `gateway.node_route` naming the node itself.
* On an unclaimed node only:
  [`user.accept_contract`](../protocols/user/ops/user.accept_contract.md) and
  [`user.accept_membership`](../protocols/user/ops/user.accept_membership.md).
  A linked peer can claim an unclaimed node under the bundled invite policy.
* On a claimed node only:
  [`user.request_membership`](../protocols/user/ops/user.request_membership.md).
  Under the bundled join policy, the node signs the peer a swarm membership
  contract. A swarm member passes the checks that admit the user's nodes, such
  as [`mod.auth.admin_network_action`](../protocols/auth/types/mod.auth.admin_network_action.md).

Every other operation refuses a network caller, or requires a grant that the
peer does not hold.

## Reset

Removing the data directory resets the node. The node gets a new identity and
a new onion address, and its claim, issued tokens and grants are removed. No
operation resets a node in place.
