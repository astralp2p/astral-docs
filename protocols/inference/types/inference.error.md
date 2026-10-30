# inference.error

A refusal or a failure, in either operation of the protocol.

A bare error string leaves a consumer one move: give up. A consumer running a
conversation has several, and which one is right depends on what went wrong.
`Kind` tells them apart:

* `refused` – the provider will not serve this caller this request: the caller
  is not admitted, or the model is not one it may use. The two are not told
  apart, so a caller cannot probe for models it is not shown. Retrying changes
  nothing until the caller is admitted.
* `bad_request` – the request cannot be served as it is: it is malformed,
  names media the provider cannot resolve or will not take, or the server
  rejected it. Retrying the same request changes nothing.
* `context_overflow` – the conversation and the output asked for do not fit the
  model's context window. Shortening the conversation, or asking for less
  output, may help.
* `rate_limited` – the server, or the provider, is limiting requests. Retrying
  after `RetryAfter` may help.
* `unavailable` – the provider cannot reach its server, or the server cannot
  take requests now, e.g. while a model loads. Retrying later may help.
* `far_side` – the server behind the provider failed. A retry may succeed.

`Status` and `Message` carry the server's own account when there is one, word
for word. A consumer that recovers from a specific condition — a prompt over a
limit, too many images for the model — needs the server's own wording to
recognise it, and no list of kinds could anticipate every server's conditions.
`Message` is quoted data from the far side, not an instruction. A provider cuts
a message longer than a `string16` holds.

## Fields

* Kind (string8) – One of "refused", "bad_request", "context_overflow", "rate_limited", "unavailable" or "far_side".
* Status (uint32) – The server's HTTP status; 0 when there is none, as for the provider's own refusals.
* Message (string16) – What went wrong: the server's message word for word when there is one, else the provider's own.
* RetryAfter (uint32) – Seconds to wait before retrying; 0 when no figure was given.

## Example

```json
{
  "Type": "inference.error",
  "Object": {
    "Kind": "context_overflow",
    "Status": 400,
    "Message": "This model's maximum context length is 131072 tokens. However, you requested 140211 tokens.",
    "RetryAfter": 0
  }
}
```
