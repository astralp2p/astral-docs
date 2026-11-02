# Policy Delegates

A node can delegate admission decisions to an approval app. A policy setter
names the app and its decision operation. The node then asks that operation
to approve or refuse each request.

## The five policies

| Policy | Decides | Setter |
|--------|---------|--------|
| [App](../core-definitions/app.md) register | App registration through [`apphost.register`](../protocols/apphost/ops/apphost.register.md) | [`apphost.set_app_register_policy`](../protocols/apphost/ops/apphost.set_app_register_policy.md) |
| Grant request | Additional app grants through [`apphost.request_grant`](../protocols/apphost/ops/apphost.request_grant.md) | [`apphost.set_grant_request_policy`](../protocols/apphost/ops/apphost.set_grant_request_policy.md) |
| [Swarm](../core-definitions/swarm.md) join | Another node's request to join this swarm through [`user.request_membership`](../protocols/user/ops/user.request_membership.md) | [`user.set_swarm_join_policy`](../protocols/user/ops/user.set_swarm_join_policy.md) |
| Swarm invite | An invitation for this node to join a swarm through [`user.accept_membership`](../protocols/user/ops/user.accept_membership.md) | [`user.set_swarm_invite_policy`](../protocols/user/ops/user.set_swarm_invite_policy.md) |
| Contract accept | Activation of a signed contract through [`user.accept_contract`](../protocols/user/ops/user.accept_contract.md) | [`user.set_contract_accept_policy`](../protocols/user/ops/user.set_contract_accept_policy.md) |

All five policies accept by default. The operation's validation still applies.
Under these defaults, registration and grant requests grant every requested permit,
including
[`mod.auth.admin_manage_apps_action`](../protocols/auth/types/mod.auth.admin_manage_apps_action.md).

Only the grant request policy also has modes: `accept_all` and `reject_all`.
A delegate takes precedence over the mode. Without a delegate, an unset mode
or `accept_all` accepts; any other stored value refuses every request.

## Delegating a decision

A setter takes `identity`, `operation` and an optional `timeout`:

* `identity` names the delegate by hex public key or directory name. The node's
  own identity and `anyone` are refused.
* `operation` names its decision operation, such as `apphost.decide_app_register`.
* `timeout` limits the wait for one answer. Omitted, zero or negative means
  10 minutes. Values above 10 minutes are refused.

Only `apphost.set_grant_request_policy` accepts `mode`: `accept_all` or
`reject_all`, without `identity`, `operation` or `timeout`. Setting a mode
clears the delegate; setting a delegate clears the mode. Omitting `identity`
and `operation` (and `mode` for grant requests) restores the default policy.

Every setter requires
[`mod.auth.admin_manage_apps_action`](../protocols/auth/types/mod.auth.admin_manage_apps_action.md).
The user and node identities hold this action by default. The setter saves the
choice in the node's tree, then returns [`ack`](../primitive-types/ack.md).
The choice survives restarts.

The node queries the delegate as itself, sends one request object and reads
one decision:

* `Allow: true` accepts; `Allow: false` refuses.
* An app register decision also selects the new app's permits. A null or
  invalid `Authorizers` entry, or one naming an `Actor`, refuses registration
  even with `Allow: true`.
* An unreachable delegate, a timeout or an unexpected response object refuses
  the request. The caller's disconnection also ends the wait and refuses it.
* Changing the policy does not change the delegate for a pending request.

