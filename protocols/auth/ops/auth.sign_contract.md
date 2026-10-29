# auth.sign_contract

Co-sign a `mod.auth.contract` with the issuer's and subject's private keys
held by the node. The contract is read from the input stream and a
`mod.auth.signed_contract` carrying both signatures is returned.

A query whose origin is `network`, `mcp` or any origin other than local is
answered `origin not allowed: <origin>` before a contract is read. A command of a
[`shell.shell`](../../shell/ops/shell.shell.md) session carries no origin and is
checked as local, with the session's identity as the caller.

Each party of each contract passes the signer rule of
[`crypto.sign_hash`](../../crypto/ops/crypto.sign_hash.md): the party is the
caller and is not the node, or the caller is another identity that holds
[`mod.auth.sudo_action`](../types/mod.auth.sudo_action.md) for the party. The
issuer is checked first, then the subject. A refused issuer answers
`authorize issuer: ` followed by the reason. A refused subject answers
`authorize subject: ` followed by the reason. The reason is
`cannot sign with another identity's key`, or `cannot sign with the node's key`
for a caller that arrives as the node and names the node. A refused contract
reaches no key.

One contract passes without the signer rule: the claim contract of
[node setup](../../../topics/node-setup.md).
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

The rule reads nothing of the issuer's history. A user the node has had
re-claims it once its contract is cleared or has expired. An identity the node
minted through [`apphost.register`](../../apphost/ops/apphost.register.md),
[`messaging.create_mailbox`](../../messaging/ops/messaging.create_mailbox.md) or
[`mcp.create_agent`](../../mcp/ops/mcp.create_agent.md) passes as issuer.

[`user.bootstrap`](../../user/ops/user.bootstrap.md) applies the same rule to
the claim contract it signs.

An authorized contract is signed as the issuer, then as the subject. The node
must hold the private keys of both parties. A missing issuer key fails with:

```
sign as issuer: no signing scheme available for key secp256k1:<hex>: the node holds no usable private key for it; a key is held as an indexed mod.crypto.private_key object or on a connected signing device
```

`secp256k1:<hex>` is the issuer's public key. A missing subject key fails with
the same text after a `sign as subject: ` prefix in place of
`sign as issuer: `, naming the subject's public key.

## Arguments

* in (string) – Optional input stream format (e.g. `json`).
* out (string) – Optional output stream format (e.g. `json`).
* (stream) – `mod.auth.contract` objects to sign, one `mod.auth.signed_contract` or `error_message` returned per input; an object of another type is answered with an `error_message`. An explicit `eos` input is answered with a final `eos`; a stream ended by EOF is not.

## Returned objects

A query whose origin is not local is answered `origin not allowed: <origin>`.
Otherwise the operation returns, per input, one of:
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
    | astral-query -eos auth.sign_contract -in json -out json
{"Type":"mod.auth.signed_contract","Object":{...}}
{"Type":"eos","Object":null}
```
