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

* Nested `Blueprint` frames are capped; `RefSpec`/`PtrSpec` cycles surface as typed errors.
* `ArraySpec.Length` and registered name lengths are bounded.
* `Aliases` over `Struct Blueprints` are not supported.
