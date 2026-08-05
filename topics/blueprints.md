# Blueprints

* A `Blueprint` describes a `Typed Object`'s wire structure so the [`Codec`](codec.md) reads or writes it without compiled code.
* Every [`Object Type`](../core-definitions/object-type.md) known to a [`Node`](../core-definitions/node.md) is backed by a compile-time prototype or a `Blueprint`, both held in one registry keyed by `Object Type`.

## Kinds

* `Struct` — ordered named `Fields`; wire is each field's value in declared order.
* [`Alias`](../core-definitions/alias.md) — names an existing primitive; wire is identical to the underlying primitive.

## Specs

* Each `Field` has a `Name` and one `Spec`:
    * `PrimitiveSpec` — primitive from the allowlist.
    * `RefSpec` — another registered `Object Type`.
    * `SliceSpec` — [`uint32`](../primitive-types/uint32.md) count + elements.
    * `ArraySpec` — elements only; length is in the schema.
    * `MapSpec` — `uint32` count + sorted key/value pairs.
    * `PtrSpec` — [`bool`](../primitive-types/bool.md) presence + value if present.
    * `ObjectSpec` — [`string8`](../primitive-types/string8.md) type tag + payload.
* `Slice/Array/MapSpec` with empty element or value type → heterogeneous; each element carries its own type tag.
* `Slice/Array/MapSpec` with a named element or value type admits a nil element.
  A decoder built from such a `Spec` must accept `0x00` in the element slot and
  read it as nil. A decoder compiled against a non-optional element of the same
  type rejects `0x00` — see
  [Presence flag values](binary-encoding.md#presence-flag-values). Both are
  correct for their own element kind, so the two are not mutually readable even
  when both sides hold the same `Spec`.
* Primitive allowlist: `stringN` / `uintN` / `bytesN` (`N` ∈ {8, 16, 32, 64}), `bool`,
  [`time`](../primitive-types/time.md),
  [`identity`](../primitive-types/identity.md),
  [`object_id.sha256`](../primitive-types/object_id.sha256.md),
  [`nonce64`](../primitive-types/nonce64.md), `duration`,
  [`zone`](../primitive-types/zone.md).
* `MapSpec.KeyType` is [`string16`](../primitive-types/string16.md) or `uintN` (`N` ∈ {8, 16, 32, 64}).

## JSON

* A `Blueprint`'s [`JSON Encoding`](json-encoding.md) `Payload` always carries
  all three keys `Type`, `Fields`, and `Underlying`. `Struct` kind carries the
  `Fields` array and an empty-string `Underlying`;
  [`Alias`](../core-definitions/alias.md) kind carries the `Underlying`
  primitive name and an empty `Fields` array (`[]`). `Type` and `Underlying`
  are JSON strings; `Fields` is a JSON array.
* Each `Field` is an object with `Name` (a JSON string) and `Spec` keys. `Spec`
  is an interface-typed slot ([JSON Encoding](json-encoding.md)): a nested
  "Type"/"Object" container whose "Type" is the carrier's exact registered
  `Object Type` name — one of `astral.blueprint.primitive_spec`,
  `astral.blueprint.ref_spec`, `astral.blueprint.slice_spec`,
  `astral.blueprint.array_spec`, `astral.blueprint.map_spec`,
  `astral.blueprint.ptr_spec`, `astral.blueprint.object_spec`. The "Type" value
  is matched case-sensitively; key names are case-insensitive
  ([JSON Encoding](json-encoding.md)).
* Carrier payloads (name and type keys are JSON strings; `Length` is a JSON
  number): `PrimitiveSpec` `{"PrimitiveType"}` ·
  `RefSpec`/`PtrSpec`/`SliceSpec` `{"Type"}` (a `SliceSpec`'s empty `Type` →
  heterogeneous) · `ArraySpec` `{"Type","Length"}` · `MapSpec`
  `{"KeyType","ValueType"}` · `ObjectSpec` `{}`.
* Key order within any `Payload` is not significant — decoding is by key name.
  The reference encoder emits `Payload` keys in alphabetical order (e.g.
  `Fields`, `Type`, `Underlying`); the examples below use that order.

```
{"Type":"astral.blueprint","Object":{"Fields":[
  {"Name":"Author","Spec":{"Type":"astral.blueprint.primitive_spec","Object":{"PrimitiveType":"identity"}}},
  {"Name":"Body","Spec":{"Type":"astral.blueprint.primitive_spec","Object":{"PrimitiveType":"string16"}}}
],"Type":"example.message","Underlying":""}}
```

## Registry

* Maps `Object Type` → `Blueprint` or prototype. Names are unique and immutable.
* A registry can have a `Parent`; lookups walk the chain, local entries shadow.
* `Object Type` names are ASCII non-empty. `Field Names` are ASCII non-empty, unique within a `Blueprint` (case-insensitive).
* A `Blueprint` is itself an [`Object`](../core-definitions/object.md); registering returns the [`Object ID`](../core-definitions/object-id.md) of its canonical form.
* Nested types resolve through the same registry given to the enclosing `Decode`.

## Sync

* Exchanged in dependency order: aliases first, then structs topologically sorted so every `RefSpec`/`PtrSpec`/`SliceSpec`/`ArraySpec`/`MapSpec` edge targets an already-replayed name.
* Replay compares by `Object ID`: same name + matching ID is a no-op, same name + mismatched bytes is a conflict.

## Limits

* Nested `Blueprint` frames are capped — the figure and the floor every implementation must accept are in [Decoding limits](codec.md#decoding-limits); `RefSpec`/`PtrSpec` cycles surface as typed errors.
* `ArraySpec.Length` and registered name lengths are bounded.
* `Aliases` over `Struct Blueprints` are not supported.
