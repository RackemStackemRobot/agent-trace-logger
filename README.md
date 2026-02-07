# Agent Trace Logger

A tiny JSONL trace logger for agent pipelines.

This repo exists to generate step-level provenance logs that are compatible with the Prompt Injection Origin Detector tool.

## What it emits

Each call writes one JSON line containing:

- trace_id
- step
- source
- component
- timestamp (UTC)
- preview (trimmed human-readable snippet)
- hash (short SHA-256 prefix)

These fields are intentionally aligned with the expectations of the Prompt Injection Origin Detector.

## Install

No external dependencies.

## Usage

```python
import trace_logger

trace_logger.emit(
    out_path="trace.jsonl",
    trace_id="abc-123",
    step=1,
    source="user",
    component="ingest",
    text="User asked to summarize a document",
)
```

## Recommended logging points

To support injection origin detection, emit logs at:

- raw user input
- retrieval chunks before merge
- tool outputs before merge
- agent-to-agent messages before consumption
- final assembled model input

## Notes

- preview is trimmed and single-line for log readability
- hash lets you correlate content without storing full text
