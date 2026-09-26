# auth.sign_contract

Co-sign a `mod.auth.contract` with the issuer's and subject's private keys
held by the node. The contract is read from the input stream and a
`mod.auth.signed_contract` carrying both signatures is returned.

A query whose origin is `network`, `mcp` or any origin other than local is
rejected before a contract is read. A command of a
[`shell.shell`](../../shell/ops/shell.shell.md) session carries no origin and is
checked as local, with the session's identity as the caller.

Each party of each contract passes the signer rule of
[`crypto.sign_hash`](../../crypto/ops/crypto.sign_hash.md): the party is the
caller and is not the node, or the caller is another identity that holds
[`mod.auth.sudo_action`](../types/mod.auth.sudo_action.md) for the party. The
issuer is checked first, then the subject. A refused issuer answers
`authorize issuer: ` followed by the reason. A refused subject answers
`authorize subject: ` followed by the reason. The reason is `cannot sign with
another identity's key`, or `cannot sign with the node's key` for a caller that
arrives as the node and names the node. A refused contract reaches no key.

One contract passes without the signer rule: the claim contract of node setup.
The node signs it while all of these hold:

* The caller is the node. A local caller that presents no identity is
  rewritten to the node's identity.
* The subject is the node. The issuer is not the node.
* The permits are exactly the permits
  [`user.new_node_contract`](../../user/ops/user.new_node_contract.md) writes:
  the same actions in the same order, the same delegation, and no constraints.
* The contract expires more than 1 hour from now and at most 365 days and
  1 hour from now. 365 days is the default validity of
  `user.new_node_contract`.
* The node is unclaimed: the node holds no active contract.
* The node has indexed no contract from the issuer to the node carrying
  [`mod.nodes.relay_for_action`](../../nodes/types/mod.nodes.relay_for_action.md)
  or
  [`mod.user.swarm_membership_action`](../../user/types/mod.user.swarm_membership_action.md),
  expired contracts included. A failed lookup refuses the contract.

[`apphost.register`](../../apphost/ops/apphost.register.md) and
[`messaging.create_identity`](../../messaging/ops/messaging.create_identity.md),
which [`mcp.create_agent`](../../mcp/ops/mcp.create_agent.md) mints its agents
through, index a relay contract for each identity they mint, after the
identity's private key is indexed. An
identity whose registration fails between those two steps holds no relay
contract. The node indexes the node contract of each user it accepts, so the
claim contract is never signed again for a user the node has had, even after
the node's active contract is cleared or has expired.

An authorized contract is signed as the issuer, then as the subject. The node
must hold the private keys of both parties. A missing issuer key fails with
`sign as issuer: unsupported`. A missing subject key fails with
`sign as subject: unsupported`.

## Arguments

* in (string) – Optional input stream format (e.g. `json`).
* out (string) – Optional output stream format (e.g. `json`).
* (stream) – `mod.auth.contract` objects to sign, one `mod.auth.signed_contract` or `error_message` returned per input; an object of another type is answered with an `error_message`. An explicit `eos` input is answered with a final `eos`; a stream ended by EOF is not.

## Returned objects

The query is rejected when its origin is not local. Otherwise the operation
returns, per input, one of:
* An `error_message` reading `invalid contract` if the contract has no issuer
  or no subject.
* An `error_message` reading `authorize issuer: ` or `authorize subject: `
  followed by the reason, if the caller may not sign as that party.
* An `error_message` object if the contract cannot be decoded, signing fails,
  or either signature is already present on the contract.
* A `mod.auth.signed_contract` object containing the original contract and
  both signatures.
* An `eos` object answering an explicit `eos` input.

## Examples

```shellsession
$ echo '{"Type":"mod.auth.contract","Object":{"Issuer":"...","Subject":"...","Permits":[{"Action":"mod.user.see_swarm_action"}],"ExpiresAt":"2027-05-27T12:00:00+02:00"}}' \
    | astral-query auth.sign_contract -in json -out json
{"Type":"mod.auth.signed_contract","Object":{...}}
```
