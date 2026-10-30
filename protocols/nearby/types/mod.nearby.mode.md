# mod.nearby.mode

Controls how the node broadcasts its presence on the local network.

## Fields

`mod.nearby.mode` is a `uint8` alias. The value is one of:

* `0` – Silent: the node sends no nearby datagram: no status, no scan reply,
  and no scan of its own. The node still receives the statuses other nodes
  broadcast.
* `1` – Visible: the node broadcasts its status and answers scans; content
  depends on the contract state.
* `2` – Stealth: the node broadcasts with a masked identity to hide the
  user–node association. A status with no attachments is not sent.

The default mode when a user identity is set is `2` (Stealth).

While no user identity is set, the node acts in mode `1` (Visible) unless the
stored mode is `0` (Silent). A stored `0` (Silent) applies before and after the
claim.

## Disclosure

* An unclaimed node in mode `1` (Visible) attaches a `mod.nearby.flag` reading
  `adoptable`, a `mod.nearby.public_profile` with its node identity and alias,
  and its endpoints.
* A claimed node in mode `1` (Visible) attaches its active contract, which
  names the user.
* Every nearby datagram in every mode names the node identity as its source
  and carries the node's signature. Stealth hides the user, not the node.
* A scan reply goes to the scan's source address, whatever its subnet. A scan
  with a spoofed source address reflects a signed status to the ether port
  (`8822` by default) of that address. `listen: false` in `ether.yaml` or a
  firewall closes this.

## Example

```json
{
  "Type": "mod.nearby.mode",
  "Object": 1
}
```
