# inference.model

One model a provider offers, with the capabilities a caller needs in order to
decide whether to use it at all.

`ContextWindow` and `MaxOutput` are what let a caller size a request without
discovering the limits by being refused. `Modalities` says which kinds of
[`inference.content_part`](inference.content_part.md) the model accepts, so a
caller can tell before sending a picture whether pictures are welcome.

## Fields

* ID (string8) – The identifier a request names in `Model`.
* DisplayName (string8) – A human-readable name, or empty.
* ContextWindow (uint32) – Total tokens one request may span, prompt and output together; 0 when unstated.
* MaxOutput (uint32) – The largest output one request may ask for.
* Modalities ([]string8) – Input kinds accepted: "text", "image", "audio", "video". Empty means text alone.
* EffortLevels ([]inference.effort_level) – The effort settings this model honours; empty means effort is not settable.
* Streams (bool) – Whether the model can answer as a stream of deltas.
* Description (string8) – Free text about the model, or empty.

## Example

```json
{
  "Type": "inference.model",
  "Object": {
    "ID": "gpt-4o",
    "DisplayName": "GPT-4o",
    "ContextWindow": 128000,
    "MaxOutput": 16384,
    "Modalities": ["text", "image"],
    "EffortLevels": [
      {"Name": "low", "Description": "fastest, cheapest", "TokenBudget": 1024}
    ],
    "Streams": true,
    "Description": "general-purpose multimodal"
  }
}
```
