# coldcard.scan

Scan for connected Coldcard hardware wallets and update the module's device state.

The caller must hold
[`mod.coldcard.scan_action`](../types/mod.coldcard.scan_action.md). The
operation answers an `error_message` reading `not permitted` before any device
is scanned when the caller is not authorized.

## Arguments

* in (string8) – Input format.
* out (string8) – Output format.

## Returned objects

The operation returns one of:
* An `error_message` object if the scan fails.
* An `ack` object on success.

## Examples

```shellsession
$ astral-query coldcard.scan -out json
{"Type":"ack","Object":null}
```
