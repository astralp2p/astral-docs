# objects.search

Run a search query across registered searchers. The query string follows the `objects.search_query` grammar (bare words, `tag:value`, `-tag:value`, `?tag:value`, `~tag:value`).

The caller must hold
[`mod.auth.see_objects_action`](../../auth/types/mod.auth.see_objects_action.md).
The query is rejected before any repository is opened when the caller is not
authorized, and a refused caller receives no bytes.

## Arguments

* q (string, required) – The search query.
* repo (string8) – If set, only matches whose objects exist in this repository are returned.
* zone (zone) – Zone filter for the search context. Defaults to all zones.
* out (string8) – Output format.

## Returned objects

The operation returns one of:
* An `error_message` object if the repository is not found or the search fails to start.
* A stream of `mod.objects.search_result` objects (deduplicated by object id) followed by an `eos` object. The search context has a one-minute timeout.

## Examples

```shellsession
$ astral-query objects.search -q 'mime:text/plain hello' -out json
{"Type":"mod.objects.search_result","Object":{"SourceID":"02bef8840eb35ef2ae3c83c07cb5779278904f99cb4103f71e37cc69931ae5e15f","ObjectID":"data1aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"}}
{"Type":"eos","Object":null}
```
