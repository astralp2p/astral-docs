# astrald.mod.fs.events.file_added

Describes a new file detected in a watched repository. The type is registered, but no node emits it.

## Fields

* Path (string16) – Filesystem path of the added file.
* ObjectID (object_id.sha256) – Object ID assigned to the new file.

## Example

```json
{
  "Type": "astrald.mod.fs.events.file_added",
  "Object": {
    "Path": "/data/myrepo/photo.jpg",
    "ObjectID": "data1b7s3jaxhj67biqz8ffkwrsaertjw81jfeostx3xgj73cdx43kskxi"
  }
}
```
