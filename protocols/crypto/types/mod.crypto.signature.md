# mod.crypto.signature

A generic container for a signature, tagged with the scheme that produced it.

## Fields

* Scheme (string8) – Name of the signature scheme (e.g. `asn1`, `bip137`).
* Data (bytes16) – Raw signature bytes for the given scheme.

The text form is `<scheme>:<base64-encoded data>`; JSON encodes the object as its named
fields, not as that text. `Data` carries the same base64 in both forms.

## Example

```json
{
  "Type": "mod.crypto.signature",
  "Object": {
    "Data": "MEYCIQDJ1xPxQO1Mnv2l5z3reHcBj8FtVfp+jKL6aXSbhAzTmAIhAMFZnUnPVqraUY0iigrOK5oyCd84y8wNHzdVOo3BC5s7",
    "Scheme": "asn1"
  }
}
```
