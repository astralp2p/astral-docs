# string32

Basic string type, equivalent to string8, string16, and string64 in JSON.

## Binary Encoding

A uint32 length prefix followed by the string.

## JSON Encoding

A plain JSON string.

## Text Encoding

A plain string.

## Example

`"hi"`, in each encoding:

```
binary   00 00 00 02 68 69
json     "hi"
text     hi
```
