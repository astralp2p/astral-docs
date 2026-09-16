# objects.repositories

List repositories registered with the module (network zone excluded).

The caller must hold
[`mod.auth.see_objects_action`](../../auth/types/mod.auth.see_objects_action.md).
The query is rejected before any repository is opened when the caller is not
authorized, and a refused caller receives no bytes.

## Arguments

* out (string8) – Output format.

## Returned objects

The operation returns a stream of `mod.objects.repository_info` objects (one per registered repository) followed by an `eos` object.

* The stream is flat. A group's `Children` names other repositories in the same stream and embeds no record.
* Stream order is unspecified and does not encode hierarchy. `Children` order is the group's lookup order.
* Membership is not a tree. A repository can be a member of more than one group, and a group can reach itself through its members.

## Examples

```shellsession
$ astral-query objects.repositories -out json
{"Type":"mod.objects.repository_info","Object":{"Name":"main","Label":"World","Free":6412488633,"Kind":"group","Children":["device","virtual","network"],"Concurrent":false}}
{"Type":"mod.objects.repository_info","Object":{"Name":"device","Label":"This device","Free":6412488633,"Kind":"group","Children":["memory","local","removable"],"Concurrent":false}}
{"Type":"mod.objects.repository_info","Object":{"Name":"memory","Label":"In-memory repos","Free":134217657,"Kind":"group","Children":["mem0","system"],"Concurrent":false}}
{"Type":"mod.objects.repository_info","Object":{"Name":"mem0","Label":"Default memory","Free":67108864,"Kind":"repository","Children":[],"Concurrent":false}}
{"Type":"mod.objects.repository_info","Object":{"Name":"system","Label":"System memory","Free":67108793,"Kind":"repository","Children":[],"Concurrent":false}}
{"Type":"mod.objects.repository_info","Object":{"Name":"local","Label":"Local storage","Free":6278270976,"Kind":"group","Children":["data"],"Concurrent":true}}
{"Type":"mod.objects.repository_info","Object":{"Name":"data","Label":"Default","Free":6278270976,"Kind":"repository","Children":[],"Concurrent":false}}
{"Type":"mod.objects.repository_info","Object":{"Name":"removable","Label":"Removable devices","Free":0,"Kind":"group","Children":[],"Concurrent":true}}
{"Type":"mod.objects.repository_info","Object":{"Name":"virtual","Label":"Virtual repositories","Free":0,"Kind":"group","Children":[],"Concurrent":true}}
{"Type":"mod.objects.repository_info","Object":{"Name":"network","Label":"Network repositories","Free":0,"Kind":"group","Children":[],"Concurrent":true}}
{"Type":"eos","Object":null}
```
