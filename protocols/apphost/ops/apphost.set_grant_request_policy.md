# apphost.set_grant_request_policy

Select how the node decides
[`apphost.request_grant`](apphost.request_grant.md): `accept_all` (the default),
`reject_all`, or a delegate.

`accept_all` approves every request that passes the [permit check](../README.md#grants).
Any app with a token can obtain the permits it requests. `reject_all` refuses
every request. A delegate decides each request through its decision operation.

The caller must hold
[`mod.auth.admin_manage_apps_action`](../../auth/types/mod.auth.admin_manage_apps_action.md).
An unauthorized caller receives `error_message` reading `not permitted`;
the policy stays unchanged.

* `mode` selects `accept_all` or `reject_all` and clears the delegate. It cannot
  be combined with `identity`, `operation` or `timeout`.
* `identity` and `operation` set a delegate and clear the mode. Both are required.
* Omitting `mode`, `identity` and `operation` clears both stored values and
  restores `accept_all`. `timeout` is then ignored.

The node stores the delegate at `/mod/apphost/policy/grant_request` and the
mode at `/mod/apphost/policy/grant_request_mode`. It returns `ack` after saving.
A delegate takes precedence over any stored mode. Without a delegate, an unset
mode or `accept_all` accepts; any other stored value refuses every request.
Setting a mode clears the delegate first; a failed mode write leaves it cleared.
This policy is independent of the
[app register policy](apphost.set_app_register_policy.md).

For each delegated request, the node queries `operation` on `identity` as
itself, sends one
[`mod.apphost.grant_policy_request`](../types/mod.apphost.grant_policy_request.md),
and expects one [`mod.apphost.grant_decision`](../types/mod.apphost.grant_decision.md).
An unreachable delegate, a timeout or an unexpected response object refuses
the request. The caller's disconnection also ends the wait and refuses it.
Changing the policy does not change the delegate for a pending request.

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

Restoring the default policy, `accept_all`:

```shellsession
$ astral-query apphost.set_grant_request_policy -out json
{"Type":"ack","Object":null}
```
