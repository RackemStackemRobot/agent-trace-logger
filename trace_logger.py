import json
import hashlib
from datetime import datetime, timezone


def _utc_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _content_hash(text: str) -> str:
    h = hashlib.sha256(text.encode("utf-8", errors="ignore")).hexdigest()
    return h[:12]


def _safe_preview(text: str, max_len: int) -> str:
    text = (text or "").replace("\r", " ").replace("\n", " ").strip()
    if len(text) <= max_len:
        return text
    return text[: max_len - 3] + "..."


def emit(
    *,
    out_path: str,
    trace_id: str,
    step: int,
    source: str,
    component: str,
    text: str,
    preview_len: int = 160,
) -> dict:
    """
    Emit one JSONL trace event compatible with Prompt Injection Origin Detector.

    Writes a single line to out_path.
    Returns the event dict (useful for testing).
    """
    preview = _safe_preview(text, preview_len)

    event = {
        "trace_id": str(trace_id),
        "step": int(step),
        "source": str(source),
        "component": str(component),
        "timestamp": _utc_iso(),
        "preview": preview,
        "hash": _content_hash(text or ""),
    }

    with open(out_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")

    return event
