# objects.scan

Stream the ids of every object in a repository, optionally following live additions.

The caller must hold
[`mod.auth.see_objects_action`](../../auth/types/mod.auth.see_objects_action.md).
The query is rejected before any repository is opened when the caller is not
authorized, and a refused caller receives no bytes.

## Arguments

* repo (string8, required) – Repository to scan.
* follow (bool) – If true, keep the operation open and stream new ids as they are added.
* zone (zone) – Zone filter for the scan context. Defaults to all zones.
* out (string8) – Output format.

## Returned objects

The operation returns one of:
* An `error_message` object if the repository is not found or the scan cannot start.
* A stream of `object_id.sha256` objects followed by an `eos` object (or kept open in `follow` mode).

## Examples

```shellsession
$ astral-query objects.scan -repo local -out json
{"Type":"object_id.sha256","Object":"data1aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"}
{"Type":"object_id.sha256","Object":"data1bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"}
{"Type":"eos","Object":null}
```
