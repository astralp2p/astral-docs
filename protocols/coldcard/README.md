# coldcard

The `coldcard` protocol integrates Coldcard hardware wallet devices with the node. It detects connected devices via USB, maps each device's serial number to its derived public key, and exposes the resulting crypto engine for signing.

The `coldcard.scan` operation re-scans the USB bus and refreshes the module's device state.

## Actions

One action gates the protocol. `coldcard.scan` submits it before it scans.

* [`mod.coldcard.scan_action`](types/mod.coldcard.scan_action.md) – scan the node's attached Coldcard devices
