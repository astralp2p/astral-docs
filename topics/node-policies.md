# Node Policies

A node decides what it lets in at two levels. The gate decides which
operations are open at all, by whether the caller has a token and what state
the node is in. The admission policies decide the questions that need an
answer each time: may this app register, may this node join the swarm, should
this node accept that invitation. [Node Setup](node-setup.md) explains the
node states and the manager this page relies on.

## The gate

apphost passes every query of an IPC, WebSocket or HTTP session through the
gate before routing it ([apphost, Gate](../protocols/apphost/README.md#gate)).
`gate` in `apphost.yaml` holds two kinds of list:

* `gate.tokenless` – the operations a session without a token may call. Such a
  session reaches the node only, never an app: a query without a token runs
  with the node's own authority, and an app must never receive a query nobody
  authenticated.
* `gate.states.fresh`, `gate.states.unclaimed`, `gate.states.claimed` – the
  operations any query to the node may call in that state, with a token or
  without.

A session without a token needs the operation on both lists. A query with a
token to another identity, such as an app, passes the gate. An entry is an
operation path, or `*`, which matches every operation; no other entry is a
pattern. The gate refuses an IPC or WebSocket query with `error_msg{denied}`
and an HTTP query with status `403`. An operation the gate admits still checks
the caller's authorization itself.

What a session reaches under the default lists:

| State | Without a token | With a token, the node's token included |
|-------|-----------------|-----------------------------------------|
| `fresh` | `.spec`, [`apphost.register_manager`](../protocols/apphost/ops/apphost.register_manager.md), [`user.info`](../protocols/user/ops/user.info.md) | the same |
| `unclaimed` | `.spec`, `user.info`, [`apphost.register`](../protocols/apphost/ops/apphost.register.md) | `.spec`, `user.info`, [`user.derive_identity`](../protocols/user/ops/user.derive_identity.md), [`user.bootstrap`](../protocols/user/ops/user.bootstrap.md), [`user.join`](../protocols/user/ops/user.join.md), `apphost.register` |
| `claimed` | `.spec`, `apphost.register`, `apphost.register_manager`, `user.info` | every operation |

A list the file supplies replaces the default list, and an omitted list keeps
its default. `allow_anonymous` and `anonymous_allowlist` are removed, and a
file that names either stops the node at startup.

## The five policies

| Policy | Decides | Setter | Tree path | Request | Decision | Refusal |
|--------|---------|--------|-----------|---------|----------|---------|
| App register | each [`apphost.register`](../protocols/apphost/ops/apphost.register.md) | [`apphost.set_app_register_policy`](../protocols/apphost/ops/apphost.set_app_register_policy.md) | `/mod/apphost/policy/app_register` | [`mod.apphost.app_register_request`](../protocols/apphost/types/mod.apphost.app_register_request.md) | [`mod.apphost.app_register_decision`](../protocols/apphost/types/mod.apphost.app_register_decision.md) | `registration declined` |
| Grant request | each [`apphost.request_grant`](../protocols/apphost/ops/apphost.request_grant.md) | [`apphost.set_grant_request_policy`](../protocols/apphost/ops/apphost.set_grant_request_policy.md) | `/mod/apphost/policy/grant_request`, and the mode at `/mod/apphost/policy/grant_request_mode` | [`mod.apphost.grant_policy_request`](../protocols/apphost/types/mod.apphost.grant_policy_request.md) | [`mod.apphost.grant_decision`](../protocols/apphost/types/mod.apphost.grant_decision.md) | `grant declined` |
| [Swarm](../core-definitions/swarm.md) join | each [`user.request_membership`](../protocols/user/ops/user.request_membership.md), the request of a node that joins this node's swarm | [`user.set_swarm_join_policy`](../protocols/user/ops/user.set_swarm_join_policy.md) | `/mod/user/policy/swarm_join` | [`mod.user.swarm_join_request`](../protocols/user/types/mod.user.swarm_join_request.md) | [`mod.user.swarm_join_decision`](../protocols/user/types/mod.user.swarm_join_decision.md) | `request declined` |
| Swarm invite | each [`user.accept_membership`](../protocols/user/ops/user.accept_membership.md), an invitation to a node without an active contract | [`user.set_swarm_invite_policy`](../protocols/user/ops/user.set_swarm_invite_policy.md) | `/mod/user/policy/swarm_invite` | [`mod.user.swarm_invite_request`](../protocols/user/types/mod.user.swarm_invite_request.md) | [`mod.user.swarm_invite_decision`](../protocols/user/types/mod.user.swarm_invite_decision.md) | `invitation declined` |
| Contract accept | each [`user.accept_contract`](../protocols/user/ops/user.accept_contract.md), a signed contract the node activates | [`user.set_contract_accept_policy`](../protocols/user/ops/user.set_contract_accept_policy.md) | `/mod/user/policy/contract_accept` | [`mod.user.contract_accept_request`](../protocols/user/types/mod.user.contract_accept_request.md) | [`mod.user.contract_accept_decision`](../protocols/user/types/mod.user.contract_accept_decision.md) | `contract declined` |

The node decides the app register, swarm join and swarm invite policies in
this order:

1. A stored delegate decides.
2. Otherwise the config value decides ([Config values](#config-values)).
3. Otherwise `reject_all` decides.

The default config values are `reject_all`:

* The app register policy refuses every registration.
* The swarm join policy declines every requester.
* The swarm invite policy declines every invitation.

The grant request and contract accept policies have no config value. While
they name no delegate, the node applies the bundled policy, which accepts:

* The grant request policy grants every permit an app asks for.
* The contract accept policy accepts every contract that passes validation.

The grant request policy also has two modes, `accept_all` and `reject_all`. An
unset mode selects `accept_all`. A stored mode value other than `accept_all`
refuses every request. A stored delegate decides whatever the mode holds.

## Config values

`policies.app_register` in `apphost.yaml`, and `policies.swarm_join` and
`policies.swarm_invite` in `user.yaml`, hold the config values. A value is one
of:

* `accept_all`: the policy accepts. The app register policy writes every permit
  an app asks for,
  [`mod.auth.admin_manage_apps_action`](../protocols/auth/types/mod.auth.admin_manage_apps_action.md)
  included. The swarm join policy admits every requester. The swarm invite
  policy accepts every invitation.
* `reject_all`: the policy refuses.
* A mapping of `identity`, `operation` and `timeout`: the policy asks a
  delegate, as a stored delegate does. `identity` and `operation` are required.
  `timeout` lies in 0 to `10m`; zero waits 10 minutes. The node resolves
  `identity` at each decision. An `identity` that does not resolve refuses the
  decision.

Any other value stops the node at startup. A key the file omits keeps its
default.

```yaml
# apphost.yaml
policies:
  app_register: {identity: control-plane, operation: cp.approve_app, timeout: 5m}
```

```yaml
# user.yaml
policies:
  swarm_join: accept_all
  swarm_invite: reject_all
```

## Delegating a decision

A delegate is named in one of two ways:

* The [manager appointment](node-setup.md#appointing-the-manager) binds the
  policies the manager takes on, with the manager as their delegate, and
  clears the delegate of every other policy.
* A setter names a delegate at any later time.

A setter takes `identity` and `operation`, and an optional `timeout`:

* `identity` names the delegate, as a hex public key or a name the directory
  resolves. The setter refuses the node's own identity and `anyone`.
* `operation` names the op the node queries on the delegate, such as
  `apphost.decide_app_register`.
* `timeout` bounds the wait for one answer. Omitted, zero or negative waits 10
  minutes. A value above 10 minutes is refused.
* `mode`, taken by `apphost.set_grant_request_policy` alone, selects
  `accept_all` or `reject_all`. A mode is given without `identity`,
  `operation` and `timeout`. A mode clears the delegate, and a delegate clears
  the mode.
* A setter without `identity` and `operation`, and for the grant request policy
  without `mode`, clears the delegate. The app register, swarm join and swarm
  invite policies then apply the config value. The grant request and contract
  accept policies apply the bundled policy.

Every setter requires
[`mod.auth.admin_manage_apps_action`](../protocols/auth/types/mod.auth.admin_manage_apps_action.md),
or a caller that is the node's
[manager](../protocols/apphost/README.md#manager). The user identity and the
node identity hold the action by default. The default gate admits the setters
on a `claimed` node only, so before the claim only the manager appointment
binds a delegate. A setter answers [`ack`](../primitive-types/ack.md) once the
choice is saved in the node's tree. The choice survives a restart.

For each decision, the node queries the delegate's operation as the node itself,
sends one request object and reads one object back:

* A decision object with `Allow` true accepts. A
  [`mod.apphost.app_register_decision`](../protocols/apphost/types/mod.apphost.app_register_decision.md)
  also lists the permits the node writes for the new app. It refuses even with
  `Allow` true when an entry in its `Authorizers` is null, invalid or names an
  `Actor`.
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

On a `fresh` node, an approval app becomes the node's manager with
[`apphost.register_manager`](../protocols/apphost/ops/apphost.register_manager.md)
and binds the policies it decides
([Node Setup, The manager](node-setup.md#the-manager)). The manager then calls
the setters without `mod.auth.admin_manage_apps_action`.

On a node that is not `fresh`, an approval app obtains its identity with
[`apphost.register`](../protocols/apphost/ops/apphost.register.md), like every
other app. The register policy decides the registration. A holder of
`mod.auth.admin_manage_apps_action`, such as the user or a session with the
node's token ([Session Identity](session-identity.md#the-nodes-token)), names
the app a delegate with the setters.

Control Plane is a ready-made approval app. Its specification at
[control-plane-specs v6.1 `docs/node-setup.md`](https://git.satforge.dev/astralp2p/control-plane-specs/src/tag/v6.1/docs/node-setup.md#taking-the-delegation)
predates the manager appointment: it takes the delegation with the setters.

## Before the claim

A node that is to ask before it admits takes these steps:

1. The approval app calls `apphost.register_manager` on the `fresh` node and
   binds the policies it decides. The node is then `unclaimed`.
2. The approval app serves its decision ops.
3. The approval app claims the node with
   [`user.bootstrap`](../protocols/user/ops/user.bootstrap.md) or
   [`user.join`](../protocols/user/ops/user.join.md) under its App token
   ([User and Swarm](user-and-swarm.md#claiming-a-node)).

A policy the appointment does not bind applies its config value or its bundled
policy. The grant request policy then grants every permit an app with a token
asks for with
[`apphost.request_grant`](../protocols/apphost/ops/apphost.request_grant.md),
once the node is `claimed` and the gate admits the query.

The swarm invite and contract accept policies decide only while the node has no
active contract: before the claim, and again once the active contract is
cleared, as after an expulsion or at a start that finds it expired. A running
node keeps an expired active contract until it restarts. A linked peer reaches
`user.accept_membership` on a node without an active contract; the default
swarm invite policy declines its invitation
([Node Exposure](node-exposure.md#linked-peers)). A delegate named while the
node is claimed stays in the tree and decides once the node has no active
contract again.

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

[`tree.get`](../protocols/tree/ops/tree.get.md) on a delegate path of the table
reads a policy's delegate as a `policy.delegate` object, and on
`/mod/apphost/policy/grant_request_mode` reads the grant request mode as a
`string8`. An absent delegate means the config value for the app register,
swarm join and swarm invite policies, and the bundled policy for the contract
accept policy. For the grant request policy, an absent delegate leaves the
decision to the mode. `tree.get` does not read the config values.
`tree.get` requires
[`mod.auth.see_node_state_action`](../protocols/auth/types/mod.auth.see_node_state_action.md).

## Distribution and test configuration

The defaults are the distribution configuration. A node needs no
`apphost.yaml` or `user.yaml` for it:

```yaml
# apphost.yaml
gate:
  tokenless: [.spec, apphost.register, apphost.register_manager, user.info]
  states:
    fresh: [.spec, apphost.register_manager, user.info]
    unclaimed: [.spec, user.info, user.derive_identity, user.bootstrap, user.join, apphost.register,
                apphost.bind, apphost.register_handler, apphost.cancel]
    claimed: ["*"]
policies:
  app_register: reject_all
```

```yaml
# user.yaml
policies:
  swarm_join: reject_all
  swarm_invite: reject_all
```

The only way forward from `fresh` is the manager appointment. The claim
operations need a token, which the manager holds after its appointment.

A test node claims without a manager, and every admission policy accepts. The
astrald end-to-end tests run every node with this configuration:

```yaml
# apphost.yaml
gate:
  tokenless: [.spec, apphost.register, user.info, user.derive_identity, user.bootstrap, user.join]
  states:
    fresh: ["*"]
policies:
  app_register: accept_all
```

```yaml
# user.yaml
policies:
  swarm_join: accept_all
  swarm_invite: accept_all
```

* A session without a token calls `user.bootstrap` or `user.join` on a `fresh`
  node and claims it in one query. `apphost.register_manager` is not on the
  `tokenless` list, so a test that appoints a manager calls it with the node's
  token.
* The `unclaimed` and `claimed` lists keep their defaults.
* Under `accept_all`, any local program, or any page open in a local browser,
  that registers holds every permit it asks for. This configuration does not
  belong on a node a user owns.
