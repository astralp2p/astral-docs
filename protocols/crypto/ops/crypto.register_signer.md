# crypto.register_signer

The operation binds the calling app as the signer of a fixed set of keys on its
hosting node. The channel remains open for the binding's lifetime; closing it
releases all keys.

The node sends signing requests on the channel, and the app answers on the same
channel. An app that signs through a binding exposes no signing operation of its
own, so no query reaches its signer.

## Admission

The caller is the signer. Each refusal below is answered with an
`error_message`, and the node closes the channel.

1. A query of any origin other than local is answered `origin not allowed`.
2. The node identity, or a query with no caller, is answered `not permitted`.
3. The caller sends one [`mod.crypto.signer_keys`](../types/mod.crypto.signer_keys.md)
   as its first object, within 10 seconds. The node closes a channel that sends
   nothing in that time.
4. The set holds 1–64 distinct pairs of key and scheme. Every key is a 33-byte
   compressed `secp256k1` key, and every pair is one of the
   [supported pairs](#supported-pairs). The node's own key is answered `cannot
   sign with the node's key`.
5. The caller holds
   [`mod.auth.register_signer_action`](../../auth/types/mod.auth.register_signer_action.md)
   for every distinct key, or is answered `not permitted`.
6. Admission claims every pair or none. A pair held by a live binding refuses
   the entire set with `key already claimed by a signer` and leaves the existing
   binding untouched.

[`apphost.register`](../../apphost/ops/apphost.register.md) requests the action
when `grant_permits` names it, subject to registration policy.

### Supported pairs

| Key type | Scheme | Request |
|----------|--------|---------|
| `secp256k1` | `bip137` | [`mod.crypto.sign_text_request`](../types/mod.crypto.sign_text_request.md) |
| `secp256k1` | `asn1` | [`mod.crypto.sign_hash_request`](../types/mod.crypto.sign_hash_request.md) |

## Arguments

* in (string8) – Input format.
* out (string8) – Output format.

The key set travels on the channel. The operation takes no argument naming a
key, and no value of any argument stands for every key.

## The binding

The `ack` confirms readiness. The open channel then carries:

| Direction | Object | Rule |
|-----------|--------|------|
| node → app | [`mod.crypto.sign_text_request`](../types/mod.crypto.sign_text_request.md) | One signature over a text. |
| node → app | [`mod.crypto.sign_hash_request`](../types/mod.crypto.sign_hash_request.md) | One signature over a hash. |
| node → app | [`mod.crypto.sign_cancel`](../types/mod.crypto.sign_cancel.md) | The node no longer waits for the request. |
| app → node | [`mod.crypto.sign_answer`](../types/mod.crypto.sign_answer.md) | Echoes `RequestID` and carries a signature or an error. |

Several requests may be outstanding on one binding. The app answers them in any
order. The node waits at most `signer_timeout` for an answer (`crypto.yaml`,
default 5 minutes), because a signer may wait for a person to approve.

The binding ends when the channel closes. The node releases the binding's pairs,
and every outstanding request fails with `signer is gone`. A node restart ends
all bindings, and nothing about a binding is stored.

## Signing through a binding

* A key with a local private key signs locally. A binding that claims such a key
  receives no request for it.
* [`AuthorizeSigner`](../README.md) decides who may sign. A caller it refuses
  causes no request.
* The node verifies every signature against the claimed key and the request's
  payload before any caller receives it. A signature that does not verify, or
  carries another scheme, fails the request and ends the binding.
* The node does not retry a request and does not fall back to another scheme
  once a binding has been asked.
* A signing request carries a non-empty payload that fits its frame. The node
  refuses any other before asking the binding, so a payload never ends a binding.

An app holding the action sees the text or hash sent for signing under the keys
it claims, and may refuse them. No app produces a signature the node accepts for
a key it does not hold. A claim proves nothing about possession of the key.

An undecodable frame, an unexpected object, or an answer that does not carry
exactly one of a signature and an error ends the binding. An answer with no
outstanding `RequestID`, including a late answer, is ignored.

## Returned objects

* `error_message`, then close: a refused admission.
* `ack`, then the binding exchange: successful admission. This is a
  [readiness ack](../../../topics/op-modes.md#control-signals).

## Examples

```shellsession
$ echo '{"Type":"mod.crypto.signer_keys","Object":{"Keys":[{"Key":{"Type":"secp256k1","Key":"Anm+Zn753LusVaBilc6HCwcCm/zbLc4o2VnygVsW+BeY"},"Scheme":"bip137"}]}}' | astral-query crypto.register_signer -in json -out json
{"Type":"ack","Object":null}
```