The [decision types and refusal messages](#what-a-delegate-sees) are listed below.

## Approval apps

Any app that serves a decision operation can be a delegate. It registers with
`apphost.register` and requests `mod.auth.admin_manage_apps_action` to set
itself as delegate. The user can also set the delegate with the
[node's token](session-identity.md#the-nodes-token).

[Control Plane](https://git.satforge.dev/astralp2p/control-plane-specs/src/tag/v6.1/docs/node-setup.md#taking-the-delegation)
is one approval app. After registration, it delegates app register and grant
request decisions to itself. The user delegates swarm join and swarm invite
decisions to it with the node's token.

## After the claim

To require approval after [Node Setup](node-setup.md):

1. The approval app registers and serves its decision operations.
2. The app or user delegates app register and grant request decisions to it.
3. The app or user delegates swarm join decisions to it, if it handles joins.
4. The user reviews the apps that registered before step 2, with
   [`apphost.list_tokens`](../protocols/apphost/ops/apphost.list_tokens.md) and
   [`apphost.list_grants`](../protocols/apphost/ops/apphost.list_grants.md), and
   withdraws unwanted grants and tokens with
   [`apphost.revoke`](../protocols/apphost/ops/apphost.revoke.md) and
   [`apphost.delete_token`](../protocols/apphost/ops/apphost.delete_token.md).

Until step 2, the default policies grant requested permits to any registering
local program or browser page, and to any token holder using
`apphost.request_grant`. An app with `mod.auth.admin_manage_apps_action` can
replace the delegates. Delegation does not revoke existing grants or tokens.

The swarm invite and contract accept policies decide only while the node has no
active contract: before claim, after expulsion or after a restart clears an
expired contract. Expiry alone does not clear a running node's active contract.
A linked peer can claim an unclaimed node under the default swarm invite policy
([Node Exposure](node-exposure.md#linked-peers)). A holder of
`mod.auth.admin_manage_apps_action`, including the node's token holder, can
delegate both policies before claim. Delegates set while claimed remain stored
and decide when the node becomes unclaimed again.

## What a delegate sees

| Request | Fields | Decision | Refusal message |
|---------|--------|----------|-----------------|
| [`mod.apphost.app_register_request`](../protocols/apphost/types/mod.apphost.app_register_request.md) | `Origin`, unverified `Name`, `GrantPermits`, `ContractPermits` | [`mod.apphost.app_register_decision`](../protocols/apphost/types/mod.apphost.app_register_decision.md) | `registration declined` |
| [`mod.apphost.grant_policy_request`](../protocols/apphost/types/mod.apphost.grant_policy_request.md) | `Requester` receiving the grants, `Origin`, `Permits`, `Duration` | [`mod.apphost.grant_decision`](../protocols/apphost/types/mod.apphost.grant_decision.md) | `grant declined` |
| [`mod.user.swarm_join_request`](../protocols/user/types/mod.user.swarm_join_request.md) | `Requester` asking to join | [`mod.user.swarm_join_decision`](../protocols/user/types/mod.user.swarm_join_decision.md) | `request declined` |
| [`mod.user.swarm_invite_request`](../protocols/user/types/mod.user.swarm_invite_request.md) | `Inviter`, offered `Contract` | [`mod.user.swarm_invite_decision`](../protocols/user/types/mod.user.swarm_invite_decision.md) | `invitation declined` |
| [`mod.user.contract_accept_request`](../protocols/user/types/mod.user.contract_accept_request.md) | `Caller`, `Contract` | [`mod.user.contract_accept_decision`](../protocols/user/types/mod.user.contract_accept_decision.md) | `contract declined` |

`Origin` is the caller's web origin, empty for local IPC. A delegate can use it
to refuse browser requests. The node does not verify an app's `Name`.

## Reading the current policy

[`tree.get`](../protocols/tree/ops/tree.get.md) reads these stored values:

| Policy | Delegate path |
|--------|---------------|
| App register | `/mod/apphost/policy/app_register` |
| Grant request | `/mod/apphost/policy/grant_request` |
| Swarm join | `/mod/user/policy/swarm_join` |
| Swarm invite | `/mod/user/policy/swarm_invite` |
| Contract accept | `/mod/user/policy/contract_accept` |

Each delegate is a `policy.delegate` object.
The grant request mode is a [`string8`](../primitive-types/string8.md) at
`/mod/apphost/policy/grant_request_mode`. Unset values follow the
[default rules](#the-five-policies). Reading requires
[`mod.auth.see_node_state_action`](../protocols/auth/types/mod.auth.see_node_state_action.md).
