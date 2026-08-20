# objects.repositories

List repositories registered with the module (network zone excluded).

The caller must hold
[`mod.auth.see_objects_action`](../../auth/types/mod.auth.see_objects_action.md).
The query is rejected before any repository is opened when the caller is not
authorized, and a refused caller receives no bytes.

## Arguments

* out (string8) – Output format.

## Returned objects

The operation returns a stream of `mod.objects.repository_info` objects (one per repository) followed by an `eos` object.

## Examples

```shellsession
$ astral-query objects.repositories -out json
{"Type":"mod.objects.repository_info","Object":{"Name":"main","Label":"World","Free":0}}
{"Type":"mod.objects.repository_info","Object":{"Name":"device","Label":"This device","Free":0}}
{"Type":"mod.objects.repository_info","Object":{"Name":"local","Label":"Local storage","Free":549755813888}}
{"Type":"mod.objects.repository_info","Object":{"Name":"memory","Label":"In-memory repos","Free":0}}
{"Type":"mod.objects.repository_info","Object":{"Name":"mem0","Label":"Default memory","Free":67108864}}
{"Type":"eos","Object":null}
```
