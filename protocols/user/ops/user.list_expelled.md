# user.list_expelled

Stream all signed expulsions issued by the active contract's issuer, terminated by `eos`. The caller must hold `mod.user.see_swarm_action`. Rejected with code `2` if the node has no active contract, and with code `4` if the caller is not authorized.

## Arguments

This operation takes no arguments.

## Returned objects

The operation returns one of:
* An `error_message` object if fetching expulsions or encoding fails.
* A `mod.user.signed_expulsion` object for each ban on record.
* An `eos` object terminating the stream.

## Examples

```shellsession
$ astral-query user.list_expelled -out json
{"Type":"mod.user.signed_expulsion","Object":{...}}
{"Type":"eos","Object":""}
```
