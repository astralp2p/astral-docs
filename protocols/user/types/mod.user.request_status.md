# mod.user.request_status

The status of a request in SwarmState. It is derived from the stored entries
and never stored itself.

The wire form is a `string8` holding the word itself. The text form is the word verbatim; JSON encodes the type as that same string. The empty word, and any word not listed below, is not a valid value.

## Values

| Value | Meaning |
|-------|---------|
| `fulfilled` | A contract with both signatures names the request as its `RequestID`. Nothing that follows changes it. |
| `declined` | A decline of the request exists. It closes the request. |
| `approved` | A counting approval of an expel request exists, or the user key's expulsion of the request's subject, and no decline. Only an expel request is `approved`. |
| `expired` | The request's Timeout has passed, and no earlier value applies. |
| `offered` | A valid offer for the request exists, and the Timeout has not passed. |
| `pending` | No answer exists and the Timeout has not passed. |

When more than one applies, the first listed wins.

## Example

```json
{
  "Type": "mod.user.request_status",
  "Object": "pending"
}
```
