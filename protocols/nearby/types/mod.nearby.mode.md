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
  `mod.nearby.stealth_hint` that only a node knowing the node identity or the
  user identity reads. It also scans. A node without an active contract sends
  no status in Stealth.

The node refuses a value above `2`. Setting one fails, and a `mode` above `2`
in `nearby.yaml` fails the load of the module.

The stored mode is the tree value `/mod/nearby/mode`. `mode` in `nearby.yaml`
writes it at each start when the file states the key. Otherwise a mode set
through the tree persists across restarts. An unset stored mode reads as `2`
(Stealth) on a claimed node.

While no user identity is set, the node acts in mode `1` (Visible) unless the
stored mode is `0` (Silent). A stored `0` (Silent) applies before and after the
claim. A stored `1` (Visible) survives the claim, so a node set to Visible
before the claim stays Visible after it.

`silent_listen` in `nearby.yaml`, the tree value `/mod/nearby/silent_listen`,
decides whether a node in mode `0` (Silent) acts on the statuses it hears. It
defaults to `true`: the node contacts peers of its own user by the rules of the
other modes ([nearby](../README.md)). When it is `false`, the node caches and
lists the peers it hears and emits no `mod.nearby.peer_seen`.

## Disclosure

* A node in mode `0` (Silent) sends nothing on nearby: no periodic status, no
  status on an address change, no scan reply and no scan.
* A node without an owner in mode `1` (Visible) sends a `mod.nearby.flag`
  reading `adoptable`, a `mod.nearby.public_profile` with its node identity
  and alias and no user identity, and a `mod.nearby.status_proof`.
* A claimed node in mode `1` (Visible) sends a `mod.nearby.public_profile`
  with its node identity, its user identity and its alias, and a
  `mod.nearby.status_proof`. Every node on the local network reads them.
* A claimed node in mode `2` (Stealth) sends a `mod.nearby.stealth_hint` and a
  `mod.nearby.status_proof` whose signature is wrapped. A node that knows the
  user identity recovers the node identity from the hint. A node that knows the
  node identity recovers the user identity from the hint. Either node unwraps
  and verifies the proof. Any other node learns neither identity, and recovers
  no public key from the wrapped signature.
* No status carries an endpoint, a contract or a `mod.dir.alias`.
* A scan reply is the node's normal status, broadcast on the subnet that
  contains the scan's source IP. It discloses nothing beyond the periodic
  status.
* A node linked to this node reads its active contract with
  [`user.contract`](../../user/ops/user.contract.md). The contract names the
  user. Its permits show whether the node is a management node
  ([user](../../user/README.md)). Its expiry, by default 365 days after the
  contract was made, shows when the user claimed or adopted the node.
* An observer on the local network sees UDP traffic on the ether port (`8822`
  by default) and TCP traffic on port `1791`, which shows that the device runs
  astral. No mode hides the device's IP or MAC address.

## Example

```json
{
  "Type": "mod.nearby.mode",
  "Object": 1
}
```
