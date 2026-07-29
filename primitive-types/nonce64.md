# nonce64

A 64-bit nonce.

## Binary Encoding

8 raw bytes of the nonce value.

## JSON Encoding

A hex string, **not** zero-padded. A value with leading zero nibbles is shorter
than 16 digits, so a parser must not require a fixed width.

## Text Encoding

A hex string, zero-padded to 16 digits.

The two forms differ: the same nonce is padded in the text encoding and
unpadded in JSON.

## Example

`0x0102030405060708`, in each encoding:

```
binary   01 02 03 04 05 06 07 08
json     "102030405060708"
text     0102030405060708
```

`0x42` — the padding difference is visible here, and is the case a fixed-width
parser gets wrong:

```
binary   00 00 00 00 00 00 00 42
json     "42"
text     0000000000000042
```
