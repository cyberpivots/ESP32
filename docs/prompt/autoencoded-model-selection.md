# Autoencoded Model Selection

## Source basis

This guidance references `SRC-OPENAI-LATEST-MODEL`.

## Profiles

- `short`: low-risk summarization, simple formatting, quick repo lookups.
- `standard`: normal coding, documentation edits, local verification.
- `deep`: cross-cutting architecture, hardware risk analysis, source-backed
  research, multi-step implementation.
- `validation`: independent review, CI diagnosis, evidence checking.

## Default routing

- Use `standard` for ordinary development.
- Use `deep` for hardware, radio, power, firmware framework, and architecture
  decisions.
- Use `validation` before accepting framework changes, live flashing workflows,
  or relay-load procedures.

## Current model guidance

Current OpenAI documentation identifies `gpt-5.5` as the latest model and
recommends reasoning effort tuning by workload. This repository stores routing
policy only; it does not call the OpenAI API by default.

