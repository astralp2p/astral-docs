# tree.set

Set the value at a path. The value is passed as a typed object via the input stream.

## Arguments

* path (string8, required) – The path to write.
* type (string) – The object type name to use when parsing `value`; inferred from the node's current value if empty.
* value (string) – The text-encoded value to store. Defaults to empty; when empty the op enters streaming mode and reads typed objects from the input stream.
* (stream) – Typed objects to store at the path, consumed only when `value` is empty; one `ack` or `error_message` is returned per streamed object. An explicit `eos` input is answered with a final `eos`; a stream ended by EOF is not.

## Returned objects

The operation returns one of:
* An `error_message` object if there was an error.
* An `ack` object if the value was stored successfully.
* An `eos` object answering an explicit `eos` input in streaming mode.

## Examples

```shellsession
$ echo '{"Type":"bool","Object":false}' | astral-query tree.set -path /mod/tcp/settings/listen -in json -out json
{"Type":"ack","Object":null}
```

```shellsession
$ echo '{"Type":"string8","Object":"hello"}' | astral-query tree.set -path /tmp/mykey -in json -out json
{"Type":"ack","Object":null}
```

```shellsession
$ astral-query tree.set -path /tmp/mykey -type string8 -value hello -out json
{"Type":"ack","Object":null}
```
