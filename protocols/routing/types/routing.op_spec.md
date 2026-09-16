# routing.op_spec

Describes a single routable operation: its name and the parameters it accepts.

## Fields

* Name (string32) – The operation name as used in query strings.
* Parameters (list of [`routing.op_param`](routing.op_param.md)) – One entry per accepted parameter.

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
