# Contract

* A `Contract` is a permission granted by one [`Identity`](identity.md) (the `Issuer`) to
  another (the `Subject`), authorising the `Subject` to represent the `Issuer` on the
  `Astral Network` in some capacity.
* A [`User`](user.md) signs a `Contract` with a [`Node`](node.md) so the `Node` can act for the
  `User`; an [`App`](app.md) signs a `Contract` with its host `Node` so the `Node` can route
  its traffic.
* A `Contract` carries an `Issuer`, a `Subject`, a list of [`Permits`](permit.md), and an
  expiry time.
* A `Contract` grants an action when one of its `Permits` matches that action.
* A `Contract` carries no signatures on its own; once co-signed by both the `Issuer`
  and the `Subject` it becomes a `Signed Contract`. A `Contract` carries authority
  only when both signed it, and authority is walked from the `Subject` to the
  `Issuer`.
* See the wire type [`mod.auth.contract`](../protocols/auth/types/mod.auth.contract.md).
