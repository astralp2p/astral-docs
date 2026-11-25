# mod.user.request_status

The status of a request in SwarmState. It is derived from the stored entries
and never stored itself.

The wire form is a `string8` holding the word itself. The text form is the word verbatim; JSON encodes the type as that same string. The empty word, and any word not listed below, is not a valid value.

## Values

| Value | Meaning |
|-------|---------|
| `declined` | A decline of the request exists. It beats any approval. |
| `approved` | An approval of the request exists and no decline. |
| `expired` | No answer exists and the request's Timeout has passed. |
| `pending` | No answer exists and the Timeout has not passed. |

When more than one applies, the first listed wins.

## Example

```json
{
  "Type": "mod.user.request_status",
  "Object": "pending"
}
```
