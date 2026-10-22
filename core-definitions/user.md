# User

* A `User` cannot send or accept [`Queries`](query.md).
* A `User` acts on the `Astral Network` by controlling one or more [`Nodes`](node.md).
* A `User` and `Node` cryptographically sign [`Objects`](object.md) that can be used to prove
  to other [`Identities`](identity.md) that the `User` controls the `Node`.
* A `Node` starts without a `User`. [Node Setup](../topics/node-setup.md) claims a `Node`
  for a `User` identity derived from BIP-39 words.
