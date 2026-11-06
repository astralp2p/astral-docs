# sys

The `sys` protocol holds the node's lifecycle: its state and its manager. A
new node is `fresh`. A `fresh` node appoints a manager with
[`sys.register_manager`](ops/sys.register_manager.md) and becomes `unclaimed`.
A claim makes the node `claimed`
([User and Swarm, Claiming a node](../../topics/user-and-swarm.md#claiming-a-node)).
[Node Setup](../../topics/node-setup.md) narrates the lifecycle.

## Node states

A node is in one of three states.
[`user.info`](../user/ops/user.info.md) reports the state in `State`.

| State | Condition |
|-------|-----------|
| `fresh` | The node has no active contract, has never held one, and has no manager. |
| `unclaimed` | The node has no active contract, and it has a manager or has held an active contract before. |
| `claimed` | The node has an active contract. |

* The node records at `/mod/user/config/owned` that it has held an active
  contract. The record is written when a contract activates. Expiry and
  expulsion do not clear it.
* A node without the `user` module is `fresh` until a manager is appointed,
  and `unclaimed` afterwards.
* The state waits for the `user` module to start. A read whose context ends
  first reads `fresh`.
* The apphost [gate](../apphost/README.md#gate) admits each query by the node's
  state.

## Manager

The manager is the [`App`](../../core-definitions/app.md) identity
[`sys.register_manager`](ops/sys.register_manager.md) appoints. A node has at
most one manager. Only a `fresh` node appoints a manager, and the appointment
moves the node to `unclaimed`. The node stores the manager at
`/mod/sys/manager`. A node without a record at `/mod/sys/manager` reads the
record at `/mod/apphost/manager`, where earlier nodes stored it. No operation
removes the manager. A claim keeps it.

The manager:

* is the delegate of each policy its appointment binds;
* holds
  [`mod.auth.configure_node_state_action`](../auth/types/mod.auth.configure_node_state_action.md)
  in every node state, `claimed` included, so it may call the policy setters
  ([Node Policies, Delegating a decision](../../topics/node-policies.md#delegating-a-decision));
* may claim the node with [`user.bootstrap`](../user/ops/user.bootstrap.md) or
  [`user.join`](../user/ops/user.join.md) under its App token.

[`user.info`](../user/ops/user.info.md) reports the manager in `Manager`.

## Operations

* [`sys.register_manager`](ops/sys.register_manager.md) – provision a fresh App identity and appoint it the node's manager

## Types

* [`mod.sys.register_manager_request`](types/mod.sys.register_manager_request.md) – the registration an app sends to become the manager
* [`mod.sys.policy_binding`](types/mod.sys.policy_binding.md) – one policy the manager decides
