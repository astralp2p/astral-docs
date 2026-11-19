# nat.reflect_udp_offer

The first answer of [`nat.reflect_udp`](../ops/nat.reflect_udp.md): where the caller sends the datagram to be reflected, and what it carries.

## Fields

* Port (uint16) – The UDP port the reflecting node listens on for this query, on the IPv4 address the caller dialed it at.
* Token (bytes8) – The 16-byte random token the datagram's payload must equal.

## Example

```json
{
  "Type": "nat.reflect_udp_offer",
  "Object": {
    "Port": 47001,
    "Token": "q83vEjRWeJCrze8SNFZ4kA=="
  }
}
```
