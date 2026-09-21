# mod.objects.probe

The result of probing an object: its astral type (if any), MIME type, host repository, read latency, and `Object ID`.

## Fields

* Type (string8) – The astral type name, or empty if the payload has no astral stamp.
* Repo (string8) – Name of the repository the object was found in.
* Mime (string8) – Detected MIME type of the first bytes (via Go's `http.DetectContentType`).
* Time (duration) – Time taken to fetch the probe sample, in nanoseconds.
* ObjectID (object_id.sha256, optional) – The `Object ID` of the probed object. It carries the object's `Size`, also when the probe named a [`Partial Object ID`](../../../core-definitions/object-id.md). For the [`Empty Object`](../../../core-definitions/object.md) its `Size` is 0. A node sets it on every successful probe. A probe without it comes from a node that does not report it.

## Example

```json
{
  "Type": "mod.objects.probe",
  "Object": {
    "Type": "string8",
    "Repo": "local",
    "Mime": "text/plain; charset=utf-8",
    "Time": 421000,
    "ObjectID": "data1aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
  }
}
```
