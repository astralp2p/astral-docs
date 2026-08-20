# objects.describe

Collect descriptors for an object from all registered describers.

The caller must hold
[`mod.auth.see_objects_action`](../../auth/types/mod.auth.see_objects_action.md).
The query is rejected before any repository is opened when the caller is not
authorized, and a refused caller receives no bytes.

## Arguments

* id (object_id.sha256, required) – The id to describe.
* zone (zone) – Zone filter for describer lookups. Defaults to all zones.
* only (string8) – Comma-separated list of descriptor object types to include.
* except (string8) – Comma-separated list of descriptor object types to exclude.
* out (string8) – Output format.

## Returned objects

The operation returns a stream of `mod.objects.describe_result` objects (one per descriptor) followed by an `eos` object. The describe context has a one-minute timeout.

## Examples

```shellsession
$ astral-query objects.describe -id data1aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa -out json
{"Type":"mod.objects.describe_result","Object":{"SourceID":"02bef8840eb35ef2ae3c83c07cb5779278904f99cb4103f71e37cc69931ae5e15f","ObjectID":"data1aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa","Data":{"Type":"string8","Object":"hello"}}}
{"Type":"eos","Object":null}
```

```shellsession
$ astral-query objects.describe -id data1aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa -only mod.objects.repository_info -out json
{"Type":"eos","Object":null}
```
