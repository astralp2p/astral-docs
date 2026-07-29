# identity

Represented by a 66-digit hex string of a secp256k1 public key.

## Anonymous identity

The all-zero 33-byte key is the anonymous identity ("anyone"). Two anonymous identities compare equal.

## Binary Encoding

The binary encoding of an identity is 33 bytes of the raw secp256k1 public key.

The binary encoding of the anonymous identity is 33 zero bytes.

## JSON Encoding

The JSON encoding of an identity is the hex string of the secp256k1 public key.

The JSON encoding of the anonymous identity is the string `"anyone"`, which is also accepted on parse.

## Text Encoding

The text encoding of an identity is the hex string of the secp256k1 public key.

The text encoding of the anonymous identity is the 66-zero hex string. Parsing accepts either the literal string `anyone` or 66 `0` hex characters.
## Example

A secp256k1 public key, in each encoding:

```
binary   03 10 ac 91 60 c6 37 78 0c 41 5d ec 1e 68 0e 18
         c3 fa 42 d9 fb f6 76 54 78 b0 34 fc 5b 58 ca 74
         1f
json     "0310ac9160c637780c415dec1e680e18c3fa42d9fbf6765478b034fc5b58ca741f"
text     0310ac9160c637780c415dec1e680e18c3fa42d9fbf6765478b034fc5b58ca741f
```

The binary form is the 33 raw key bytes; the JSON and text forms are the same
bytes as 66 hex digits.
