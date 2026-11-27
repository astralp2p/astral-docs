# mod.user.swarm_offer_added

Emitted by user once for each valid offer that appears in the node's SwarmState. It travels as the `Data` of a [`mod.events.event`](../../events/types/mod.events.event.md) to the node's own receivers and never leaves the node.

An offer is a half-signed [`mod.auth.contract`](../../auth/types/mod.auth.contract.md) that answers a contract request ([App grants](../README.md#app-grants)). It is valid when the merge check stored it: its request is stored and not declined, and its issuer is not expelled. No event follows an offer whose request is declined or expired, or whose issuer is expelled. The subject of the offer, the app's host, reacts by co-signing the offers for its own requests.

Every event of the swarm is a signal to read the entries again: a receiver reads the current state before it acts, and copes with a duplicate. The node emits it for every valid entry it holds, and a receiver keeps those whose `Subject` it serves. The node emits nothing at startup for entries it already holds.

## Fields

* OfferID (object_id) – Entry ID of the stored half-signed contract.
* RequestID (object_id) – Entry ID of the contract request the offer answers.
* Issuer (identity) – The approver that signed the offer.
* Subject (identity) – The node the offer names, the filer of the request.

## Example

```json
{
  "Type": "mod.user.swarm_offer_added",
  "Object": {
    "OfferID": "data1q9m3fd0d3x5kz7vu4tn2yjh8lcw6ar5p0se4gbxn8o2ty7k1hvnqe",
    "RequestID": "data1eotsgeey6k7os9bhn5c6aow7rqf7jqmayqyq87bwpfatmo7e8mdcp",
    "Issuer": "0282fee8775757cdd8fda8b220195f5b8611312cd145c5a1a3aa55df210e779b2c",
    "Subject": "03a7c1f5b9d4e62a8f730ce15d2b4a9c11e8d77c3b5f04a6d92e1b8f72c4d3e5a6"
  }
}
```
