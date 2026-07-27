from __future__ import annotations

from importlib import resources
import json
from pathlib import Path
import shutil
import tempfile
from typing import Any

from recoleta.app.runtime import typer


_DEMO_MARKER = ".recoleta-demo"
_LIVE_FLEET_URL = "https://neapolitanicecream.github.io/recoleta/"


def _validated_demo_output_dir(output_dir: Path, *, force: bool) -> Path:
    resolved = output_dir.expanduser().resolve()
    if resolved == Path.cwd().resolve():
        raise ValueError("Demo output must be a dedicated child directory")
    if not resolved.exists():
        return resolved
    if not resolved.is_dir():
        raise ValueError(f"Demo output exists and is not a directory: {resolved}")
    children = list(resolved.iterdir())
    if not children:
        return resolved
    if not force:
        raise ValueError(
            f"Demo output is not empty: {resolved}; pass --force to replace a prior demo"
        )
    if not (resolved / _DEMO_MARKER).is_file():
        raise ValueError(
            f"Refusing to replace an unmarked directory: {resolved}; "
            "choose a new output directory"
        )
    return resolved


def _write_demo_context(output_dir: Path) -> None:
    (output_dir / _DEMO_MARKER).write_text(
        "Recoleta bundled evaluation snapshot\n",
        encoding="utf-8",
    )
    (output_dir / "EVALUATION.md").write_text(
        "\n".join(
            [
                "# Recoleta evaluation snapshot",
                "",
                "This site was built from a curated public output produced by the",
                "running Recoleta fleet on 2026-07-23.",
                "",
                "- No source fetches were performed.",
                "- No model or embedding calls were performed.",
                "- The snapshot verifies package installation and site rendering only.",
                "- It does not count as a qualified external activation.",
                "",
                f"Inspect the current public fleet: {_LIVE_FLEET_URL}",
                "",
            ]
        ),
        encoding="utf-8",
    )


def _relocate_demo_manifest(
    *,
    manifest: dict[str, Any],
    output_dir: Path,
) -> dict[str, Any]:
    relocated_manifest = dict(manifest)
    artifacts_dir = output_dir / "artifacts"
    relocated_manifest["output_dir"] = str(output_dir)
    relocated_manifest["input_dir"] = str(artifacts_dir)
    relocated_manifest["input_dirs"] = [
        {
            **input_entry,
            "path": str(artifacts_dir),
        }
        for input_entry in manifest.get("input_dirs", [])
    ]
    return relocated_manifest


def build_demo_snapshot(*, output_dir: Path, force: bool = False) -> dict[str, Any]:
    resolved_output_dir = _validated_demo_output_dir(output_dir, force=force)
    resolved_output_dir.parent.mkdir(parents=True, exist_ok=True)

    from recoleta.site import export_trend_static_site

    demo_root = resources.files("recoleta.demo_data")
    with resources.as_file(demo_root.joinpath("Trends")) as input_dir:
        with tempfile.TemporaryDirectory(
            prefix=".recoleta-demo-",
            dir=resolved_output_dir.parent,
        ) as temporary_root:
            temporary_output = Path(temporary_root) / "site"
            manifest_path = export_trend_static_site(
                input_dir=input_dir,
                output_dir=temporary_output,
            )
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest = _relocate_demo_manifest(
                manifest=manifest,
                output_dir=resolved_output_dir,
            )
            manifest_path.write_text(
                json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True)
                + "\n",
                encoding="utf-8",
            )
            _write_demo_context(temporary_output)
            if resolved_output_dir.exists():
                shutil.rmtree(resolved_output_dir)
            temporary_output.replace(resolved_output_dir)

    return {
        "status": "ok",
        "output_dir": str(resolved_output_dir),
        "index_path": str(resolved_output_dir / "index.html"),
        "source": "bundled-production-fleet-snapshot",
        "snapshot_date": "2026-07-23",
        "network_calls": False,
        "model_calls": False,
        "qualified_activation": False,
        "live_fleet_url": _LIVE_FLEET_URL,
        "manifest": manifest,
    }


def run_demo_command(
    *,
    output_dir: Path,
    force: bool,
    json_output: bool,
) -> dict[str, Any]:
    try:
        payload = build_demo_snapshot(output_dir=output_dir, force=force)
    except ValueError as exc:
        typer.echo(str(exc))
        raise typer.Exit(code=2) from None

    if json_output:
        typer.echo(json.dumps(payload, ensure_ascii=False, sort_keys=True))
        return payload

    typer.echo("Built an offline Recoleta evaluation snapshot.")
    typer.echo(f"Open: {payload['index_path']}")
    typer.echo(
        "No network or model calls were made; this does not count as a "
        "qualified activation."
    )
    typer.echo(f"Current public fleet: {payload['live_fleet_url']}")
    return payload
