# time

An object representing time.

## Binary Encoding

A uint64 representing the time in nanoseconds since Unix epoch (UTC).

## JSON Encoding

Time is encoded as an RFC 3339 string.

## Text Encoding

Time is encoded as an RFC 3339 string.

RFC 3339 is a profile of ISO 8601, not a synonym for it: ISO 8601 admits forms
this encoding does not accept. Emit and parse RFC 3339 only.

## Example

`2026-07-29T06:00:00Z`, in each encoding:

```
binary   18 c6 ad 41 b3 cc c0 00
json     "2026-07-29T06:00:00Z"
text     2026-07-29T06:00:00Z
```
