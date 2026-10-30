# inference.media_ref

Where one media part's bytes come from.

Three sources, for three situations. **Inline** carries the bytes in the request,
which is right for a picture a caller already holds, such as a screenshot it
just took. **Object** names an object the astral network already addresses; the
provider reads it through
[`objects.read`](../../objects/ops/objects.read.md), so media that is already on
the network is never transported twice, and a caller can reuse an asset it
stored once. **URL** names an address the provider fetches itself, which is right
for a resource that lives on the open web and should not pass through the
caller.

`Data` is a `bytes32`: a screenshot or a photo is commonly several megabytes,
far past what a 64 KiB field holds.

A provider may refuse any of the three, and may bound how many bytes it takes:
one that cannot reach the open web refuses `url`, one with no object access
refuses `object`. A refusal is an
[`inference.error`](inference.error.md) of Kind "bad_request" naming the part,
not a silent omission.

## Fields

* Kind (string8) – One of "inline", "object" or "url".
* Data (bytes32) – The bytes, when `Kind` is "inline".
* ObjectID (object_id.sha256) – The object, when `Kind` is "object".
* URL (string16) – The address, when `Kind` is "url".
* MIME (string8) – The media type, e.g. "image/png". Required for inline data, helpful otherwise.

## Example

Media already on the network, referenced rather than uploaded:

```json
{
  "Type": "inference.media_ref",
  "Object": {
    "Kind": "object",
    "Data": "",
    "ObjectID": "data1aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
    "URL": "",
    "MIME": "image/jpeg"
  }
}
```
