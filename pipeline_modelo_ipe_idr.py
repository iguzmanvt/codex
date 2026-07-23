#!/usr/bin/env python3
import base64
import gzip
from pathlib import Path

payload = "".join(
    Path(f"pipeline_payload_{i:02d}.txt").read_text(encoding="utf-8").strip()
    for i in range(1, 5)
)
source = gzip.decompress(base64.b64decode(payload))
exec(compile(source, "pipeline_modelo_ipe_idr.py", "exec"))
