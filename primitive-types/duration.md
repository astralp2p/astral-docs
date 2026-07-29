# duration

A length of time.

## Binary Encoding

A signed 64-bit integer count of nanoseconds (8 bytes).

## JSON Encoding

An integer number of nanoseconds.

## Text Encoding

A duration string, such as `1m30s`.

## Example

90 seconds, in each encoding:

```
binary   00 00 00 14 f4 6b 04 00
json     90000000000
text     1m30s
```
