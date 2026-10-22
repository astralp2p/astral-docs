# inference.content_part

One piece of a message: either text, or media of one kind.

Parts are ordered, and the order is what the model sees. A message that carries
a picture and a question sends both, in that order.

## Fields

* Kind (string8) – One of "text", "image", "audio" or "video".
* Text (string16) – The text, when `Kind` is "text".
* Media (inference.media_ref) – Where the bytes come from, for the media kinds.

## Example

```json
{
  "Type": "inference.content_part",
  "Object": {
    "Kind": "image",
    "Media": {"Kind": "object", "ObjectID": "data1aaaa…", "MIME": "image/png"}
  }
}
```
