# mod.user.entry_verdict

What the merge check decides about an entry offered to SwarmState.

The wire form is a `string8` holding the word itself. The text form is the word verbatim; JSON encodes the type as that same string. The empty word, and any word not listed below, is not a valid value.

## Values

| Value | Meaning |
|-------|---------|
| `accept` | Store the entry and pass it on. |
| `drop` | Never store the entry and never pass it on. |
| `wait` | Hold the entry and check it again after the next merge. |

## Example

```json
{
  "Type": "mod.user.entry_verdict",
  "Object": "wait"
}
```
