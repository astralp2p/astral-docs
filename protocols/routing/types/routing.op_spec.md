# routing.op_spec

Describes a single routable operation: its name and the parameters it accepts.

## Fields

* Name (string) – The operation name as used in query strings.
* Parameters (list) – One entry per accepted parameter, each with `Name` (string), `Type` (string), and `Required` (bool). The entry has no registered [`Object Type`](../../../core-definitions/object-type.md) of its own and cannot be requested by name.

## Example

```json
{
  "Type": "routing.op_spec",
  "Object": {
    "Name": "discover",
    "Parameters": [
      {"Name": "name", "Type": "string8", "Required": false}
    ]
  }
}
```
