# JSON Encoding

* The `JSON Encoding` is an optional encoding that is used by the `Astral
  Network`.
* The `JSON Encoding` can only be used with `Typed Objects`.
* The `JSON Encoding` uses a container with "Type" and "[Object](../core-definitions/object.md)" keys. The
  "Type" key contains the [`Object Type`](../core-definitions/object-type.md) and the "Object" key contains the
  `Payload` encoded as a JSON object.
* The exact way the `Payload` is encoded is described in the documentation
  of the specific `Object Type`.
* A value in an interface-typed slot — one whose concrete `Object Type` is not
  fixed by the enclosing type, e.g. a `Blueprint` `Field`'s `Spec`
  ([Blueprints](blueprints.md#json)) — is encoded as a nested "Type"/"Object"
  container, the same shape as a top-level object. The nested "Type" names the
  concrete `Object Type`; a JSON `null` in the slot is the absent value.
* Absent optional values are encoded as JSON `null`.
* Field-name lookup during decoding is case-insensitive. This applies to the
  container's own "Type" and "Object" keys and to `Payload` key names alike.
* A container key other than "Type" and "Object" is an error, and a decoder
  rejects the container. Ignoring the key instead leaves the `Payload` unread
  and yields a zero-valued object from a document that named a type correctly —
  a corrupted value that reports no error.
* Two keys of one container, or of one `Payload`, whose names differ only in
  case are an error. A decoder rejects the container rather than choosing
  between them.
* A container with no "Object" key carries no `Payload` and is equivalent to an
  "Object" key holding JSON `null`. The absent form of an interface-typed slot
  remains a JSON `null` in the slot, not an omitted key.


## Example

```
   {"Type":"uint32","Object":42}
```


