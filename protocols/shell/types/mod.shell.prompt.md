# mod.shell.prompt

The command prompt of a [`shell.shell`](../ops/shell.shell.md) session: the
identity the session runs as and the node serving it.

The session never sends this object as a typed object. Before reading each
command line it renders the prompt as text on the raw stream, in the form
`<GuestID>@<HostID>> `, with each identity shown by its display name in the
node's directory. The type is registered, so it has a binary encoding,
and [`objects.new`](../../objects/ops/objects.new.md) returns its zero value.

## Fields

* GuestID (identity) – Identity the session runs as: the caller, or the identity named by the `as` argument.
* HostID (identity) – Identity of the node serving the session.

## Example

```json
{
  "Type": "mod.shell.prompt",
  "Object": {
    "GuestID": "0282fee8775757cdd8fda8b220195f5b8611312cd145c5a1a3aa55df210e779b2c",
    "HostID": "02bef8840eb35ef2ae3c83c07cb5779278904f99cb4103f71e37cc69931ae5e15f"
  }
}
```
