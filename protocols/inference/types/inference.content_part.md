# inference.content_part

One piece of a message: either text, or media of one kind.

Parts are ordered, and the order is what the model sees. A message that carries
a picture and a question sends both, in that order.

`Text` is a `string32`. A part often carries a whole file or a long tool
result, and a 64 KiB cap would cut those off or split them across parts the
model then reads as separate pieces.

## Fields

* Kind (string8) – One of "text", "image", "audio" or "video".
* Text (string32) – The text, when `Kind` is "text".
* Media (optional inference.media_ref) – Where the bytes come from, for the media kinds; absent for text.

## Example

```json
{
  "Type": "inference.content_part",
  "Object": {
    "Kind": "image",
    "Text": "",
    "Media": {"Kind": "object", "ObjectID": "data1aaaa…", "MIME": "image/png"}
  }
}
```
