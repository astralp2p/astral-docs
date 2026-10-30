# tree.get

Get the value stored at a path.

The caller must hold
[`mod.auth.see_node_state_action`](../../auth/types/mod.auth.see_node_state_action.md).
The operation answers an `error_message` reading `not permitted` before any path
is walked when the caller is not authorized.

## Arguments

* path (string8, required) – The path to read.
* follow (bool) – If true, stream updates to the value as they change (the operation stays open).

## Returned objects

The operation returns one of:
* An `error_message` object if the path does not exist or there was an error.
* A `nil` object when the path exists but holds no value; a module setting then follows the module's built-in default.
* A typed object containing the stored value, followed by an `eos` object (or a stream of updates if `follow` is true).

## Examples

```shellsession
$ astral-query tree.get -path /mod/tcp/settings/listen -out json
{"Type":"bool","Object":false}
{"Type":"eos","Object":null}
```
