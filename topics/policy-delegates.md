# Policy Delegates

A node makes five admission decisions: which apps register, which grants an app
receives later, which nodes join the swarm, which invitation the node accepts,
and which contract the node activates. A policy makes each decision. Out of the
box, every policy accepts. An approval app takes over a decision when a setter
names it the policy's delegate. The node then asks the approval app every time.

## The five policies

| Policy | Decides | Setter | Tree path | Request | Decision | Refusal |
|--------|---------|--------|-----------|---------|----------|---------|
| App register | each [`apphost.register`](../protocols/apphost/ops/apphost.register.md) | [`apphost.set_app_register_policy`](../protocols/apphost/ops/apphost.set_app_register_policy.md) | `/mod/apphost/policy/app_register` | [`mod.apphost.app_register_request`](../protocols/apphost/types/mod.apphost.app_register_request.md) | [`mod.apphost.app_register_decision`](../protocols/apphost/types/mod.apphost.app_register_decision.md) | `registration declined` |
| Grant request | each [`apphost.request_grant`](../protocols/apphost/ops/apphost.request_grant.md) | [`apphost.set_grant_request_policy`](../protocols/apphost/ops/apphost.set_grant_request_policy.md) | `/mod/apphost/policy/grant_request`, and the mode at `/mod/apphost/policy/grant_request_mode` | [`mod.apphost.grant_policy_request`](../protocols/apphost/types/mod.apphost.grant_policy_request.md) | [`mod.apphost.grant_decision`](../protocols/apphost/types/mod.apphost.grant_decision.md) | `grant declined` |
| [Swarm](../core-definitions/swarm.md) join | each [`user.request_membership`](../protocols/user/ops/user.request_membership.md), the request of a node that joins this node's swarm | [`user.set_swarm_join_policy`](../protocols/user/ops/user.set_swarm_join_policy.md) | `/mod/user/policy/swarm_join` | [`mod.user.swarm_join_request`](../protocols/user/types/mod.user.swarm_join_request.md) | [`mod.user.swarm_join_decision`](../protocols/user/types/mod.user.swarm_join_decision.md) | `request declined` |
| Swarm invite | each [`user.accept_membership`](../protocols/user/ops/user.accept_membership.md), an invitation to an unclaimed node | [`user.set_swarm_invite_policy`](../protocols/user/ops/user.set_swarm_invite_policy.md) | `/mod/user/policy/swarm_invite` | [`mod.user.swarm_invite_request`](../protocols/user/types/mod.user.swarm_invite_request.md) | [`mod.user.swarm_invite_decision`](../protocols/user/types/mod.user.swarm_invite_decision.md) | `invitation declined` |
| Contract accept | each [`user.accept_contract`](../protocols/user/ops/user.accept_contract.md), a signed contract the node activates | [`user.set_contract_accept_policy`](../protocols/user/ops/user.set_contract_accept_policy.md) | `/mod/user/policy/contract_accept` | [`mod.user.contract_accept_request`](../protocols/user/types/mod.user.contract_accept_request.md) | [`mod.user.contract_accept_decision`](../protocols/user/types/mod.user.contract_accept_decision.md) | `contract declined` |

While a policy names no delegate, the node applies the bundled policy, which
accepts:

* The app register policy writes every permit an app asks for,
  [`mod.auth.admin_manage_apps_action`](../protocols/auth/types/mod.auth.admin_manage_apps_action.md)
  included.
* The grant request policy grants every permit an app asks for.
* The swarm join policy admits every requester.
* The swarm invite policy accepts every invitation.
* The contract accept policy accepts every contract that passes validation.

The grant request policy also has two modes, `accept_all` and `reject_all`. An
unset mode selects `accept_all`. A stored mode value other than `accept_all`
refuses every request. A stored delegate decides whatever the mode holds.

## Delegating a decision

A setter takes `identity` and `operation`, and an optional `timeout`:

* `identity` names the delegate, as a hex public key or a name the directory
  resolves. The setter refuses the node's own identity and `anyone`.
* `operation` names the op the node queries on the delegate, such as
  `apphost.decide_app_register`.
* `timeout` bounds the wait for one answer. Omitted, zero or negative waits 10
  minutes. A value above 10 minutes is refused.
* A setter without `identity` and `operation` clears the delegate and restores
  the bundled policy.

Every setter requires
[`mod.auth.admin_manage_apps_action`](../protocols/auth/types/mod.auth.admin_manage_apps_action.md).
The user identity and the node identity hold the action by default. A setter
answers [`ack`](../primitive-types/ack.md) once the choice is saved in the
node's tree. The choice survives a restart.

