# App Routing

* An [`App`](../core-definitions/app.md) is reached the way a [`Node`](../core-definitions/node.md)
  is: by addressing a [`Query`](../core-definitions/query.md) to its
  [`Identity`](../core-definitions/identity.md). An `App` holds no
  [`Link`](../core-definitions/link.md) of its own, so a `Query` addressed to it travels over the
  `Links` its host `Node` holds and the `Node` relays it the last hop.
* A caller names the target `App` and nothing else. It does not name the `Node` hosting the target,
  learns no `Node` from the exchange, and arranges no route: resolving the target to a host is the
  calling `Node`'s work, and it is done from state the `Node` already holds.
* Within a [`Swarm`](../core-definitions/swarm.md) whose members hold each other's `App`
  [`Contracts`](../core-definitions/contract.md), an `App` on one `Node` is therefore directly
  addressable from an `App` on another, and neither `App` arranges the route.

## The contract an app signs

* An `App` signs a `Contract` with its host `Node` carrying a
  [`Permit`](../core-definitions/permit.md) for
  [`mod.nodes.relay_for_action`](../protocols/nodes/types/mod.nodes.relay_for_action.md). The `App`
  is the `Issuer` and the `Node` is the `Subject`: the `App` permits that `Node` to relay on its
  behalf.
* The `Contract` is signed when the `App` provisions itself — `apphost.register` mints an `Identity`
  and signs the `Contract` in one step — or afterwards through `apphost.new_app_contract` and
  `apphost.sign_app_contract`.
* The `Contract` is what makes an `App` addressable. An `Identity` no `Contract` names is an
  `Identity` no `Node` relays for, and a `Query` addressed to it resolves to no host.
* An `App` hosted on several `Nodes` signs a `Contract` with each. The `Identities` are distinct —
  a `Node` assigns its own — so an `App` on two `Nodes` is two `Identities`, never one reachable at
  two places.

## Resolving the host

* A `Node` routing a `Query` whose `Target` is an `App` searches the `Contracts` it holds for those
  the `Target` issued carrying a `mod.nodes.relay_for_action` `Permit`, and takes each `Subject` as
  a `Node` hosting the `Target`. Those `Nodes` are the relay candidates.
* The `Node` links to a candidate and sends the `Query` as a relay frame naming the original
  `Caller` and the `Target`, rather than as a `Query` of its own. The framing is in
  [`Link Multiplexer`](link-mux.md).
* The `Node` attaches the calling `App`'s own `Contract` to the outgoing `Query`, so the receiving
  `Node` can establish that the caller permits this relayer to speak for it.
* A `Node` holding no such `Contract` for the `Target` has no candidate and the `Query` fails as
  unroutable. Resolution consults held `Contracts` alone and asks the network nothing.

## Authorizing the relay

* A `Node` receiving a relayed `Query` whose `Caller` is not the `Node` on the other end of the
  `Link` authorizes the relay before routing it: the relaying `Node` must be permitted to relay for
  that `Caller`.
* The permission resolves through the `Contract` the `Caller` issued. The relaying `Node` is its
  `Subject`, and re-evaluating as the `Issuer` reaches an `Identity` relaying for itself, which is
  permitted. Authority therefore flows from the `App` that granted it and from nowhere else.
* A `Node` that holds no `Contract` for the `Caller` refuses the relay. Holding one is what
  distinguishes a `Caller` a `Node` will carry from one it will not.

## Answering

* A `Node` routes a `Query` reaching it to the `App` whose `Identity` the `Target` names, over the
  handler that `App` registered.
* Registering the handler is local-only: `apphost.register_handler` refuses a `Query` arriving over
  the network, so an `App` registers with the `Node` hosting it and never across a `Link`.
* Answering is not. A handler serves whatever its `Node` routes to it, and a relayed `Query` is
  served exactly as a local one is. An `App` that must distinguish the two reads the `Query`'s
  origin and decides for itself; the `Node` draws no such line on its behalf.

## Reach

* A `Node` holds an `App`'s `Contract` only if it was given one. A `Node` gives its `Apps`'
  `Contracts` to the members of its `Swarm`, on joining and as they are signed, so the members of a
  `Swarm` come to know which `Apps` each of them hosts.
* A `Node` refuses to index a `Contract` unless its `Issuer` or `Subject` is already known to the
  `Swarm` — the [`User`](../core-definitions/user.md) the `Node` answers to, or one of its members.
  An unrelated `App` therefore acquires no route by offering its own `Contract`.
* The reach of an `App` `Identity` is therefore the `Swarm` its host belongs to. In a
  [`Local Swarm`](../core-definitions/local-swarm.md) that `Swarm` is one `User`'s own `Nodes`: an
  `App` addresses its counterpart on any of them, and an `App` outside the `Swarm` addresses none.
