# mod.nodes.node_info

A compact descriptor of a node: its alias, identity, and a list of known endpoints.

## Fields

* Alias (string8) – Self-reported alias for the node.
* Identity (identity, optional) – The node's public key.
* Endpoints ([]object) – List of `exonet.Endpoint` objects. Each entry carries its own `Object Type`, so every endpoint type is representable, `mod.kcp.endpoint` and `nat.endpoint` included.

The text form is the base62 encoding of the binary encoding; JSON encodes the object as that same text.

## Example

`Alias` `void0`, `Identity` `02bef8840eb35ef2ae3c83c07cb5779278904f99cb4103f71e37cc69931ae5e15f`, and two endpoints: `mod.tcp.endpoint` `1.2.3.4:1791` and `mod.kcp.endpoint` `1.2.3.4:1791`.

```json
{
  "Type": "mod.nodes.node_info",
  "Object": "f3ACGQgAIgO3S7N4IztycBuxWzFyeWbQ8vBEMgABQAdul2bwRmbl5CcjRnLk9WbQIAAAAwXhXuGTmGz34x9DE0yZeJIxTy7qlPgHkHXl3rZdgQ89VgAghs0emdFA"
}
```
