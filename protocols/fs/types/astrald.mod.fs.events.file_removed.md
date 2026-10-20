# astrald.mod.fs.events.file_removed

Describes a tracked file that is no longer present in a watched repository. The type is registered, but no node emits it.

## Fields

* Path (string16) – Filesystem path of the removed file.
* ObjectID (object_id.sha256) – Object ID the file held before removal.

## Example

```json
{
  "Type": "astrald.mod.fs.events.file_removed",
  "Object": {
    "Path": "/data/myrepo/photo.jpg",
    "ObjectID": "data1b7s3jaxhj67biqz8ffkwrsaertjw81jfeostx3xgj73cdx43kskxi"
  }
}
```
