from __future__ import annotations

from pathlib import Path
from xml.etree import ElementTree


def test_fleet_proof_svg_embeds_its_screenshots() -> None:
    asset_path = (
        Path(__file__).resolve().parents[1]
        / "docs"
        / "assets"
        / "recoleta-fleet-proof.svg"
    )
    root = ElementTree.parse(asset_path).getroot()
    image_elements = root.findall(".//{http://www.w3.org/2000/svg}image")
    image_hrefs = [element.get("href") for element in image_elements]

    assert len(image_hrefs) == 3
    assert all(
        href is not None and href.startswith("data:image/png;base64,")
        for href in image_hrefs
    )


def test_demo_docs_use_uv_managed_python_for_local_server() -> None:
    repository_root = Path(__file__).resolve().parents[1]
    documented_command = (
        "uv run --no-project --python 3.14 "
        "python -m http.server 8000 --directory recoleta-demo"
    )

    for relative_path in (
        "README.md",
        "docs/guides/production-fleet-case-study.md",
    ):
        document = (repository_root / relative_path).read_text(encoding="utf-8")
        assert documented_command in document
        assert "\npython -m http.server 8000 --directory recoleta-demo" not in document
