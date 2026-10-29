# user.set_contract_accept_policy

Select the policy that decides each contract
[`user.accept_contract`](user.accept_contract.md) receives. The node either
applies its default policy, which accepts every contract that passes
validation, or delegates the decision to an operation of another identity.

The caller must hold
[`mod.auth.admin_manage_apps_action`](../../auth/types/mod.auth.admin_manage_apps_action.md).
The operation answers an `error_message` reading `not permitted` before the
policy is changed when the caller is not authorized.

Naming `identity` and `operation` delegates the decision. Omitting both clears
the delegate and restores the default policy, and `timeout` is then ignored.
Naming one alone is an error. The choice is persisted in the node's tree at
`/mod/user/policy/contract_accept`, and the operation answers `ack` only once it
is saved.

For each contract, the node queries `operation` on `identity` as itself, sends
one
[`mod.user.contract_accept_request`](../types/mod.user.contract_accept_request.md),
and reads one object back. The delegate answers with a
[`mod.user.contract_accept_decision`](../types/mod.user.contract_accept_decision.md).
The wait also ends when the caller of
[`user.accept_contract`](user.accept_contract.md) disconnects. A delegate that
cannot be reached, answers nothing within `timeout`, or answers any other object
declines, and `user.accept_contract` answers an `error_message` reading
`contract declined`. A question already asked keeps the delegate it was asked of
when the policy changes.

## Arguments

* identity (string8) – The identity whose operation decides, given as a hex
  public key or a name resolved via the directory. The node's own identity is
  refused.
* operation (string8) – The operation the node queries on `identity` for
  each contract (e.g. `control.decide_contract`).
* timeout (duration) – How long the node waits for one answer. Omitted, zero,
  or negative waits 10 minutes. A value above 10 minutes is refused.

## Returned objects

The operation returns one of:
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

Delegating the decision:

```shellsession
$ astral-query user.set_contract_accept_policy -identity 0282fee8775757cdd8fda8b220195f5b8611312cd145c5a1a3aa55df210e779b2c -operation control.decide_contract -timeout 5m -out json
{"Type":"ack","Object":null}
```

Restoring the default policy:

```shellsession
$ astral-query user.set_contract_accept_policy -out json
{"Type":"ack","Object":null}
```
