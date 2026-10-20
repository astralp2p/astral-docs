# astrald.mod.fs.events.file_changed

Describes a change to a tracked file's content, carrying the old and new object IDs. The type is registered, but no node emits it.

## Fields

* Path (string16) – Filesystem path of the changed file.
* OldID (object_id.sha256) – Object ID of the file before the change.
* NewID (object_id.sha256) – Object ID of the file after the change.

## Example

```json
{
  "Type": "astrald.mod.fs.events.file_changed",
  "Object": {
    "Path": "/data/myrepo/document.pdf",
    "OldID": "data1b7ec14scdw5wgzt1s87k6zsptyru4h736cipq9mxymwg8m8pnfxyr",
    "NewID": "data1b7isekopamcgm6tqonihrmc35cye5enj7a5zsepobtt16hekje6ek"
  }
}
```
