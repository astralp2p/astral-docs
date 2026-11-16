# apphost.set_grant_request_policy

Select the delegate that decides each
[`apphost.request_grant`](apphost.request_grant.md) call. A stored delegate
decides each request in an operation of another identity. Without a stored
delegate, the config value `policies.grant_request` in `apphost.yaml` decides:
`accept_all`, `reject_all` or a delegate. The code default is `reject_all`
([Node Policies, Config values](../../../topics/node-policies.md#config-values)).

The caller must hold
[`mod.auth.configure_node_state_action`](../../auth/types/mod.auth.configure_node_state_action.md).
The user, the node and the node's [manager](../../sys/README.md#manager) hold
it. The operation answers an `error_message` reading `not permitted` before the
policy is changed when the caller does not hold it.

Naming `identity` and `operation` delegates the decision. Omitting both clears
the delegate, and the config value decides again. `timeout` is then ignored.
Naming one alone is an error. The delegate is persisted in the node's tree at
`/mod/apphost/policy/grant_request`, and the operation answers `ack` only once
it is saved. The grant request policy is independent of the policy
[`apphost.set_app_register_policy`](apphost.set_app_register_policy.md)
selects.

For each request under a delegate, the node queries `operation` on `identity`
as itself, sends one
[`mod.apphost.grant_policy_request`](../types/mod.apphost.grant_policy_request.md),
and reads one object back. The delegate answers with a
[`mod.apphost.grant_decision`](../types/mod.apphost.grant_decision.md). A
delegate that cannot be reached, answers nothing within `timeout`, or answers
any other object refuses the request. The wait also ends, and the request is
refused, when the `apphost.request_grant` caller disconnects. A question
already asked keeps the delegate it was asked of when the policy changes.

[Node Policies](../../../topics/node-policies.md) compares the five
admission policies and describes approval apps.

## Arguments

* identity (string8) – The identity whose operation decides grant requests,
  given as a hex public key or a name resolved via the directory. The node's
  own identity is refused.
* operation (string8) – The operation the node queries on `identity` for each
  request (e.g. `control.decide`).
* timeout (duration) – How long the node waits for one answer of the delegate.
  Omitted, zero, or negative waits 10 minutes. A value above 10 minutes is
  refused.

## Returned objects

The operation returns one of:
* An `error_message` object reading `unknown argument: mode` if the query names
  `mode`. The policy is not changed.
* An `error_message` object if `identity` does not resolve.
* An `error_message` object reading `the node cannot be its own delegate` if
  `identity` resolves to the node.
* An `error_message` object reading `policy delegate: no identity named` if
  `operation` is given without `identity`, or `identity` is `anyone`.
* An `error_message` object reading `policy delegate: no operation named` if
  `identity` is given without `operation`.
* An `error_message` object reading `policy delegate: timeout above 10m0s` if
  `timeout` is above 10 minutes.
* An `error_message` object if the choice was not saved.
* An `ack` object if the choice was saved.

## Examples

Delegating grant request decisions:

```shellsession
$ astral-query apphost.set_grant_request_policy -identity 0282fee8775757cdd8fda8b220195f5b8611312cd145c5a1a3aa55df210e779b2c -operation control.decide -timeout 5m -out json
{"Type":"ack","Object":null}
```

Clearing the delegate, after which the config value decides:

```shellsession
$ astral-query apphost.set_grant_request_policy -out json
{"Type":"ack","Object":null}
```
