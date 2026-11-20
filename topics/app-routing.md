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
* The `Contract` is signed when the `App` provisions itself: `apphost.register` mints an `Identity`
  and signs the `Contract` in one step. There is no second path — an `App` does not bring an
  `Identity` of its own to a `Node`.
* The `Contract` is what makes an `App` addressable. An `Identity` no `Contract` names is an
  `Identity` no `Node` relays for, and a `Query` addressed to it resolves to no host.
* An `App` hosted on several `Nodes` signs a `Contract` with each. The `Identities` are distinct —
  a `Node` assigns its own — so an `App` on two `Nodes` is two `Identities`, never one reachable at
  two places.

## Resolving the host

* A `Node` routing a `Query` whose `Target` is an `App` searches the `Contracts` it holds for those
  the `Target` issued carrying a `mod.nodes.relay_for_action` `Permit`, and takes each `Subject` as
  a `Node` hosting the `Target`. Those `Nodes` are the relay candidates.
* A `claimed` `Node` ([User and Swarm](user-and-swarm.md)) keeps as candidates only the
  `Subjects` that are current members of its
  [`Local Swarm`](../core-definitions/local-swarm.md). A `Subject` the `User` expelled, or whose
  membership `Contract` expired, is no candidate, so the `Node` neither links to it nor sends it
  the calling `App`'s `Contract` for this `Query`. A `Node` that is not `claimed` keeps every
  `Subject`.
* The `Node` links to a candidate and sends the `Query` as a relay frame naming the original
  `Caller` and the `Target`, rather than as a `Query` of its own. The framing is in
  [`Link Multiplexer`](link-mux.md).
* The `Node` attaches the calling `App`'s own `Contract` to the outgoing `Query`, so the receiving
  `Node` can establish that the caller permits this relayer to speak for it.
* The `Node` tries the candidates one at a time, in the order it found them. The first candidate
  that accepts the `Query` ends the routing. A candidate that does not accept does not end it, and
  the next candidate is tried.
* A `Node` that holds candidates tries them before it links to the `Target`. A `Link` the `Node`
  already holds to the `Target` takes the `Query` ahead of every candidate. When no candidate
  accepts, the `Node` does not link to the `Target` afterwards. Linking to the candidates shares one
  budget of 120 s, which the caller's deadline ends earlier.
