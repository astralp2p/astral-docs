# mod.user.info

A snapshot of this node's user configuration: the node's state and manager,
and on a claimed node the aliases for the node and user and the active
contract under which the node operates.

## Fields

* NodeAlias (string8) – Display name of this node (resolved via `dir`). Empty
  unless `State` is `claimed`.
* UserAlias (string8) – Display name of the user (resolved via `dir`). Empty
  unless `State` is `claimed`.
* ContractID (object_id) – ID of the active contract object. Null unless
  `State` is `claimed`.
* Contract (mod.auth.signed_contract) – The active contract itself. Null
  unless `State` is `claimed`.
* State (string8) – The node's state: `fresh`, `unclaimed` or `claimed`
  ([apphost, Node states](../../apphost/README.md#node-states)).
* Manager (identity) – The node's
  [manager](../../apphost/README.md#manager). Null when none is appointed.

## Example

```json
{
  "Type": "mod.user.info",
  "Object": {
    "NodeAlias": "phone",
    "UserAlias": "alice",
    "ContractID": "id....",
    "Contract": { "...": "..." },
    "State": "claimed",
    "Manager": "0282fee8775757cdd8fda8b220195f5b8611312cd145c5a1a3aa55df210e779b2c"
  }
}
```
