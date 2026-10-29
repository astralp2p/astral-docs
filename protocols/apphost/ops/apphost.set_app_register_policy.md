# apphost.set_app_register_policy

Select the policy that decides each [`apphost.register`](apphost.register.md)
call. The node either applies its default policy, which admits every
registration with the permits it asked for, or delegates the decision to an
operation of another identity.

The caller must hold
[`mod.auth.admin_manage_apps_action`](../../auth/types/mod.auth.admin_manage_apps_action.md).
The operation answers an `error_message` reading `not permitted` before the
policy is changed when the caller is not authorized.

Naming `identity` and `operation` delegates the decision. Omitting both clears
the delegate and restores the default policy, and `timeout` is then ignored.
Naming one alone is an error. The choice is persisted in the node's tree at
`/mod/apphost/policy/app_register`, and the operation answers `ack` only once
it is saved.

For each registration, the node queries `operation` on `identity` as itself,
sends one
[`mod.apphost.app_register_request`](../types/mod.apphost.app_register_request.md),
and reads one object back. The delegate answers with a
[`mod.apphost.app_register_decision`](../types/mod.apphost.app_register_decision.md).
A delegate that cannot be reached, answers nothing within `timeout`, or answers
any other object refuses the registration. A question already asked keeps the
delegate it was asked of when the policy changes.

## Arguments

* identity (string8) – The identity whose operation decides registrations,
  given as a hex public key or a name resolved via the directory. The node's
  own identity is refused.
* operation (string8) – The operation the node queries on `identity` for each
  registration (e.g. `control.decide`).
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

Delegating registration decisions:

```shellsession
$ astral-query apphost.set_app_register_policy -identity 0282fee8775757cdd8fda8b220195f5b8611312cd145c5a1a3aa55df210e779b2c -operation control.decide -timeout 5m -out json
{"Type":"ack","Object":null}
```

Restoring the default policy:

```shellsession
$ astral-query apphost.set_app_register_policy -out json
{"Type":"ack","Object":null}
```
