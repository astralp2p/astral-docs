# tree.get

Get the value stored at a path.

The caller must hold
[`mod.auth.see_node_state_action`](../../auth/types/mod.auth.see_node_state_action.md).
The query is rejected before any path is walked when the caller is not
authorized, and a refused caller receives no bytes.

## Arguments

* path (string8, required) – The path to read.
* follow (bool) – If true, stream updates to the value as they change (the operation stays open).

## Returned objects

The operation returns one of:
* An `error_message` object if the path does not exist or there was an error.
* A typed object containing the stored value, followed by an `eos` object (or a stream of updates if `follow` is true).

## Examples

```shellsession
$ astral-query tree.get -path /mod/tcp/settings/listen -out json
{"Type":"bool","Object":false}
{"Type":"eos","Object":null}
```
