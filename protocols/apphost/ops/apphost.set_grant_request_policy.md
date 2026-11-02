# apphost.set_grant_request_policy

Select the policy that decides each
[`apphost.request_grant`](apphost.request_grant.md) call. The node applies one
of three modes: `accept_all` approves every request, `reject_all` refuses every
request, and a delegate decides each request in an operation of another
identity. Unset selects `reject_all`.

The caller must hold
[`mod.auth.admin_manage_apps_action`](../../auth/types/mod.auth.admin_manage_apps_action.md).
The operation answers an `error_message` reading `not permitted` before the
policy is changed when the caller is not authorized.

`mode` selects `accept_all` or `reject_all` and clears the delegate. Under
`accept_all`, any app with a token grants itself any action it names; only the
permit check of [Grants](../README.md#grants) refuses a request. `mode` is
given without `identity`, `operation` and `timeout`.

Naming `identity` and `operation` delegates the decision and clears the mode.
Naming one alone is an error. Omitting `mode`, `identity` and `operation`
clears both the delegate and the mode and restores `reject_all`, and `timeout`
is then ignored.

The delegate is persisted in the node's tree at
`/mod/apphost/policy/grant_request` and the mode at
`/mod/apphost/policy/grant_request_mode`. The operation answers `ack` only once
the choice is saved. A stored delegate decides whatever the mode holds, so a
delegate stored before the modes existed keeps deciding. Setting a mode clears
the delegate before it writes the mode, so a failed mode write leaves no
delegate in force. The grant request policy is independent of the policy
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

[Policy Delegates](../../../topics/policy-delegates.md) compares the five
admission policies and describes approval apps.

## Arguments

* mode (string8) – `accept_all` or `reject_all`.
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
* An `error_message` object reading `unknown mode: <mode>` if `mode` is neither
  `accept_all` nor `reject_all`.
* An `error_message` object reading `give mode or a delegate, not both` if
  `mode` is given with `identity` or `operation`.
* An `error_message` object reading `unknown argument: timeout` if `mode` is
  given with `timeout`.
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

Approving every request that passes the permit check:

```shellsession
$ astral-query apphost.set_grant_request_policy -mode accept_all -out json
{"Type":"ack","Object":null}
```

Refusing every request:

```shellsession
$ astral-query apphost.set_grant_request_policy -mode reject_all -out json
{"Type":"ack","Object":null}
```

Delegating grant request decisions:

```shellsession
$ astral-query apphost.set_grant_request_policy -identity 0282fee8775757cdd8fda8b220195f5b8611312cd145c5a1a3aa55df210e779b2c -operation control.decide -timeout 5m -out json
{"Type":"ack","Object":null}
```

Restoring the default policy, `reject_all`:

```shellsession
$ astral-query apphost.set_grant_request_policy -out json
{"Type":"ack","Object":null}
```
