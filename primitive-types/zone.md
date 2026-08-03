# zone

A routing scope: the set of [`Zones`](../core-definitions/zone.md) — `Device`,
`Virtual`, `Network` — in which a query may be routed and resolved. Any
combination of the three is valid, including the empty set.

See [Zone](../core-definitions/zone.md) for what each `Zone` covers and how it
constrains routing.

## Binary Encoding

A single byte: a [`uint8`](uint8.md) bit field. `Device` is `0x01`, `Virtual`
is `0x02`, `Network` is `0x04`. The default is all three set, `0x07`.

## JSON Encoding

A JSON **string** holding the letters of the set bits in `d`, `v`, `n` order —
for example `"dvn"`, `"dn"`, `"d"`, or `""` for the empty set.

The form is a string. The bit field is never emitted as a JSON number, and a
number is not accepted in its place.

## Text Encoding

The same letter string as the [JSON Encoding](../topics/json-encoding.md), without quotes.

## Example

`Device | Network`, in each encoding:

```
binary   05
json     "dn"
text     dn
```
