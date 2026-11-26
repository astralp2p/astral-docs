# user.swarm_requests

Stream the requests stored in SwarmState with their status, oldest filed first, terminated by `eos`. Without `all` it streams only the pending requests. The caller must hold `mod.user.see_swarm_action`; answered `not permitted` otherwise.

## Arguments

* all (bool) – When `true`, streams every stored request whatever its status. Defaults to `false`, which streams only the requests whose status is `pending`.

## Returned objects

The operation returns one of:
* An `error_message` reading `not permitted` if the caller is not authorized.
* An `error_message` if SwarmState cannot be read.
* For each request, three objects in this order:
  * an `object_id.sha256`, the request's entry ID, which [`user.answer_request`](user.answer_request.md) takes as `id`;
  * a [`mod.user.request_status`](../types/mod.user.request_status.md), the request's status;
  * the stored request: a [`mod.user.signed_contract_request`](../types/mod.user.signed_contract_request.md), a [`mod.user.signed_join_request`](../types/mod.user.signed_join_request.md) or a [`mod.user.signed_expel_request`](../types/mod.user.signed_expel_request.md).
* An `eos` object terminating the stream.

Requests are ordered by `FiledAt`; requests filed at the same time are ordered by entry ID.

## Examples

```shellsession
$ astral-query user.swarm_requests -out json
{"Type":"object_id.sha256","Object":"data1..."}
{"Type":"mod.user.request_status","Object":"pending"}
{"Type":"mod.user.signed_join_request","Object":{...}}
{"Type":"eos","Object":""}
```
