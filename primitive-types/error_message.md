# error_message

An error message.

# Binary Encoding

Binary encoding of the payload is the same as [`string16`](string16.md) – 
16-bit-lenght-prefixed UTF8 string.

## JSON Encoding

A plain JSON string.

## Text Encoding

A plain string.

## Example

`"bad input"`, in each encoding:

```
binary   00 09 62 61 64 20 69 6e 70 75 74
json     "bad input"
text     bad input
```
