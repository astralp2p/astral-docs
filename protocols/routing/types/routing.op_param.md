# routing.op_param

One parameter a routable operation accepts. A
[`routing.op_spec`](routing.op_spec.md) carries a list of these.

## Fields

* Name (string32) – The parameter name as used in a query string.
* Type (string32) – The name of the type the parameter takes.
* Required (bool) – True when the operation rejects a query that omits the parameter.

## Example

```json
{
  "Type": "routing.op_param",
  "Object": {
    "Name": "name",
    "Type": "string8",
    "Required": false
  }
}
```
