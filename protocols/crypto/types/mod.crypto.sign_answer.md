# mod.crypto.sign_answer

An app's answer to a [`mod.crypto.sign_text_request`](mod.crypto.sign_text_request.md)
or a [`mod.crypto.sign_hash_request`](mod.crypto.sign_hash_request.md). `RequestID`
must echo the request. An answer with no outstanding request, including a late
answer, is ignored.

An answer carries exactly one of `Signature` and `Error`. Any other answer ends
the binding.

The node returns `Error` to the signing caller. A person declining on a device is
an `Error`. The node verifies `Signature` before any caller receives it.

## Fields

* RequestID (nonce64) – The `RequestID` of the request being answered.
* Signature ([`mod.crypto.signature`](mod.crypto.signature.md)) – The signature, or absent when the app did not sign.
* Error (string16) – Why the app did not sign, or empty.

## Example

```json
{
  "Type": "mod.crypto.sign_answer",
  "Object": {
    "RequestID": "9f2c41aa07d3e815",
    "Signature": null,
    "Error": "declined on the device"
  }
}
```
