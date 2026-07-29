# ip.local_addrs

Stream the IP addresses assigned to local network interfaces, excluding loopback addresses.

## Arguments

None.

## Returned objects

The operation returns one of:
* A `mod.ip.ip_address` object for each local interface address.
* An `error_message` object if sending an address fails.
* An `eos` object terminating the stream.

## Examples

```shellsession
$ astral-query ip.local_addrs -out json
{"Type":"mod.ip.ip_address","Object":"192.168.1.42"}
{"Type":"mod.ip.ip_address","Object":"10.0.0.5"}
{"Type":"eos","Object":{}}
```