For each decision, the node queries the delegate's operation as the node itself,
sends one request object and reads one object back:

* A decision object with `Allow` true accepts. A
  [`mod.apphost.app_register_decision`](../protocols/apphost/types/mod.apphost.app_register_decision.md)
  also lists the permits the node writes for the new app.
* A decision object with `Allow` false refuses.
* A delegate that cannot be reached, answers nothing within `timeout`, or
  answers any other object refuses.
* The wait also ends, and the decision refuses, when the caller of the decided
  op disconnects.
* A question already asked keeps the delegate it was asked of when the policy
  changes.

A refused decision answers the caller with the refusal message of the table
above.

## Approval apps

An approval app is an app that serves the decision ops and is named as their
delegate. The node assumes no particular approval app. Any app that serves a
decision op can be one.

An approval app obtains its identity with
[`apphost.register`](../protocols/apphost/ops/apphost.register.md), like every
other app. While the app register policy accepts every registration, the app
receives the permits it asks for. `mod.auth.admin_manage_apps_action` among them
lets the app name itself as a delegate with the setters. The user can also name
it with the node's token
([Session Identity](session-identity.md#the-nodes-token)).

Control Plane is a ready-made approval app. After it registers, Control Plane
names itself the delegate of the app register and grant request policies. The
user names it the delegate of the swarm join and swarm invite policies with the
node's token. Its specification is
[control-plane-specs `docs/node-setup.md`](https://git.satforge.dev/astralp2p/control-plane-specs/src/tag/v6.1/docs/node-setup.md#taking-the-delegation).

## After the claim

A node that is to ask before it admits takes these steps after
[Node Setup](node-setup.md):

1. The approval app registers and serves its decision ops.
2. The approval app, or the user, names it the delegate of the app register
   policy.
3. The approval app, or the user, names it the delegate of the grant request and
   swarm join policies it decides.
4. The user reviews the apps that registered before step 2, with
   [`apphost.list_tokens`](../protocols/apphost/ops/apphost.list_tokens.md) and
   [`apphost.list_grants`](../protocols/apphost/ops/apphost.list_grants.md), and
   withdraws what they hold with
   [`apphost.revoke`](../protocols/apphost/ops/apphost.revoke.md) and
   [`apphost.delete_token`](../protocols/apphost/ops/apphost.delete_token.md).

Until step 2, any local program, and any page open in a local browser, that
registers holds what it asks for
([`apphost.register`](../protocols/apphost/ops/apphost.register.md)). An app
that holds `mod.auth.admin_manage_apps_action` can call the setters and name
another delegate, so step 4 matters.

The swarm invite and contract accept policies decide only while the node has no
active contract: before the claim, and again once the active contract expires or
is cleared. A linked peer can claim an unclaimed node under the bundled swarm
invite policy ([Node Exposure](node-exposure.md#linked-peers)). A holder of
`mod.auth.admin_manage_apps_action`, such as a session with the node's token,
can delegate both policies before the claim. A delegate named while the node is
claimed stays in the tree and decides once the node is unclaimed again.

## What a delegate sees

* A [`mod.apphost.app_register_request`](../protocols/apphost/types/mod.apphost.app_register_request.md)
  carries the caller's web `Origin`, empty for a local IPC caller, so a delegate
  can refuse pages in a browser. It carries the `Name` the app gives itself,
  which the node does not verify, and the permits the app asks for on each
  record.
* A [`mod.apphost.grant_policy_request`](../protocols/apphost/types/mod.apphost.grant_policy_request.md)
  carries the `Requester` that receives the grants, its web `Origin`, the
  `Permits` and the `Duration`.
* A [`mod.user.swarm_join_request`](../protocols/user/types/mod.user.swarm_join_request.md)
  carries the `Requester`, the node that asks to join.
* A [`mod.user.swarm_invite_request`](../protocols/user/types/mod.user.swarm_invite_request.md)
  carries the `Inviter` and the offered `Contract`.
* A [`mod.user.contract_accept_request`](../protocols/user/types/mod.user.contract_accept_request.md)
  carries the `Caller` and the `Contract`.

## Reading the current policy

[`tree.get`](../protocols/tree/ops/tree.get.md) on a tree path of the table
reads a policy's delegate as a `policy.delegate` object. An absent value means
the bundled policy. `tree.get` requires
[`mod.auth.see_node_state_action`](../protocols/auth/types/mod.auth.see_node_state_action.md).
