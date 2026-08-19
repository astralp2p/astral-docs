# user.assets

Stream the list of object IDs currently held in this user's asset list. The
caller must hold `mod.user.see_swarm_action`; rejected with code `4` otherwise.

## Arguments

This operation takes no arguments.

## Returned objects

The operation streams one `object_id` per asset, then an `eos`. An
`error_message` is returned instead if encoding fails.

## Examples

```shellsession
$ astral-query user.assets -out json
{"Type":"object_id","Object":"id1...."}
{"Type":"object_id","Object":"id2...."}
{"Type":"eos","Object":""}
```
