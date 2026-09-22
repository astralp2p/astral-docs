# objects.find

Find identities that can provide a given object.

The caller must hold
[`mod.auth.see_objects_action`](../../auth/types/mod.auth.see_objects_action.md).
The query is rejected before any repository is opened when the caller is not
authorized, and a refused caller receives no bytes.

## Arguments

* id (object_id.sha256, required) – The id to look up.
* zone (zone) – Zone filter for finder lookups. Defaults to all zones.
* out (string8) – Output format.

The `id` can be a
[`Partial Object ID`](../../../core-definitions/object-id.md). The operation
reads no repository, so it resolves no `Partial Object ID` before the fan-out.
Every `Finder` receives the `id` as given.

A `Finder` decides for itself whether it matches by `Hash` alone. A `Finder`
that matches an `Object ID` exactly contributes nothing to a call carrying a
`Partial Object ID`. A `Finder` contributing nothing does not fail the
operation, which streams the identities the other finders returned.

## Returned objects

The operation returns one of:
* An `error_message` object if `id` is missing/zero or the lookup fails.
* A stream of `identity` objects (deduplicated by string form) followed by an `eos` object. The lookup context has a one-minute timeout.

## Examples

```shellsession
$ astral-query objects.find -id data1aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa -out json
{"Type":"identity","Object":"02bef8840eb35ef2ae3c83c07cb5779278904f99cb4103f71e37cc69931ae5e15f"}
{"Type":"eos","Object":null}
```
