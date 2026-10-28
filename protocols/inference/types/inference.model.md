# inference.model

One model a provider offers, with the capabilities a caller needs in order to
decide whether to use it at all.

`ContextWindow` and `MaxOutput` are what let a caller size a request without
discovering the limits by being refused. `Modalities` says which kinds of
[`inference.content_part`](inference.content_part.md) the model accepts, so a
caller can tell before sending a picture whether pictures are welcome.

`Tools` says whether the model takes [`inference.tool`](inference.tool.md)
definitions and can answer with calls. A caller that runs a tool loop needs
that before it picks a model, not after its first answer comes back as prose.

`DefaultEffort` names the level the model runs at when a request names none.
Without it, "default" is a word a caller can show but not explain, and two
providers of the same model may well differ in it. A level named `off` in
`EffortLevels` means the model can be told not to think at all.

## Fields

* ID (string8) – The identifier a request names in `Model`.
* DisplayName (string8) – A human-readable name, or empty.
* ContextWindow (uint32) – Total tokens one request may span, prompt and output together; 0 when unstated.
* MaxOutput (uint32) – The largest output one request may ask for.
* Modalities ([]string8) – Input kinds accepted: "text", "image", "audio", "video". Empty means text alone.
* EffortLevels ([]inference.effort_level) – The effort settings this model honours; empty means effort is not settable. "off", when listed, turns thinking off.
* Streams (bool) – Whether the model can answer as a stream of deltas.
* Description (string8) – Free text about the model, or empty.
* DefaultEffort (string8) – The effort level the model uses when a request names none; empty when the provider does not know.
* Tools (bool) – Whether the model takes tool definitions and can answer with tool calls.

## Example

```json
{
  "Type": "inference.model",
  "Object": {
    "ID": "atlas-32b",
    "DisplayName": "Atlas 32B",
    "ContextWindow": 131072,
    "MaxOutput": 8192,
    "Modalities": ["text", "image"],
    "EffortLevels": [
      {"Name": "off", "Description": "answer without thinking", "TokenBudget": 0},
      {"Name": "low", "Description": "think briefly", "TokenBudget": 1024},
      {"Name": "high", "Description": "think thoroughly", "TokenBudget": 8192}
    ],
    "Streams": true,
    "Description": "general-purpose multimodal",
    "DefaultEffort": "low",
    "Tools": true
  }
}
```
