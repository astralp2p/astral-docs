# bytes32

Basic byte-array type, equivalent to bytes8, bytes16, and bytes64 in JSON. Differs from those only in the width of the length prefix.

## Binary Encoding

A uint32 length prefix followed by that many raw bytes.

## JSON Encoding

A base64 string.

## Text Encoding

A base64 string.

## Example

The two bytes `0a 0b`, in each encoding:

```
binary   00 00 00 02 0a 0b
json     "Cgs="
text     Cgs=
```
