## Integrating this logger into a real system

This logger is meant to be embedded into an AI agent pipeline so that downstream tools (like the Prompt Injection Origin Detector) can analyze where malicious instructions entered the system.

### 1) Remove demo artifacts

Before using this in a real system:

- delete `demo_trace.jsonl`  
- delete or ignore `sample_trace.jsonl`  
- keep `trace_logger.py` only  

These files are for demonstration and testing only.

### 2) Decide where to store trace logs

Pick a path for your runtime traces, for example:

- `./traces/agent_trace.jsonl`  
- `/var/log/agent/trace.jsonl`  

Make sure the directory exists and is writable by your application.

Example:

```bash
mkdir traces
```

### 3) Instrument your pipeline at trust boundaries

Emit a trace event at every point where untrusted text enters or moves between components.

At minimum, log:

- raw user input (before any modification)
- each retrieval (RAG) chunk before merging into context
- each tool output before injecting into prompts
- agent-to-agent messages before consumption
- the final assembled model input

Example (conceptual):

```python
import trace_logger

trace_logger.emit(
    out_path="traces/agent_trace.jsonl",
    trace_id=request_id,
    step=1,
    source="user",
    component="ingest",
    text=user_input,
)
```

Repeat this pattern at each step, incrementing `step`.

### 4) Keep previews human-readable and safe

The `preview` field is intentionally human-readable to support debugging and incident response.

Recommended practices:

- keep previews short (default is 160 chars)
- avoid logging full documents or full secrets
- log before any transformations so origin can be determined

If needed, redact obvious secrets before passing text to the logger.

### 5) Generate one trace per request

Use a unique `trace_id` for each request or workflow execution.

All steps belonging to the same request should share the same `trace_id`.

This allows the Origin Detector to reconstruct the timeline.

### 6) Analyze traces with the Origin Detector

Once traces are being written, analyze them using the Prompt Injection Origin Detector repo:

```bash
python origin_detector.py --trace traces/agent_trace.jsonl
```

To export a machine-readable report:

```bash
python origin_detector.py --trace traces/agent_trace.jsonl --out report.json
```

### 7) Production considerations

- rotate or archive trace files periodically  
- restrict access to trace logs (they may contain sensitive previews)  
- consider masking tokens, API keys, or secrets before logging  
- store traces in append-only files for forensic integrity  

### 8) What this does not do

This logger does not:

- prevent prompt injection  
- sanitize content  
- enforce policy  

It only emits structured trace logs so forensic and governance tools can operate correctly.

Prevention and enforcement should be handled by your control plane or agent governance layer.
