# mod.user.swarm_contract_added

Emitted by user once when a stored contract first counts. It travels as the `Data` of a [`mod.events.event`](../../events/types/mod.events.event.md) to the node's own receivers and never leaves the node.

A contract counts when both its signatures are valid, it has not expired, and neither its issuer nor its subject is expelled. A half-signed offer never emits this event. The event carries the entry ID of the completed contract, which differs from the `OfferID` of the offer it completes; both share the object ID of the unsigned contract body. The node's auth indexes the contract on it, the host sees its request fulfilled, and a UI reads the grant.

Every event of the swarm is a signal to read the entries again: a receiver reads the current state before it acts, and copes with a duplicate. The node emits it for every valid entry it holds, and a receiver keeps those whose `Subject` it serves. The node emits nothing at startup for entries it already holds.

## Fields

* ContractID (object_id) – Entry ID of the stored contract with both signatures.
* Issuer (identity) – The contract's issuer.
* Subject (identity) – The contract's subject.
* RequestID (object_id) – The contract's `RequestID`: the request it answers, or `null` when it answers none, as a membership the user key signed directly.

## Example

```json
{
  "Type": "mod.user.swarm_contract_added",
  "Object": {
    "ContractID": "data1w4h8sx2rj6d0cv9ntk3pa5ylf7ze1mg8ub4qo0i2xe6nrs9t3dyc",
    "Issuer": "0282fee8775757cdd8fda8b220195f5b8611312cd145c5a1a3aa55df210e779b2c",
    "Subject": "03a7c1f5b9d4e62a8f730ce15d2b4a9c11e8d77c3b5f04a6d92e1b8f72c4d3e5a6",
    "RequestID": "data1eotsgeey6k7os9bhn5c6aow7rqf7jqmayqyq87bwpfatmo7e8mdcp"
  }
}
```
