# Protocols

* Subdirectories in this directory are named after protocols they describe.
* The `Object Types` used by protocols are described in their "types" subdirectory.
* The `Operations` used by protocols are described in their "ops" subdirectory.
* All operations implicitly support the special `in` and `out` parameters.
  Those parameters select the input and output encoding for the `Operation`.
  The two directions accept different token sets; both are listed in
  [`Channel`](../core-definitions/channel.md).
* Operation parameters are named for what they carry:
  * A parameter naming an [`Identity`](../core-definitions/identity.md) is
    named `identity`. Its value is a `string8` holding a hex public key or a
    name, and the node resolves it as [`dir.resolve`](dir/ops/dir.resolve.md)
    does.
  * A parameter named `id` carries an
    [`Object ID`](../core-definitions/object-id.md). An operation that looks the
    object up accepts a
    [`Partial Object ID`](../core-definitions/object-id.md) as well; an
    operation that records the `id` accepts only an `Object ID` with a nonzero
    `Size`.
  * A `nonce64` parameter is named for what the nonce identifies: `query_id`,
    `link_id`, `session_id`.
  * A parameter naming an identity by its role in the operation keeps the
    role's name: `user.new_node_contract` takes `user` and `node`, and
    `shell.shell` takes `as`.
* The `Target` of a [`Query`](../core-definitions/query.md) is the identity the
  query is routed to, such as the `target:` prefix of
  [`astral-query`](../tools/astral-query.md). It is not an operation parameter.