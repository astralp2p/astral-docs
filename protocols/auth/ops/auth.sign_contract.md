# auth.sign_contract

Co-sign a `mod.auth.contract` with the issuer's and subject's private keys
held by the node. The contract is read from the input stream and a
`mod.auth.signed_contract` carrying both signatures is returned. The node
must hold the private keys of both the issuer and the subject; otherwise the
operation fails with `no signing scheme available for key ...`.

## Arguments

* in (string) – Optional input stream format (e.g. `json`).
* out (string) – Optional output stream format (e.g. `json`).
* (stream) – `mod.auth.contract` objects to sign, one `mod.auth.signed_contract` or `error_message` returned per input; an object of another type is answered with an `error_message`. An explicit `eos` input is answered with a final `eos`; a stream ended by EOF is not.

## Returned objects

The operation returns one of:
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
