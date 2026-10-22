# inference.message

One turn of a conversation.

`Role` is passed through as-is: "system", "user" and "assistant" are the three
every provider understands. A conversation is the ordered list of messages in a
request.

## Fields

* Role (string8) – "system", "user" or "assistant".
* Parts ([]inference.content_part) – The content of this turn, in order.

## Example

```json
{
  "Type": "inference.message",
  "Object": {
    "Role": "user",
    "Parts": [
      {"Kind": "text", "Text": "what is in this picture?"},
      {"Kind": "image", "Media": {"Kind": "url", "URL": "https://example.test/cat.jpg", "MIME": "image/jpeg"}}
    ]
  }
}
```
