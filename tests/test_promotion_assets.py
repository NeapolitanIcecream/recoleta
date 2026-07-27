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
