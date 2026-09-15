# dir.apply_filters

Apply a set of named filters to an identity and return whether any filter matches. The identity defaults to the caller; pass `identity` to test a different identity. Returns `true` if any of the named filters returns true for the identity, `false` otherwise.

The caller must hold
[`mod.auth.see_node_state_action`](../../auth/types/mod.auth.see_node_state_action.md).
The query is rejected before any filter is applied when the caller is not
authorized, and a refused caller receives no bytes.

## Arguments

* filters (string8, required) – Comma-separated list of filter names to apply.
* identity (string8) – Identity to test, resolved via `dir.resolve`. Defaults to the caller's identity.

## Returned objects

The operation returns one of:
* An `error_message` object if `identity` cannot be resolved.
* A `bool` object indicating whether any filter matched.

## Examples

```shellsession
$ astral-query dir.apply_filters -filters local,friends -identity 0282fee8775757cdd8fda8b220195f5b8611312cd145c5a1a3aa55df210e779b2c -out json
{"Type":"bool","Object":true}
```
