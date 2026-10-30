# coldcard

The `coldcard` protocol is what the `astral-coldcard` [`App`](../../core-definitions/app.md)
serves. The app signs for the keys of attached Coldcard hardware wallets. It claims
each device's key, derived at `m/1791'/0'/0'/0/0`, on a
[`crypto.register_signer`](../crypto/ops/crypto.register_signer.md) binding, so
signing under that key reaches the device through the
[`crypto`](../crypto/README.md) protocol.

The app advertises the [service](../services/README.md) `coldcard`. A caller reaches
the app by the identity [`services.discover`](../services/ops/services.discover.md)
returns. The node serves no `coldcard` operation.

The local [`User`](../../core-definitions/user.md) and the local
[`Node`](../../core-definitions/node.md) may use the app, and nobody else. An
offering to any other caller has `Available: false`.

| Operation | Purpose |
|-----------|---------|
| [`coldcard.scan`](ops/coldcard.scan.md) | Rescan the attached devices now. |

The app scans on an interval, so a caller does not need `coldcard.scan` to have a
device noticed.

A device signs `bip137` text only: ASCII, at most 240 bytes. A person approves each
signature on the device.
