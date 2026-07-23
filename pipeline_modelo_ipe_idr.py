#!/usr/bin/env python3
import base64
import gzip
import traceback
from pathlib import Path

try:
    payload = "".join(
        Path(f"pipeline_payload_{i:02d}.txt").read_text(encoding="utf-8").strip()
        for i in range(1, 5)
    )
    source = gzip.decompress(base64.b64decode(payload)).decode("utf-8")
    source = source.replace(
        "expense_chunks(zip_paths[(2024, table)])",
        "expense_chunks(zip_paths[(2024, table)], table)",
    )
    exec(compile(source, "pipeline_modelo_ipe_idr.py", "exec"))
except BaseException:
    diagnostic = Path("output") / "diagnostic_traceback.txt"
    diagnostic.parent.mkdir(parents=True, exist_ok=True)
    diagnostic.write_text(traceback.format_exc(), encoding="utf-8")
    raise
