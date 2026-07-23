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

    source = source.replace(
        "import numpy as np\nimport pandas as pd\nimport requests\n",
        """import numpy as np
import pandas as pd
import requests

_JSON_ENCODER_DEFAULT = json.JSONEncoder.default
def _json_encoder_default(self, obj):
    if isinstance(obj, np.generic):
        return obj.item()
    if obj is pd.NA:
        return None
    if isinstance(obj, Path):
        return str(obj)
    return _JSON_ENCODER_DEFAULT(self, obj)
json.JSONEncoder.default = _json_encoder_default
""",
        1,
    )

    source = source.replace(
        """            destination = RAW_DIR / str(year) / filename
            network = download_file(url, destination)
""",
        """            destination = RAW_DIR / str(year) / filename
            cache_destination = Path('.cache/enigh') / str(year) / filename
            if cache_destination.exists():
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(cache_destination, destination)
                network = {
                    'http_final_url': url,
                    'http_content_type': 'application/zip; restored-from-actions-cache',
                    'bytes_descargados': destination.stat().st_size,
                    'http_content_length': destination.stat().st_size,
                }
                log(f'RESTAURADO DESDE CACHE: {year} {table}')
            else:
                network = download_file(url, destination)
                cache_destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(destination, cache_destination)
""",
        1,
    )

    exec(compile(source, "pipeline_modelo_ipe_idr.py", "exec"))
except BaseException:
    diagnostic = Path("output") / "diagnostic_traceback.txt"
    diagnostic.parent.mkdir(parents=True, exist_ok=True)
    diagnostic.write_text(traceback.format_exc(), encoding="utf-8")
    raise
