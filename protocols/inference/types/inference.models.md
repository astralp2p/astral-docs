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
      {"ID": "atlas-8b", "ContextWindow": 32768, "MaxOutput": 4096, "Modalities": ["text"], "Streams": true, "Tools": true},
      {"ID": "atlas-32b", "ContextWindow": 131072, "MaxOutput": 8192, "Modalities": ["text", "image"], "Streams": true, "DefaultEffort": "low", "Tools": true}
    ]
  }
}
```
