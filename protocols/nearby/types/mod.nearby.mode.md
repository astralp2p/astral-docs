# mod.nearby.mode

Controls how the node broadcasts its presence on the local network.

## Fields

`mod.nearby.mode` is a `uint8` alias. The value is one of:

* `0` – Silent: the node sends no nearby datagram. It sends no status, no scan
  reply and no scan of its own. The node still receives the statuses other
  nodes broadcast.
* `1` – Visible: the node broadcasts its status, answers scans and scans; the
  attachments depend on the contract state.
* `2` – Stealth: the node broadcasts its status and answers scans with a
  `mod.nearby.stealth_hint` that hides the user–node association. It also
  scans. A status with no attachments is not sent.

The stored mode is the tree value `/mod/nearby/mode`. `mode` in `nearby.yaml`
writes it at each start; the default is `2` (Stealth).

While no user identity is set, the node acts in mode `1` (Visible) unless the
stored mode is `0` (Silent). A stored `0` (Silent) applies before and after the
claim.

## Disclosure

* A node in mode `1` (Visible) attaches its endpoints: TCP and KCP endpoints,
  its Tor onion endpoint when tor listens, and its gateway endpoints. It also
  attaches its alias when one is set.
* An unclaimed node in mode `1` (Visible) also attaches a `mod.nearby.flag`
  reading `adoptable` and a `mod.nearby.public_profile` with its node identity
  and alias.
* A claimed node in mode `1` (Visible) also attaches its active contract,
  which names the user.
* A claimed node in mode `2` (Stealth) attaches only a
  `mod.nearby.stealth_hint`. Stealth hides the user, not the node.
* Every nearby datagram names the node identity as its source and carries the
  node's signature.
* A scan reply goes to the scan's source address, whatever its subnet. A scan
  with a spoofed source address reflects a signed status to the ether port
  (`8822` by default) of that address. Mode `0` (Silent), `listen: false` in
  `ether.yaml`, or a firewall closes this.

## Example

```json
{
  "Type": "mod.nearby.mode",
  "Object": 1
}
```
