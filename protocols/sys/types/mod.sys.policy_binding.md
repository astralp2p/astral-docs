# mod.sys.policy_binding

An element of the `Policies` field of a
[`mod.sys.register_manager_request`](mod.sys.register_manager_request.md).
The admission policies it bound are removed: joins and app permits are
requests in SwarmState, answered with
[`user.answer_request`](../../user/ops/user.answer_request.md).
[`sys.register_manager`](../ops/sys.register_manager.md) refuses a request
that carries any binding. The type stays on the wire while the request keeps
the field.

## Fields

* Policy (string8) – A policy name.
* Operation (string8) – An operation of the manager.
* Timeout (duration) – A wait for one answer.