* Each candidate that does not accept leaves one of three answers: a refusal (any `Reject Code`
  other than `7`, the generic `1` included, or a candidate that received the calling `App`'s
  `Contract` and did not accept it), unavailable (`Reject Code` `7`, or a candidate the `Node`
  could not reach or could not deliver the `Contract` to), or no route (the candidate answered
  [no route here](link-mux.md#response-semantics)).
* When no candidate accepts, the `Query` fails with the first refusal; with no refusal, it fails as
  unavailable (`7`) when any candidate was unavailable; otherwise it fails as route not found.
* Resolution consults held `Contracts`, and on a miss asks linked members once. A `Node` that
  holds no such `Contract` for the `Target`, and reaches the `Target` over no `Link` of its own,
  asks each member of its `Swarm` it holds a `Link` with for the `Target`'s relay `Contracts`, with
  [`user.relay_contracts`](../protocols/user/ops/user.relay_contracts.md), all members at once.
* The `Node` indexes the first answered `Contract` that passes the admission rule of
  [Reach](#reach), with the answering member as the delivering `Node`, and stops asking. The
  candidates are then the `Subjects` of the relay `Contracts` the `Target` issued that the `Node`
  holds.
* The ask is a detached flight that lasts at most 10 s, so it runs on when the `Query` that
  started it ends. A `Query` waits for the flight at most 3 s, then routes on without a candidate.
  `Queries` to one `Target` that miss while a flight for it runs share that flight, so each miss
  asks the members once. A `Contract` that arrives after the `Query` stopped waiting, within the
  10 s, is indexed all the same, and the next `Query` to the `Target` finds its candidate in the
  index without an ask.
* A `Contract` that arrived within the 10 s is indexed even when the 10 s end first: the `Node`
  gives indexing it a bound of its own, 2 s, so the flight stays registered at most 2 s past the
  10 s.
* The `Node` never asks for a `Target` that is the `Node` itself, a member of its
  [`Local Swarm`](../core-definitions/local-swarm.md), or its `User`. The ask's own `Queries`
  target members, so an ask never starts another ask.
* An ask that yields no candidate leaves the `Query` failing as route not found.
* The `Node` records a miss for a `Target` only when every member it asked answered without an
  error before the 10 s ended and none held a `Contract` the `Node` admits. For 30 s after a
  recorded miss, the `Node` asks nothing for that `Target`, and a `Query` to it with no held
  `Contract` fails as route not found without an ask.
* An ask whose 10 s ended before every member answered, or in which any member's ask failed with
  an error, records no miss, so the next `Query` to the `Target` asks again. A `Node` with no
  `Link` to a member of its `Swarm` has nobody to ask, and that is an answer of none: the miss is
  recorded.

## Authorizing the relay

* A `Node` receiving a relayed `Query` whose `Caller` is not the `Node` on the other end of the
  `Link` authorizes the relay before routing it: the relaying `Node` must be permitted to relay for
  that `Caller`.
* A `claimed` `Node` first requires the relaying `Node` to be a current member of its
  `Local Swarm`. It refuses a relaying `Node` that is not one, an expelled or lapsed former member
  included, whatever `Contracts` it holds, with the refused code (`1`), and it refuses as well when
  it cannot read its `Local Swarm`. A `Node` that is not `claimed` skips this check. A relayed
  `Query` whose `Caller` is the relaying `Node` itself is not a relay and is not checked.
* The permission resolves through the `Contract` the `Caller` issued. The relaying `Node` is its
  `Subject`, and re-evaluating as the `Issuer` reaches an `Identity` relaying for itself, which is
  permitted. Authority therefore flows from the `App` that granted it and from nowhere else.
* A `Node` that holds no `Contract` for the `Caller` refuses the relay. Holding one is what
  distinguishes a `Caller` a `Node` will carry from one it will not.

## Failures

* A `Query` to an `App` ends in one of the
  [Routing outcomes](../core-definitions/query.md#routing-outcomes), and the `Caller` acts on it:

| Outcome | Typical cause | `Caller` action |
|---------|---------------|-----------------|
| unavailable (`7`) | host unreachable, host's `Link` closed while routing, host starting | retry with backoff, 1 s doubling to 30 s, bounded |
| timeout | host behind a dead `Link` | retry with backoff, bounded |
| route not found | `App` not registered on its host, removed, unknown, its relay `Contract` held neither by the `Node` nor by any linked member, or every host a former member | discover again, or stop |
| rejected `1` or another code | host refused the relay or the calling `App`'s `Contract` (for one, the host was expelled from the `Swarm`), or the `App` refused the `Query` | stop |
| target not allowed | the `Caller`'s `Node` policy excludes the `Target` | stop |

* An `App` that is removed from its host and an `App` that is not registered on it yet both answer
  route not found: a host answers [no route here](link-mux.md#response-semantics) for either.

## Answering

* A `Node` routes a `Query` reaching it to the `App` whose `Identity` the `Target` names, over the
  handler that `App` registered.
* Registering the handler is local-only: `apphost.register_handler` refuses a `Query` arriving over
  the network, so an `App` registers with the `Node` hosting it and never across a `Link`.
* Answering is not. A handler serves whatever its `Node` routes to it, and a relayed `Query` is
  served exactly as a local one is. An `App` that must distinguish the two reads the `Query`'s
  origin and decides for itself; the `Node` draws no such line on its behalf.

## Reach

* A `Node` holds an `App`'s `Contract` only if it was given one. When a `Link` to a member of its
  `Swarm` first comes up, a `Node` gives that member the `Contracts` of the `Apps` every member
  hosts, as far as the `Node` holds them and they pass the admission rule below. It leaves out the
  `Contracts` whose `Subject` is the receiving member. A new member therefore learns the `Apps` of
  the whole `Swarm` from the first member it links to, before it links to their hosts.
* A `Node` gives the `Contract` of an `App` it hosts to the members it is linked to when the `App`
  registers. A member not linked at that moment receives it at its next first `Link` to any member
  that holds it.
* A member that missed both deliveries obtains the `Contract` when it routes a `Query` to the
  `App`: it asks its linked members on the miss ([Resolving the host](#resolving-the-host)).
* A relay `Contract` is one that carries a `Permit` for `mod.nodes.relay_for_action`, alone or
  beside other `Permits`. Routing finds an `App`'s hosts by that `Permit`, so every relay
  `Contract` routes.
* A `Node` indexes a relay `Contract` only when it passes one admission rule:
  * its `Subject` is the `Node` itself or a member of the `Node`'s
    [`Local Swarm`](../core-definitions/local-swarm.md), and an expelled `Node` is not a member;
  * the `Issuer` signature and the `Subject` signature verify;
  * it has not expired.
* A relay `Contract` that another `Node` delivers is indexed only when the delivering `Node` is a
  member of the `Local Swarm` as well. The delivering `Node` need not be the `Subject`.
* Between `Nodes`, only a relay `Contract` whose every `Permit` is for
  `mod.nodes.relay_for_action` travels. A `Node` refuses a delivered relay `Contract` that carries
  another `Permit`, and gives no such `Contract` to a member.
* The rule holds on every path into the index: a `Contract` another `Node` delivers, a `Contract`
  the `Node` signs for an `App` it hosts, and a `Contract` the `Node` reads again from its own
  storage when it rebuilds its index. A rebuilt index therefore holds no `Contract` whose `Subject`
  has been expelled.
* An unrelated `App` acquires no route by offering its own `Contract`: the `Subject` is already a
  member and has signed the `Contract`, so a forwarding member hands out only `Contracts` a host in
  the `Swarm` agreed to.
* The reach of an `App` `Identity` is therefore the `Swarm` its host belongs to. In a
  [`Local Swarm`](../core-definitions/local-swarm.md) that `Swarm` is one `User`'s own `Nodes`: an
  `App` addresses its counterpart on any of them, and an `App` outside the `Swarm` addresses none.
