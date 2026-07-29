# string8

Basic string type, equivalent to string16, string32, and string64 in JSON.

## Binary Encoding

A uint8 length prefix followed by the string.

## JSON Encoding

A plain JSON string.

## Text Encoding

A plain string.

## Example

`"hi"`, in each encoding:

```
binary   02 68 69
json     "hi"
text     hi
```
