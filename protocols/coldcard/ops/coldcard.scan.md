# coldcard.scan

Enumerate the attached Coldcard hardware wallets now, read each device's key, and
update the keys the app claims. The query targets the app's identity.

The caller must be the local [`User`](../../../core-definitions/user.md) or the local
[`Node`](../../../core-definitions/node.md). The operation answers an `error_message`
reading `not permitted` before any device is scanned when it is not.

## Arguments

* in (string8) – Input format.
* out (string8) – Output format.

## Returned objects

The operation returns one of:
* An `error_message` object if the scan fails.
* An `ack` object on success.

## Examples

```shellsession
$ astral-query app-identity:coldcard.scan -out json
{"Type":"ack","Object":null}
```
