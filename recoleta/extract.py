from __future__ import annotations

import httpx
import trafilatura
from tenacity import retry, retry_if_exception, stop_after_attempt, wait_exponential_jitter


def _should_retry_httpx(exc: BaseException) -> bool:
    if isinstance(exc, httpx.RequestError):
        return True
    if isinstance(exc, httpx.HTTPStatusError):
        status = exc.response.status_code
        return status >= 500 or status == 429
    return False


@retry(
    retry=retry_if_exception(_should_retry_httpx),
    stop=stop_after_attempt(3),
    wait=wait_exponential_jitter(initial=0.5, max=6.0),
    reraise=True,
)
def fetch_url_html(client: httpx.Client, url: str) -> str:
    response = client.get(url)
    response.raise_for_status()
    return response.text


def extract_html_maintext(html: str) -> str | None:
    extracted = trafilatura.extract(
        html,
        include_comments=False,
        include_tables=False,
        include_formatting=False,
        deduplicate=True,
    )
    if not extracted:
        return None
    stripped = extracted.strip()
    return stripped or None

