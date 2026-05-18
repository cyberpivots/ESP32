# Handoff 0001 - Scaffold To Research

## From

Architect

## To

Hardware, Communications, QA

## Context

The workspace scaffold is framework-neutral and source-backed. Seed hardware
profiles exist for the requested starting devices, but physical validation and
exact module/relay board matching are not complete.

## Next actions

- Hardware: confirm exact board revisions, relay board electrical requirements,
  XBee adapter/interface hardware, and Heltec board variant.
- Communications: define first protocol candidates and acceptance tests.
- QA: extend `scripts/verify_scaffold.py` as repository behavior grows.

