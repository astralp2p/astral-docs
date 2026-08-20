# objects.get_blueprint

Return the [blueprint](../../../topics/blueprints.md) — the runtime wire-structure
schema — for a single type name. The blueprint describes only the named type;
referenced types are not resolved or included, so the caller fetches each
referenced type itself. The operation returns an `error_message` if the named
type is primitive (primitives have no blueprint) or is unknown.

The caller must hold
[`mod.auth.see_objects_action`](../../auth/types/mod.auth.see_objects_action.md).
The query is rejected before any repository is opened when the caller is not
authorized, and a refused caller receives no bytes.

## Arguments

* type (string8, required) – The type name to return the blueprint for.
* out (string8) – Output format.

## Returned objects

The operation returns one of:
* An `error_message` object if the named type is primitive (has no blueprint) or is unknown.
* The [`astral.blueprint`](../../../topics/blueprints.md) object for the named type. Its `Object` carries `Type` (the type name), `Fields` (the ordered field specs; empty for an alias), and `Underlying` (the aliased primitive name; empty for a struct).

## Examples

```shellsession
$ astral-query objects.get_blueprint -type mod.gateway.endpoint -out json
{"Type":"astral.blueprint","Object":{"Fields":[{"Name":"GatewayID","Spec":{"Type":"astral.blueprint.primitive_spec","Object":{"PrimitiveType":"identity"}}},{"Name":"TargetID","Spec":{"Type":"astral.blueprint.primitive_spec","Object":{"PrimitiveType":"identity"}}}],"Type":"mod.gateway.endpoint","Underlying":""}}
```
