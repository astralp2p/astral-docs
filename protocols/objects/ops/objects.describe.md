# objects.describe

Collect descriptors for an object from all registered describers.

The caller must hold
[`mod.auth.see_objects_action`](../../auth/types/mod.auth.see_objects_action.md).
The query is rejected before any repository is opened when the caller is not
authorized, and a refused caller receives no bytes.

Other nodes are reached two ways, both only within the `network` zone:

* The swarm describer is a registered describer. It asks every other member of
  the swarm, concurrently. A member describes an object without holding its
  bytes.
* `sources` names nodes the caller chooses. `sources_only` decides whether they
  are asked on top of the registered describers or alone.

The node asks other nodes as itself. It authorized its caller; the other node
trusts that decision. A source equal to this node is skipped. A source that is
also a swarm member is asked twice when `sources_only` is `false`, and its
descriptors arrive twice.

A query arriving from the network runs without the `network` zone: the node
answers from its own describers and asks no other node.

## Arguments

* id (object_id.sha256, required) – The id to describe.
* zone (zone) – Limits the query's routing zone and never widens it. Without it, the routing zone stands.
* only (string8) – Comma-separated list of descriptor object types to include.
* except (string8) – Comma-separated list of descriptor object types to exclude.
* sources (string) – Comma-separated identities or aliases to ask. A repeated entry is asked once. Absent by default.
* sources_only (bool) – `true` asks only `sources` and runs no registered describer. Defaults to `false`, which asks `sources` on top of the registered describers.
* out (string8) – Output format.

The `id` can be a
[`Partial Object ID`](../../../core-definitions/object-id.md). The operation
reads no repository, so it resolves no `Partial Object ID` before the fan-out.
Every `Describer` receives the `id` as given.

A `Describer` decides for itself whether it matches by `Hash` alone. A
`Describer` that matches an `Object ID` exactly contributes nothing to a call
carrying a `Partial Object ID`. A `Describer` contributing nothing does not
fail the operation, which streams the descriptors the other describers
returned.

## Returned objects

The operation returns an `error_message` object if a `sources` entry does not resolve to an identity. Otherwise it returns a stream of `mod.objects.describe_result` objects (one per descriptor) followed by an `eos` object. The describe context has a one-minute timeout.

## Examples

```shellsession
$ astral-query objects.describe -id data1aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa -out json
{"Type":"mod.objects.describe_result","Object":{"SourceID":"02bef8840eb35ef2ae3c83c07cb5779278904f99cb4103f71e37cc69931ae5e15f","ObjectID":"data1aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa","Data":{"Type":"string8","Object":"hello"}}}
{"Type":"eos","Object":null}
```

```shellsession
$ astral-query objects.describe -id data1aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa -only mod.objects.repository_info -out json
{"Type":"eos","Object":null}
```
