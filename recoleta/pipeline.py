from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed

import httpx
from rich.progress import Progress

from recoleta.extract import (
    extract_html_maintext,
    extract_pdf_text,
    fetch_url_bytes,
    fetch_url_html,
)
from recoleta.pipeline.service import PipelineService

__all__ = [
    "PipelineService",
    "Progress",
    "ThreadPoolExecutor",
    "as_completed",
    "extract_html_maintext",
    "extract_pdf_text",
    "fetch_url_bytes",
    "fetch_url_html",
    "httpx",
]
