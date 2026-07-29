# nearby.broadcast

Triggers an immediate broadcast of the local node's status to nearby peers. The op is a no-op when the module is in silent mode; in stealth mode the broadcast is suppressed unless at least one attachment is present.

## Arguments

* out (string, optional) – Output encoding format. Defaults to the channel default.

## Returned objects

The operation returns one of:
* An `error_message` object if the broadcast fails.
* An `ack` object on success.

## Examples

```shellsession
$ astral-query nearby.broadcast -out json
{"Type":"ack","Object":{}}
```
