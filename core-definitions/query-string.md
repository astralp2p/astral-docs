# Query String

* A `Query String` contains the `Operation Name` and the `Operation Parameters`.
* A `Query String` encodes `Parameter` values by using only the type-specific
  payload of [`Text Encoding`](../topics/text-encoding.md). The [`Object Type`](object-type.md) is defined by the `Parameter`.
* A `Query String` is encoded using the standard HTTP query string format
  ("operation?param1=value1&param2=value2").
* A `Query String` has no length limit of its own. The limit is whichever
  carrier transports it:
  * over a [`Link`](link.md), a [`uint16`](../primitive-types/uint16.md) length — 65 535 bytes (see
    [Link Multiplexer](../topics/link-mux.md));
  * over the apphost protocols, a [`string16`](../primitive-types/string16.md)
    — also 65 535 bytes;
  * over HTTP, whatever the transport permits in a request path, since no
    astral-level prefix applies.
* An implementation must not assume a single figure across carriers, and must
  not enforce a cap the carrier does not impose.
