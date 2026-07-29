# Zone

* A `Zone` scopes where a [`Query`](query.md) or [`Operation`](op.md) may be routed and
  resolved.
* There are three `Zones`:
  * `Device` — local to the [`Node`](node.md) itself: its own storage and hosted
    [`Apps`](app.md).
  * `Virtual` — the `Node`'s virtual providers, which are neither device-local nor
    on the network.
  * `Network` — other [`Nodes`](node.md), reached over [`Links`](link.md).
* A `Zone` is a set: any combination of the three can be permitted at once.
* An `Operation` that accepts a `Zone` treats it as a filter; the default is all
  `Zones`.
* The `Network` `Zone` is stripped from untrusted queries (e.g. anonymous guests),
  confining them to the local `Node`: a `Query` that lacks it cannot reach another
  `Node` and fails with `route_not_found` before any [`Link`](link.md) is tried.
  Authenticating (presenting an access token) retains it.
* A `Zone` is written in text as a string of `d`, `v`, `n` (e.g. `dvn`), and on the
  wire as a [`uint8`](../primitive-types/uint8.md) bit field. The encodings are
  given in [`zone`](../primitive-types/zone.md).
* The bits are `Device` = `0x01` (letter `d`), `Virtual` = `0x02` (letter `v`),
  `Network` = `0x04` (letter `n`).
* The text form concatenates the letters of the set bits in `d`, `v`, `n` order.
* The default is all three bits set (`0x07`, text `dvn`).
