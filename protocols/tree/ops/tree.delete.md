# tree.delete

Delete the value at a path.

## Arguments

* path (string8, required) – The path to delete.
* recursive (bool) – Delete the node and all of its subnodes depth-first. Defaults to false.

## Returned objects

The operation returns one of:
* An `error_message` object if the path does not exist or there was an error.
* An `ack` object if the value was deleted successfully.

## Examples

```shellsession
$ astral-query tree.delete -path /tmp/mykey -out json
{"Type":"ack","Object":null}
```

```shellsession
$ astral-query tree.delete -path /tmp/mydir -recursive true -out json
{"Type":"ack","Object":null}
```
