# time

An object representing time.

## Binary Encoding

An int64 count of nanoseconds since the Unix epoch (UTC), carried in the eight
bytes of a uint64 as two's complement. An instant before the epoch has a
negative count and therefore occupies the upper half of the unsigned range. A
decoder reads the eight bytes and interprets them as int64; reading them as an
unsigned count places every pre-epoch instant in the 23rd century.

The representable range is `1677-09-21T00:12:43.145224192Z` through
`2262-04-11T23:47:16.854775807Z`. An instant outside it has no encoding.

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

`1969-01-01T00:00:00Z`, a pre-epoch instant, whose count is
`-31536000000000000`:

```
binary   ff 8f f6 2c d2 5d 00 00
json     "1969-01-01T00:00:00Z"
text     1969-01-01T00:00:00Z
```
