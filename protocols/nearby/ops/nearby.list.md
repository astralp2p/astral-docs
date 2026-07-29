# nearby.list

Returns the current cached set of nearby nodes as a stream of `mod.nearby.status` objects, one per known peer, terminated by `eos`. Expired cache entries are pruned before iteration.

## Arguments

* out (string, optional) – Output encoding format. Defaults to the channel default.

## Returned objects

The operation returns one of:
* A `mod.nearby.status` object for each cached nearby peer.
* An `eos` object terminating the stream.

## Examples

```shellsession
$ astral-query nearby.list -out json
{"Type":"mod.nearby.status","Object":{"Identity":"<identity>","Attachments":{...}}}
{"Type":"eos","Object":{}}
```
