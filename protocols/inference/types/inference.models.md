# inference.models

An inventory: every model a provider offers one caller.

This object is both the answer of [`inference.models`](../ops/inference.models.md)
and the object a provider puts in its `services` offering's `Info` bundle, so a
caller that found the provider by discovery already has the inventory without
asking for it.

The list is per caller and already filtered: a model absent here is one the
caller may not use, not one the provider lacks.

## Fields

* Models ([]inference.model) – The models this caller may use.

## Example

```json
{
  "Type": "inference.models",
  "Object": {
    "Models": [
      {"ID": "gpt-4o-mini", "ContextWindow": 128000, "MaxOutput": 16384, "Modalities": ["text", "image"], "Streams": true},
      {"ID": "gpt-4o", "ContextWindow": 128000, "MaxOutput": 16384, "Modalities": ["text", "image"], "Streams": true}
    ]
  }
}
```
