# dir.alias_map

Return the complete alias-to-identity mapping as a single `mod.dir.alias_map` object.

The caller must hold
[`mod.auth.see_node_state_action`](../../auth/types/mod.auth.see_node_state_action.md).
The query is rejected before the alias map is read when the caller is not
authorized, and a refused caller receives no bytes.

## Returned objects

The operation returns one of:
* A `mod.dir.alias_map` object containing all registered aliases.

## Examples

```shellsession
$ astral-query dir.alias_map -out json
{"Type":"mod.dir.alias_map","Object":{"Aliases":{"alice":"0282fee8775757cdd8fda8b220195f5b8611312cd145c5a1a3aa55df210e779b2c","bob":"03a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2"}}}
```
