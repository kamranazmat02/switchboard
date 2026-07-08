# ADR 0001: FastAPI over Flask for the webhook layer

## Status
Accepted, 2026-07-03.

## Context
Switchboard receives Twilio voice webhooks and, in v0.2, bidirectional
audio via Media Streams (WebSocket). Need a Python HTTP framework that
handles both cleanly.

## Decision
FastAPI.

## Consequences
Positive:
- Native async — required for Media Streams WebSocket handling planned in v0.2.
- Built-in Pydantic validation for Twilio webhook payloads.
- OpenAPI schema generated for free — useful for the tenant admin API planned in v1.0.

Negative:
- Slightly heavier learning curve than Flask.

Alternatives considered:
- Flask + flask-sock: simpler, but async story is uglier.
- Starlette: FastAPI's foundation; too low-level for the productivity gain FastAPI adds.