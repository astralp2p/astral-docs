# player

The `player` protocol controls a music player: playback state (play, pause, seek) and the play queue (append, remove, move). Tracks are referred to by their [`Object ID`](../../core-definitions/object-id.md) in all operations; the player fetches the audio data through the [`objects`](../objects/README.md) protocol.

## Design notes

* **Observability** – `player.state` and `player.queue` accept a `follow` argument. With `follow`, the operation stays open and streams a new snapshot whenever the state or queue changes, so any number of front-ends can stay in sync while controlling the player concurrently.
* **Position extrapolation** – the player does not stream continuous position updates. A `player.state` object carries the playback position at the time given by `UpdatedAt`; while the status is "playing", observers compute the current position as `Position + (now - UpdatedAt)`. A new state is emitted on every transition (play, pause, seek, track change).
* **Track metadata** – the state snapshot includes the current track's title, artist, album and the object ID of its cover image. The player does the media-format heavy lifting: it reads the file's tags, extracts embedded artwork and stores it as an object on the local node, so front-ends only ever deal with typed objects and object IDs.
* **Queue versioning** – the queue has a `Version` that increases on every modification. Index-based operations (`player.remove`, `player.move`) accept an optional `version` argument and are rejected if the queue has changed since, protecting concurrent editors from acting on stale indexes.

## Discovery

A player advertises itself as the [`services`](../services/README.md) service
named `player`. Its offering is `Available` with an `Info` bundle holding one
[`services.operations_list`](../services/types/services.operations_list.md) of
the `player.*` operations below. A front-end finds every player in its swarm
with `services.discover -services player -reach swarm` and addresses the
operations to the offering's `ProviderID`.

A player answers under its own app identity, as a desktop player does, or under
its node's identity, as a player built into a mobile node does. A player gives
full control to every caller that reaches it.

## Operations

State:

* [player.state](ops/player.state.md) – get or follow the playback state
* [player.play](ops/player.play.md) – start or resume playback
* [player.pause](ops/player.pause.md) – pause playback
* [player.seek](ops/player.seek.md) – seek within the current track
* [player.next](ops/player.next.md) – skip to the next queue entry
* [player.prev](ops/player.prev.md) – skip to the previous queue entry

Queue:

* [player.queue](ops/player.queue.md) – get or follow the play queue
* [player.append](ops/player.append.md) – add a track to the queue
* [player.remove](ops/player.remove.md) – remove a queue entry
* [player.move](ops/player.move.md) – reorder a queue entry
* [player.clear](ops/player.clear.md) – empty the queue and stop playback

## Types

* [player.state](types/player.state.md) – a snapshot of the playback state
* [player.queue](types/player.queue.md) – a snapshot of the play queue
