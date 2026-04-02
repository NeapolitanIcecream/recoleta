from __future__ import annotations

import argparse
import ast
import csv
import fnmatch
import json
import os
import re
import subprocess
import tempfile
import tomllib
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Literal, cast

REPO_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_VERSION = 1
HOTSPOT_CLASSIFICATIONS = ("monitor", "refactor_soon", "refactor_now")
HOTSPOT_CLASSIFICATION_RANK = {
    "monitor": 1,
    "refactor_soon": 2,
    "refactor_now": 3,
}
SEVERITY_RANK = {
    "warning": 1,
    "high": 2,
    "critical": 3,
}
QUEUE_ORDER = (
    "pipeline",
    "site/render",
    "translation",
    "sources",
    "storage",
    "cli",
    "rag",
    "other",
)


@dataclass(frozen=True)
class MetricBands:
    warning_min: int
    warning_max: int
    high_min: int
    high_max: int
    critical_min: int

    def classify(self, value: int) -> Literal["warning", "high", "critical"] | None:
        if value >= self.critical_min:
            return "critical"
        if self.high_min <= value <= self.high_max:
            return "high"
        if self.warning_min <= value <= self.warning_max:
            return "warning"
        return None


@dataclass(frozen=True)
class LizardBands:
    ccn: MetricBands
    nloc: MetricBands
    parameter_count: MetricBands


@dataclass(frozen=True)
class VultureBands:
    review_candidate_min: int
    high_confidence_candidate_min: int

    def classify(
        self, confidence: int
    ) -> Literal["review_candidate", "high_confidence_candidate"] | None:
        if confidence >= self.high_confidence_candidate_min:
            return "high_confidence_candidate"
        if confidence >= self.review_candidate_min:
            return "review_candidate"
        return None


@dataclass(frozen=True)
class AuditConfig:
    repo_root: Path
    targets: tuple[str, ...]
    exclude: tuple[str, ...]
    out_dir: Path
    baseline: Path
    ruff: MetricBands
    lizard: LizardBands
    complexipy: MetricBands
    vulture: VultureBands


@dataclass(frozen=True)
class ScopeLookup:
    repo_root: Path
    allowed_rel_paths: frozenset[str]
    rel_paths_by_basename: dict[str, tuple[str, ...]]
    qualified_names_by_path: dict[str, frozenset[str]]
    qualified_names_by_path_and_leaf: dict[str, dict[str, tuple[str, ...]]]
    qualified_names_by_path_and_line: dict[str, dict[int, str]]

    @classmethod
    def from_files(cls, *, repo_root: Path, files: list[Path]) -> ScopeLookup:
        rel_paths = [relative_path(path, repo_root) for path in files]
        grouped: dict[str, list[str]] = defaultdict(list)
        qualified_names_by_path: dict[str, frozenset[str]] = {}
        qualified_names_by_path_and_leaf: dict[str, dict[str, tuple[str, ...]]] = {}
        qualified_names_by_path_and_line: dict[str, dict[int, str]] = {}
        for rel_path in rel_paths:
            grouped[Path(rel_path).name].append(rel_path)
            path = repo_root / rel_path
            symbol_index = build_symbol_index(path)
            qualified_names_by_path[rel_path] = frozenset(symbol_index["qualified_names"])
            qualified_names_by_path_and_leaf[rel_path] = symbol_index["by_leaf"]
            qualified_names_by_path_and_line[rel_path] = symbol_index["by_line"]
        rel_paths_by_basename = {
            name: tuple(sorted(values)) for name, values in grouped.items()
        }
        return cls(
            repo_root=repo_root,
            allowed_rel_paths=frozenset(rel_paths),
            rel_paths_by_basename=rel_paths_by_basename,
            qualified_names_by_path=qualified_names_by_path,
            qualified_names_by_path_and_leaf=qualified_names_by_path_and_leaf,
            qualified_names_by_path_and_line=qualified_names_by_path_and_line,
        )


@dataclass(frozen=True)
class HotspotSignal:
    tool: Literal["ruff", "lizard", "complexipy"]
    file: str
    symbol: str
    line: int | None
    severity: Literal["warning", "high", "critical"]
    metrics: dict[str, int]
    message: str

    @property
    def symbol_key(self) -> str:
        return f"{self.file}::{normalize_symbol_key(self.symbol)}"


def load_audit_config(*, repo_root: Path = REPO_ROOT) -> AuditConfig:
    pyproject_path = repo_root / "pyproject.toml"
    data = tomllib.loads(pyproject_path.read_text(encoding="utf-8"))
    config_data = data["tool"]["recoleta_refactor"]
    return AuditConfig(
        repo_root=repo_root,
        targets=tuple(config_data["targets"]),
        exclude=tuple(config_data["exclude"]),
        out_dir=resolve_repo_path(repo_root, str(config_data["out_dir"])),
        baseline=resolve_repo_path(repo_root, str(config_data["baseline"])),
        ruff=_metric_bands(config_data["ruff"]),
        lizard=LizardBands(
            ccn=MetricBands(
                warning_min=int(config_data["lizard"]["ccn_warning_min"]),
                warning_max=int(config_data["lizard"]["ccn_warning_max"]),
                high_min=int(config_data["lizard"]["ccn_high_min"]),
                high_max=int(config_data["lizard"]["ccn_high_max"]),
                critical_min=int(config_data["lizard"]["ccn_critical_min"]),
            ),
            nloc=MetricBands(
                warning_min=int(config_data["lizard"]["nloc_warning_min"]),
                warning_max=int(config_data["lizard"]["nloc_warning_max"]),
                high_min=int(config_data["lizard"]["nloc_high_min"]),
                high_max=int(config_data["lizard"]["nloc_high_max"]),
                critical_min=int(config_data["lizard"]["nloc_critical_min"]),
            ),
            parameter_count=MetricBands(
                warning_min=int(config_data["lizard"]["parameter_warning_min"]),
                warning_max=int(config_data["lizard"]["parameter_warning_max"]),
                high_min=int(config_data["lizard"]["parameter_high_min"]),
                high_max=int(config_data["lizard"]["parameter_high_max"]),
                critical_min=int(config_data["lizard"]["parameter_critical_min"]),
            ),
        ),
        complexipy=_metric_bands(config_data["complexipy"]),
        vulture=VultureBands(
            review_candidate_min=int(config_data["vulture"]["review_candidate_min"]),
            high_confidence_candidate_min=int(
                config_data["vulture"]["high_confidence_candidate_min"]
            ),
        ),
    )


def _metric_bands(values: dict[str, Any]) -> MetricBands:
    return MetricBands(
        warning_min=int(values["warning_min"]),
        warning_max=int(values["warning_max"]),
        high_min=int(values["high_min"]),
        high_max=int(values["high_max"]),
        critical_min=int(values["critical_min"]),
    )


def resolve_repo_path(repo_root: Path, value: str) -> Path:
    candidate = Path(value)
    if candidate.is_absolute():
        return candidate
    return (repo_root / candidate).resolve()


def relative_path(path: Path, repo_root: Path) -> str:
    try:
        return path.resolve().relative_to(repo_root.resolve()).as_posix()
    except ValueError:
        return Path(os.path.relpath(path.resolve(), repo_root.resolve())).as_posix()


def is_excluded(*, path: Path, repo_root: Path, patterns: tuple[str, ...]) -> bool:
    rel_path = relative_path(path, repo_root)
    rel_parts = Path(rel_path).parts
    for pattern in patterns:
        normalized = pattern.rstrip("/")
        if not normalized:
            continue
        if fnmatch.fnmatch(rel_path, normalized):
            return True
        if fnmatch.fnmatch(path.name, normalized):
            return True
        if normalized in rel_parts:
            return True
        if rel_path.startswith(f"{normalized}/"):
            return True
    return False


def collect_python_files(
    *, repo_root: Path, targets: list[str], exclude_patterns: tuple[str, ...]
) -> list[Path]:
    files: dict[str, Path] = {}
    for target in targets:
        candidate = Path(target)
        resolved = candidate if candidate.is_absolute() else (repo_root / candidate)
        resolved = resolved.resolve()
        if not resolved.exists():
            raise FileNotFoundError(f"Scope target does not exist: {target}")
        if is_excluded(path=resolved, repo_root=repo_root, patterns=exclude_patterns):
            continue
        if resolved.is_file():
            if resolved.suffix == ".py":
                files[relative_path(resolved, repo_root)] = resolved
            continue
        for path in resolved.rglob("*.py"):
            if is_excluded(path=path, repo_root=repo_root, patterns=exclude_patterns):
                continue
            files[relative_path(path, repo_root)] = path.resolve()
    return [files[key] for key in sorted(files)]


def resolve_reported_path(reported: str, lookup: ScopeLookup) -> str | None:
    reported_path = Path(str(reported))
    if reported_path.is_absolute():
        rel_path = relative_path(reported_path, lookup.repo_root)
        return rel_path if rel_path in lookup.allowed_rel_paths else None
    rel_candidate = reported_path.as_posix()
    if rel_candidate in lookup.allowed_rel_paths:
        return rel_candidate
    basename_matches = lookup.rel_paths_by_basename.get(reported_path.name, ())
    if len(basename_matches) == 1:
        return basename_matches[0]
    repo_candidate = relative_path(lookup.repo_root / reported_path, lookup.repo_root)
    if repo_candidate in lookup.allowed_rel_paths:
        return repo_candidate
    return None


def build_symbol_index(path: Path) -> dict[str, Any]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    qualified_names: list[str] = []
    by_leaf: dict[str, list[str]] = defaultdict(list)
    by_line: dict[int, str] = {}

    def walk(node: ast.AST, prefix: str = "", parent_kind: str | None = None) -> None:
        body = getattr(node, "body", None)
        if not isinstance(body, list):
            return
        for child in body:
            if isinstance(child, ast.ClassDef):
                qualified = child.name if not prefix else f"{prefix}::{child.name}"
                walk(child, qualified, "class")
                continue
            if isinstance(child, ast.AsyncFunctionDef | ast.FunctionDef):
                if not prefix:
                    qualified = child.name
                elif parent_kind == "class":
                    qualified = f"{prefix}::{child.name}"
                else:
                    qualified = f"{prefix}.{child.name}"
                qualified_names.append(qualified)
                by_line[int(child.lineno)] = qualified
                by_leaf[child.name].append(qualified)
                walk(child, qualified, "function")

    walk(tree)
    return {
        "qualified_names": tuple(sorted(qualified_names)),
        "by_leaf": {
            leaf: tuple(sorted(values))
            for leaf, values in sorted(by_leaf.items())
        },
        "by_line": dict(sorted(by_line.items())),
    }


def normalize_symbol_key(symbol: str) -> str:
    cleaned = str(symbol).strip().replace(" ", "")
    if not cleaned:
        return "unknown"
    return cleaned


def optional_int(value: object) -> int | None:
    if isinstance(value, bool):
        return int(value)
    if isinstance(value, int):
        return value
    if isinstance(value, str) and value.strip():
        try:
            return int(value)
        except ValueError:
            return None
    return None


def resolve_canonical_symbol(
    *, rel_path: str, symbol: str, line: int | None, lookup: ScopeLookup
) -> str:
    cleaned = str(symbol).strip()
    if not cleaned:
        return "unknown"
    by_line = lookup.qualified_names_by_path_and_line.get(rel_path, {})
    if line is not None and line in by_line:
        return by_line[line]
    qualified_names = lookup.qualified_names_by_path.get(rel_path, frozenset())
    if cleaned in qualified_names:
        return cleaned
    leaf = cleaned.split("::")[-1].split(".")[-1]
    matches = lookup.qualified_names_by_path_and_leaf.get(rel_path, {}).get(leaf, ())
    if len(matches) == 1:
        return matches[0]
    return cleaned


def run_command(
    command: list[str], *, cwd: Path, allowed_returncodes: set[int]
) -> subprocess.CompletedProcess[str]:
    try:
        completed = subprocess.run(
            command,
            cwd=cwd,
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError as exc:
        raise RuntimeError(f"Command not found: {command[0]}") from exc
    if completed.returncode not in allowed_returncodes:
        detail = completed.stderr.strip() or completed.stdout.strip()
        raise RuntimeError(
            f"Command failed with exit code {completed.returncode}: {' '.join(command)}"
            + (f"\n{detail}" if detail else "")
        )
    return completed


def parse_ruff_findings(
    *, raw_text: str, lookup: ScopeLookup, config: AuditConfig
) -> list[HotspotSignal]:
    findings: list[HotspotSignal] = []
    payload = json.loads(raw_text or "[]")
    for item in payload:
        if item.get("code") != "C901":
            continue
        message = str(item.get("message", ""))
        match = re.search(r"\((\d+)\s*>\s*\d+\)", message)
        if match is None:
            continue
        complexity = int(match.group(1))
        severity = config.ruff.classify(complexity)
        if severity is None:
            continue
        rel_path = resolve_reported_path(str(item.get("filename", "")), lookup)
        if rel_path is None:
            continue
        symbol_match = re.search(r"`([^`]+)`", message)
        symbol = symbol_match.group(1) if symbol_match else "<unknown>"
        location = item.get("location") or {}
        row = optional_int(location.get("row"))
        findings.append(
            HotspotSignal(
                tool="ruff",
                file=rel_path,
                symbol=resolve_canonical_symbol(
                    rel_path=rel_path,
                    symbol=symbol,
                    line=row,
                    lookup=lookup,
                ),
                line=row,
                severity=severity,
                metrics={"complexity": complexity},
                message=message,
            )
        )
    return findings


def parse_lizard_findings(
    *, raw_text: str, lookup: ScopeLookup, config: AuditConfig
) -> list[HotspotSignal]:
    findings: list[HotspotSignal] = []
    rows = csv.reader(raw_text.splitlines())
    for row in rows:
        if len(row) != 11:
            continue
        try:
            nloc = int(row[0])
            ccn = int(row[1])
            parameter_count = int(row[3])
            start_line = int(row[9])
        except ValueError:
            continue
        rel_path = resolve_reported_path(row[6], lookup)
        if rel_path is None:
            continue
        severities = {
            "ccn": config.lizard.ccn.classify(ccn),
            "nloc": config.lizard.nloc.classify(nloc),
            "parameter_count": config.lizard.parameter_count.classify(parameter_count),
        }
        ranked = [
            value for value in severities.values() if value is not None
        ]
        if not ranked:
            continue
        severity = cast(
            Literal["warning", "high", "critical"],
            max(ranked, key=lambda value: SEVERITY_RANK[value]),
        )
        findings.append(
            HotspotSignal(
                tool="lizard",
                file=rel_path,
                symbol=resolve_canonical_symbol(
                    rel_path=rel_path,
                    symbol=row[7],
                    line=start_line,
                    lookup=lookup,
                ),
                line=start_line,
                severity=severity,
                metrics={
                    "ccn": ccn,
                    "nloc": nloc,
                    "parameter_count": parameter_count,
                    "length": int(row[4]),
                    "token_count": int(row[2]),
                },
                message=(
                    f"CCN={ccn}, NLOC={nloc}, parameter_count={parameter_count}, "
                    f"length={row[4]}"
                ),
            )
        )
    return findings


def parse_complexipy_findings(
    *, raw_text: str, lookup: ScopeLookup, config: AuditConfig
) -> list[HotspotSignal]:
    findings: list[HotspotSignal] = []
    payload = json.loads(raw_text or "[]")
    for item in payload:
        complexity = int(item["complexity"])
        severity = config.complexipy.classify(complexity)
        if severity is None:
            continue
        rel_path = resolve_reported_path(str(item.get("path") or item.get("file_name")), lookup)
        if rel_path is None:
            continue
        symbol = str(item.get("function_name") or "<unknown>")
        findings.append(
            HotspotSignal(
                tool="complexipy",
                file=rel_path,
                symbol=resolve_canonical_symbol(
                    rel_path=rel_path,
                    symbol=symbol,
                    line=None,
                    lookup=lookup,
                ),
                line=None,
                severity=severity,
                metrics={"complexity": complexity},
                message=f"cognitive complexity={complexity}",
            )
        )
    return findings


def parse_vulture_candidates(
    *, raw_text: str, lookup: ScopeLookup, config: AuditConfig
) -> list[dict[str, Any]]:
    candidates: list[dict[str, Any]] = []
    pattern = re.compile(
        r"^(?P<path>.+?):(?P<line>\d+): unused (?P<kind>\w+) "
        r"'(?P<symbol>.+?)' \((?P<confidence>\d+)% confidence(?:, (?P<size>\d+) lines?)?\)$"
    )
    for raw_line in raw_text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        match = pattern.match(line)
        if match is None:
            continue
        confidence = int(match.group("confidence"))
        severity = config.vulture.classify(confidence)
        if severity is None:
            continue
        rel_path = resolve_reported_path(match.group("path"), lookup)
        if rel_path is None:
            continue
        symbol = match.group("symbol")
        kind = match.group("kind")
        candidates.append(
            {
                "id": f"{rel_path}::{kind}::{symbol}",
                "file": rel_path,
                "line": int(match.group("line")),
                "symbol": symbol,
                "kind": kind,
                "confidence": confidence,
                "classification": severity,
                "subsystem": infer_subsystem(rel_path),
                "size": int(match.group("size")) if match.group("size") else None,
            }
        )
    candidates.sort(key=dead_code_sort_key)
    return candidates


def dead_code_sort_key(item: dict[str, Any]) -> tuple[Any, ...]:
    return (
        0 if item["classification"] == "high_confidence_candidate" else 1,
        -int(item["confidence"]),
        item["file"],
        item["symbol"],
    )


def infer_subsystem(rel_path: str) -> str:
    if rel_path.startswith("recoleta/pipeline"):
        return "pipeline"
    if rel_path.startswith("recoleta/cli"):
        return "cli"
    if rel_path.startswith("recoleta/storage"):
        return "storage"
    if rel_path.startswith("recoleta/rag"):
        return "rag"
    if rel_path.startswith("recoleta/translation"):
        return "translation"
    if rel_path.startswith("recoleta/sources") or rel_path.startswith("recoleta/extract"):
        return "sources"
    if (
        rel_path.startswith("recoleta/site")
        or rel_path.startswith("recoleta/publish")
        or rel_path.startswith("recoleta/presentation")
        or rel_path.startswith("recoleta/trend_materialize")
    ):
        return "site/render"
    return "other"


def aggregate_hotspots(signals: list[HotspotSignal]) -> list[dict[str, Any]]:
    grouped: dict[str, list[HotspotSignal]] = defaultdict(list)
    for signal in signals:
        grouped[signal.symbol_key].append(signal)

    hotspots: list[dict[str, Any]] = []
    for hotspot_id, values in grouped.items():
        distinct_warning_plus = {
            signal.tool for signal in values if SEVERITY_RANK[signal.severity] >= 1
        }
        distinct_high_plus = {
            signal.tool for signal in values if SEVERITY_RANK[signal.severity] >= 2
        }
        has_critical_complexity = any(
            signal.tool in {"lizard", "complexipy"} and signal.severity == "critical"
            for signal in values
        )
        if has_critical_complexity or len(distinct_high_plus) >= 2:
            classification = "refactor_now"
        elif any(signal.severity in {"high", "critical"} for signal in values) or len(
            distinct_warning_plus
        ) >= 2:
            classification = "refactor_soon"
        else:
            classification = "monitor"

        metrics_by_tool: dict[str, dict[str, int]] = {}
        for signal in values:
            existing = metrics_by_tool.setdefault(signal.tool, {})
            for key, value in signal.metrics.items():
                existing[key] = max(existing.get(key, value), value)

        display_symbol = max((signal.symbol for signal in values), key=len)
        line_candidates = [signal.line for signal in values if signal.line is not None]
        hotspots.append(
            {
                "id": hotspot_id,
                "file": values[0].file,
                "symbol": display_symbol,
                "line": min(line_candidates) if line_candidates else None,
                "classification": classification,
                "subsystem": infer_subsystem(values[0].file),
                "tool_count": len({signal.tool for signal in values}),
                "tools": sorted({signal.tool for signal in values}),
                "metrics": metrics_by_tool,
                "signals": [
                    {
                        "tool": signal.tool,
                        "severity": signal.severity,
                        "symbol": signal.symbol,
                        "line": signal.line,
                        "metrics": signal.metrics,
                        "message": signal.message,
                    }
                    for signal in sorted(
                        values,
                        key=lambda item: (
                            -SEVERITY_RANK[item.severity],
                            item.tool,
                            item.symbol,
                        ),
                    )
                ],
            }
        )
    hotspots.sort(key=hotspot_sort_key)
    return hotspots


def hotspot_sort_key(item: dict[str, Any]) -> tuple[Any, ...]:
    metrics = item.get("metrics", {})
    return (
        -HOTSPOT_CLASSIFICATION_RANK[item["classification"]],
        -int(metrics.get("complexipy", {}).get("complexity", 0)),
        -int(metrics.get("lizard", {}).get("ccn", 0)),
        -int(metrics.get("lizard", {}).get("nloc", 0)),
        -int(metrics.get("ruff", {}).get("complexity", 0)),
        item["file"],
        item["symbol"],
    )


def build_tool_summaries(
    *,
    ruff_signals: list[HotspotSignal],
    lizard_signals: list[HotspotSignal],
    complexipy_signals: list[HotspotSignal],
    dead_code_candidates: list[dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    return {
        "ruff": severity_summary(ruff_signals),
        "lizard": severity_summary(lizard_signals),
        "complexipy": severity_summary(complexipy_signals),
        "vulture": {
            "findings_total": len(dead_code_candidates),
            "review_candidate": sum(
                1
                for candidate in dead_code_candidates
                if candidate["classification"] == "review_candidate"
            ),
            "high_confidence_candidate": sum(
                1
                for candidate in dead_code_candidates
                if candidate["classification"] == "high_confidence_candidate"
            ),
        },
    }


def severity_summary(signals: list[HotspotSignal]) -> dict[str, int]:
    counter = Counter(signal.severity for signal in signals)
    return {
        "findings_total": len(signals),
        "warning": int(counter.get("warning", 0)),
        "high": int(counter.get("high", 0)),
        "critical": int(counter.get("critical", 0)),
    }


def severity_summary_from_levels(levels: Iterable[str]) -> dict[str, int]:
    counter = Counter(level for level in levels if level in SEVERITY_RANK)
    return {
        "findings_total": sum(counter.values()),
        "warning": int(counter.get("warning", 0)),
        "high": int(counter.get("high", 0)),
        "critical": int(counter.get("critical", 0)),
    }


def build_tool_summaries_from_snapshot(
    *, hotspots: list[dict[str, Any]], dead_code_candidates: list[dict[str, Any]]
) -> dict[str, dict[str, Any]]:
    severities_by_tool: dict[str, list[str]] = {
        "ruff": [],
        "lizard": [],
        "complexipy": [],
    }
    for hotspot in hotspots:
        for signal in hotspot.get("signals", []):
            tool = signal.get("tool")
            severity = signal.get("severity")
            if tool in severities_by_tool and isinstance(severity, str):
                severities_by_tool[tool].append(severity)

    return {
        "ruff": severity_summary_from_levels(severities_by_tool["ruff"]),
        "lizard": severity_summary_from_levels(severities_by_tool["lizard"]),
        "complexipy": severity_summary_from_levels(severities_by_tool["complexipy"]),
        "vulture": {
            "findings_total": len(dead_code_candidates),
            "review_candidate": sum(
                1
                for candidate in dead_code_candidates
                if candidate["classification"] == "review_candidate"
            ),
            "high_confidence_candidate": sum(
                1
                for candidate in dead_code_candidates
                if candidate["classification"] == "high_confidence_candidate"
            ),
        },
    }


def build_recommended_queue(hotspots: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = {name: [] for name in QUEUE_ORDER}
    for hotspot in hotspots:
        if hotspot["classification"] == "monitor":
            continue
        subsystem = hotspot["subsystem"]
        grouped.setdefault(subsystem, []).append(hotspot)

    queue: list[dict[str, Any]] = []
    for subsystem in QUEUE_ORDER:
        items = sorted(grouped.get(subsystem, []), key=hotspot_sort_key)
        queue.append(
            {
                "subsystem": subsystem,
                "hotspot_count": len(items),
                "refactor_now": sum(
                    1
                    for item in items
                    if item["classification"] == "refactor_now"
                ),
                "refactor_soon": sum(
                    1
                    for item in items
                    if item["classification"] == "refactor_soon"
                ),
                "top_hotspots": [
                    {
                        "id": item["id"],
                        "file": item["file"],
                        "symbol": item["symbol"],
                        "classification": item["classification"],
                    }
                    for item in items[:5]
                ],
            }
        )
    extras = [
        subsystem
        for subsystem in grouped
        if subsystem not in QUEUE_ORDER and grouped[subsystem]
    ]
    for subsystem in sorted(extras):
        items = sorted(grouped[subsystem], key=hotspot_sort_key)
        queue.append(
            {
                "subsystem": subsystem,
                "hotspot_count": len(items),
                "refactor_now": sum(
                    1
                    for item in items
                    if item["classification"] == "refactor_now"
                ),
                "refactor_soon": sum(
                    1
                    for item in items
                    if item["classification"] == "refactor_soon"
                ),
                "top_hotspots": [
                    {
                        "id": item["id"],
                        "file": item["file"],
                        "symbol": item["symbol"],
                        "classification": item["classification"],
                    }
                    for item in items[:5]
                ],
            }
        )
    return queue


def build_baseline_diff(
    *,
    current_hotspots: list[dict[str, Any]],
    current_dead_code_candidates: list[dict[str, Any]],
    baseline_report: dict[str, Any] | None,
    scope_files: list[str],
) -> dict[str, Any]:
    scoped_files = set(scope_files)
    if baseline_report is None:
        return {
            "baseline_available": False,
            "baseline_path": None,
            "has_regressions": False,
            "new": [],
            "worsened": [],
            "resolved": [],
        }

    baseline_hotspots = {
        item["id"]: item
        for item in baseline_report.get("hotspots", [])
        if item.get("file") in scoped_files
    }
    current_hotspots_by_id = {item["id"]: item for item in current_hotspots}
    baseline_dead_code = {
        item["id"]: item
        for item in baseline_report.get("dead_code_candidates", [])
        if item.get("file") in scoped_files
    }
    current_dead_code_by_id = {item["id"]: item for item in current_dead_code_candidates}

    diff_items = {"new": [], "worsened": [], "resolved": []}

    for hotspot_id, item in current_hotspots_by_id.items():
        previous = baseline_hotspots.get(hotspot_id)
        if previous is None:
            diff_items["new"].append(
                {
                    "kind": "hotspot",
                    "id": hotspot_id,
                    "file": item["file"],
                    "symbol": item["symbol"],
                    "after": summarize_hotspot(item),
                }
            )
            continue
        reasons = hotspot_regression_reasons(previous, item)
        if reasons:
            diff_items["worsened"].append(
                {
                    "kind": "hotspot",
                    "id": hotspot_id,
                    "file": item["file"],
                    "symbol": item["symbol"],
                    "before": summarize_hotspot(previous),
                    "after": summarize_hotspot(item),
                    "reasons": reasons,
                }
            )

    for hotspot_id, item in baseline_hotspots.items():
        if hotspot_id not in current_hotspots_by_id:
            diff_items["resolved"].append(
                {
                    "kind": "hotspot",
                    "id": hotspot_id,
                    "file": item["file"],
                    "symbol": item["symbol"],
                    "before": summarize_hotspot(item),
                }
            )

    for candidate_id, item in current_dead_code_by_id.items():
        previous = baseline_dead_code.get(candidate_id)
        if previous is None:
            diff_items["new"].append(
                {
                    "kind": "dead_code",
                    "id": candidate_id,
                    "file": item["file"],
                    "symbol": item["symbol"],
                    "after": summarize_dead_code(item),
                }
            )
            continue
        reasons = dead_code_regression_reasons(previous, item)
        if reasons:
            diff_items["worsened"].append(
                {
                    "kind": "dead_code",
                    "id": candidate_id,
                    "file": item["file"],
                    "symbol": item["symbol"],
                    "before": summarize_dead_code(previous),
                    "after": summarize_dead_code(item),
                    "reasons": reasons,
                }
            )

    for candidate_id, item in baseline_dead_code.items():
        if candidate_id not in current_dead_code_by_id:
            diff_items["resolved"].append(
                {
                    "kind": "dead_code",
                    "id": candidate_id,
                    "file": item["file"],
                    "symbol": item["symbol"],
                    "before": summarize_dead_code(item),
                }
            )

    for key in diff_items:
        diff_items[key].sort(key=lambda item: (item["kind"], item["file"], item["symbol"]))

    return {
        "baseline_available": True,
        "baseline_path": baseline_report.get("_baseline_path"),
        "has_regressions": bool(diff_items["new"] or diff_items["worsened"]),
        "new": diff_items["new"],
        "worsened": diff_items["worsened"],
        "resolved": diff_items["resolved"],
    }


def summarize_hotspot(item: dict[str, Any]) -> dict[str, Any]:
    return {
        "classification": item["classification"],
        "tools": item["tools"],
        "metrics": item["metrics"],
    }


def summarize_dead_code(item: dict[str, Any]) -> dict[str, Any]:
    return {
        "classification": item["classification"],
        "confidence": item["confidence"],
        "kind": item["kind"],
        "size": item.get("size"),
    }


def hotspot_regression_reasons(
    previous: dict[str, Any], current: dict[str, Any]
) -> list[str]:
    reasons: list[str] = []
    if HOTSPOT_CLASSIFICATION_RANK[current["classification"]] > HOTSPOT_CLASSIFICATION_RANK[
        previous["classification"]
    ]:
        reasons.append("classification")

    previous_metrics = previous.get("metrics", {})
    current_metrics = current.get("metrics", {})
    for tool_name, metric_name in (
        ("ruff", "complexity"),
        ("complexipy", "complexity"),
        ("lizard", "ccn"),
        ("lizard", "nloc"),
        ("lizard", "parameter_count"),
    ):
        old_value = int(previous_metrics.get(tool_name, {}).get(metric_name, 0))
        new_value = int(current_metrics.get(tool_name, {}).get(metric_name, 0))
        if new_value > old_value:
            reasons.append(f"{tool_name}.{metric_name}")

    if len(set(current.get("tools", []))) > len(set(previous.get("tools", []))):
        reasons.append("tool_overlap")
    return sorted(set(reasons))


def dead_code_regression_reasons(
    previous: dict[str, Any], current: dict[str, Any]
) -> list[str]:
    reasons: list[str] = []
    order = {"review_candidate": 1, "high_confidence_candidate": 2}
    if order[current["classification"]] > order[previous["classification"]]:
        reasons.append("classification")
    if int(current["confidence"]) > int(previous["confidence"]):
        reasons.append("confidence")
    return reasons


def build_repo_verdict(
    *, hotspots: list[dict[str, Any]], baseline_diff: dict[str, Any]
) -> dict[str, Any]:
    has_regressions = bool(baseline_diff.get("has_regressions"))
    current_refactor_now = [
        hotspot for hotspot in hotspots if hotspot["classification"] == "refactor_now"
    ]
    new_refactor_now = any(
        item["kind"] == "hotspot"
        and item["after"]["classification"] == "refactor_now"
        for item in baseline_diff.get("new", [])
    )
    if has_regressions or new_refactor_now:
        status = "corroding"
        summary = "Structural debt is regressing in the current scope."
    elif current_refactor_now or any(
        hotspot["classification"] == "refactor_soon" for hotspot in hotspots
    ):
        status = "strained"
        summary = "Existing hotspots remain, but the current scope did not regress."
    else:
        status = "stable"
        summary = "No refactor-now hotspots or regressions were detected."
    return {
        "status": status,
        "summary": summary,
        "has_regressions": has_regressions,
        "refactor_now_total": len(current_refactor_now),
    }


def build_summary(
    *,
    files: list[Path],
    hotspots: list[dict[str, Any]],
    dead_code_candidates: list[dict[str, Any]],
) -> dict[str, Any]:
    return build_summary_from_file_count(
        file_count=len(files),
        hotspots=hotspots,
        dead_code_candidates=dead_code_candidates,
    )


def build_summary_from_file_count(
    *,
    file_count: int,
    hotspots: list[dict[str, Any]],
    dead_code_candidates: list[dict[str, Any]],
) -> dict[str, Any]:
    hotspot_counter = Counter(item["classification"] for item in hotspots)
    dead_counter = Counter(item["classification"] for item in dead_code_candidates)
    return {
        "files_scanned": file_count,
        "hotspots_total": len(hotspots),
        "monitor_total": int(hotspot_counter.get("monitor", 0)),
        "refactor_soon_total": int(hotspot_counter.get("refactor_soon", 0)),
        "refactor_now_total": int(hotspot_counter.get("refactor_now", 0)),
        "dead_code_candidates_total": len(dead_code_candidates),
        "dead_code_high_confidence_total": int(
            dead_counter.get("high_confidence_candidate", 0)
        ),
    }


def render_markdown_report(report: dict[str, Any]) -> str:
    summary = report["summary"]
    repo_verdict = report["repo_verdict"]
    tool_summaries = report["tool_summaries"]
    hotspots = report["hotspots"]
    dead_code_candidates = report["dead_code_candidates"]
    baseline_diff = report["baseline_diff"]
    queue = report["recommended_refactor_queue"]

    lines = [
        "# Refactor Audit",
        "",
        "## Repo verdict",
        "",
        f"- Status: `{repo_verdict['status']}`",
        f"- Summary: {repo_verdict['summary']}",
        f"- Files scanned: {summary['files_scanned']}",
        f"- Hotspots: {summary['hotspots_total']} total, "
        f"{summary['refactor_now_total']} `refactor_now`, "
        f"{summary['refactor_soon_total']} `refactor_soon`, "
        f"{summary['monitor_total']} `monitor`",
        f"- Dead code candidates: {summary['dead_code_candidates_total']} total, "
        f"{summary['dead_code_high_confidence_total']} high-confidence",
        "",
        "## Tool summaries",
        "",
        "| Tool | Total | Warning | High | Critical |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    for tool_name in ("ruff", "lizard", "complexipy"):
        item = tool_summaries[tool_name]
        lines.append(
            f"| {tool_name} | {item['findings_total']} | {item['warning']} | "
            f"{item['high']} | {item['critical']} |"
        )
    vulture_summary = tool_summaries["vulture"]
    lines.extend(
        [
            "",
            f"Vulture candidates: {vulture_summary['findings_total']} total, "
            f"{vulture_summary['high_confidence_candidate']} high-confidence, "
            f"{vulture_summary['review_candidate']} review candidates.",
            "",
            "## Top hotspots",
            "",
            "| Classification | Tools | File | Symbol | Notes |",
            "| --- | ---: | --- | --- | --- |",
        ]
    )
    if hotspots:
        for hotspot in hotspots[:15]:
            notes = ", ".join(
                f"{tool}:{format_tool_metrics(tool, hotspot['metrics'][tool])}"
                for tool in hotspot["tools"]
            )
            lines.append(
                f"| {hotspot['classification']} | {hotspot['tool_count']} | "
                f"{hotspot['file']} | {hotspot['symbol']} | {notes} |"
            )
    else:
        lines.append("| none | 0 | - | - | - |")

    lines.extend(
        [
            "",
            "## Dead code candidates",
            "",
            "| Classification | Confidence | File | Symbol | Kind |",
            "| --- | ---: | --- | --- | --- |",
        ]
    )
    if dead_code_candidates:
        for candidate in dead_code_candidates[:15]:
            lines.append(
                f"| {candidate['classification']} | {candidate['confidence']}% | "
                f"{candidate['file']} | {candidate['symbol']} | {candidate['kind']} |"
            )
    else:
        lines.append("| none | 0 | - | - | - |")

    lines.extend(
        [
            "",
            "## Baseline diff",
            "",
            f"- Baseline available: {baseline_diff['baseline_available']}",
            f"- Regressions detected: {baseline_diff['has_regressions']}",
            f"- New: {len(baseline_diff['new'])}",
            f"- Worsened: {len(baseline_diff['worsened'])}",
            f"- Resolved: {len(baseline_diff['resolved'])}",
        ]
    )
    for label in ("new", "worsened", "resolved"):
        items = baseline_diff[label]
        if not items:
            continue
        lines.extend(["", f"### {label.title()}", ""])
        for item in items[:10]:
            lines.append(
                f"- `{item['kind']}` {item['file']} :: {item['symbol']}"
            )

    lines.extend(
        [
            "",
            "## Recommended refactor queue",
            "",
            "| Subsystem | Hotspots | Refactor now | Refactor soon |",
            "| --- | ---: | ---: | ---: |",
        ]
    )
    for item in queue:
        lines.append(
            f"| {item['subsystem']} | {item['hotspot_count']} | "
            f"{item['refactor_now']} | {item['refactor_soon']} |"
        )
    return "\n".join(lines) + "\n"


def format_tool_metrics(tool_name: str, metrics: dict[str, int]) -> str:
    if tool_name == "lizard":
        return (
            f"CCN={metrics.get('ccn', 0)}, "
            f"NLOC={metrics.get('nloc', 0)}, "
            f"PARAM={metrics.get('parameter_count', 0)}"
        )
    if tool_name in {"ruff", "complexipy"}:
        return f"complexity={metrics.get('complexity', 0)}"
    return ", ".join(f"{key}={value}" for key, value in sorted(metrics.items()))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def build_baseline_snapshot(
    report: dict[str, Any],
    *,
    baseline_report: dict[str, Any] | None = None,
    scope_files: Iterable[str] | None = None,
) -> dict[str, Any]:
    snapshot = dict(report)
    scoped_file_set = set(scope_files or [])
    if baseline_report is not None and scoped_file_set:
        snapshot["hotspots"] = sorted(
            [
                item
                for item in baseline_report.get("hotspots", [])
                if item.get("file") not in scoped_file_set
            ]
            + snapshot["hotspots"],
            key=hotspot_sort_key,
        )
        snapshot["dead_code_candidates"] = sorted(
            [
                item
                for item in baseline_report.get("dead_code_candidates", [])
                if item.get("file") not in scoped_file_set
            ]
            + snapshot["dead_code_candidates"],
            key=dead_code_sort_key,
        )
        preserved_scope = baseline_report.get("scope", snapshot["scope"])
        scope_files_value = preserved_scope.get("files", [])
        file_count = preserved_scope.get("file_count", len(scope_files_value))
        snapshot["scope"] = preserved_scope
        snapshot["summary"] = build_summary_from_file_count(
            file_count=int(file_count),
            hotspots=snapshot["hotspots"],
            dead_code_candidates=snapshot["dead_code_candidates"],
        )
        snapshot["tool_summaries"] = build_tool_summaries_from_snapshot(
            hotspots=snapshot["hotspots"],
            dead_code_candidates=snapshot["dead_code_candidates"],
        )
        snapshot["recommended_refactor_queue"] = build_recommended_queue(
            snapshot["hotspots"]
        )
    snapshot["baseline_diff"] = {
        "baseline_available": False,
        "baseline_path": None,
        "has_regressions": False,
        "new": [],
        "worsened": [],
        "resolved": [],
    }
    snapshot["repo_verdict"] = build_repo_verdict(
        hotspots=snapshot["hotspots"],
        baseline_diff=snapshot["baseline_diff"],
    )
    return snapshot


def run_refactor_audit(
    *,
    scope_targets: list[str],
    out_dir: Path,
    baseline_path: Path,
    update_baseline: bool,
    fail_on_regression: bool,
    config: AuditConfig,
) -> tuple[int, dict[str, Any]]:
    files = collect_python_files(
        repo_root=config.repo_root,
        targets=scope_targets,
        exclude_patterns=config.exclude,
    )
    default_scope_files = collect_python_files(
        repo_root=config.repo_root,
        targets=list(config.targets),
        exclude_patterns=config.exclude,
    )
    if not files:
        raise RuntimeError("No Python files matched the requested scope.")
    lookup = ScopeLookup.from_files(repo_root=config.repo_root, files=files)
    out_dir.mkdir(parents=True, exist_ok=True)
    raw_dir = out_dir / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)

    file_args = [str(path) for path in files]

    ruff_raw = raw_dir / "ruff.json"
    ruff_completed = run_command(
        [
            "ruff",
            "check",
            *file_args,
            "--select",
            "C90",
            "--output-format",
            "json",
        ],
        cwd=config.repo_root,
        allowed_returncodes={0, 1},
    )
    ruff_raw.write_text(ruff_completed.stdout or "[]", encoding="utf-8")
    ruff_signals = parse_ruff_findings(
        raw_text=ruff_completed.stdout, lookup=lookup, config=config
    )

    lizard_raw = raw_dir / "lizard.csv"
    lizard_completed = run_command(
        ["lizard", *file_args, "-l", "python", "--csv"],
        cwd=config.repo_root,
        allowed_returncodes={0, 1},
    )
    lizard_raw.write_text(lizard_completed.stdout, encoding="utf-8")
    lizard_signals = parse_lizard_findings(
        raw_text=lizard_completed.stdout, lookup=lookup, config=config
    )

    complexipy_raw = raw_dir / "complexipy.json"
    with tempfile.TemporaryDirectory(
        dir=raw_dir, prefix="complexipy-run-"
    ) as complexipy_temp_dir:
        temp_dir_path = Path(complexipy_temp_dir)
        complexipy_completed = run_command(
            [
                "complexipy",
                *file_args,
                "--max-complexity-allowed",
                str(config.complexipy.warning_min - 1),
                "--output-json",
                "--color",
                "no",
            ],
            cwd=temp_dir_path,
            allowed_returncodes={0, 1},
        )
        generated_complexipy = list(temp_dir_path.glob("complexipy_results_*.json"))
        if not generated_complexipy:
            raise RuntimeError(
                "complexipy did not emit a JSON report. "
                + (complexipy_completed.stderr.strip() or complexipy_completed.stdout.strip())
            )
        latest_complexipy = max(
            generated_complexipy, key=lambda path: path.stat().st_mtime_ns
        )
        complexipy_raw.write_text(
            latest_complexipy.read_text(encoding="utf-8"),
            encoding="utf-8",
        )
    complexipy_signals = parse_complexipy_findings(
        raw_text=complexipy_raw.read_text(encoding="utf-8"),
        lookup=lookup,
        config=config,
    )

    vulture_raw = raw_dir / "vulture.txt"
    vulture_completed = run_command(
        ["vulture", *file_args, "--min-confidence", str(config.vulture.review_candidate_min)],
        cwd=config.repo_root,
        allowed_returncodes={0, 3},
    )
    vulture_raw.write_text(vulture_completed.stdout, encoding="utf-8")
    dead_code_candidates = parse_vulture_candidates(
        raw_text=vulture_completed.stdout, lookup=lookup, config=config
    )

    current_scope_files = [relative_path(path, config.repo_root) for path in files]
    full_scope_file_set = {
        relative_path(path, config.repo_root) for path in default_scope_files
    }
    is_partial_scope = set(current_scope_files) != full_scope_file_set

    hotspots = aggregate_hotspots(ruff_signals + lizard_signals + complexipy_signals)
    tool_summaries = build_tool_summaries(
        ruff_signals=ruff_signals,
        lizard_signals=lizard_signals,
        complexipy_signals=complexipy_signals,
        dead_code_candidates=dead_code_candidates,
    )

    baseline_report: dict[str, Any] | None = None
    if baseline_path.exists():
        baseline_report = json.loads(baseline_path.read_text(encoding="utf-8"))
        if baseline_report is not None:
            baseline_report["_baseline_path"] = str(baseline_path)
    baseline_diff = build_baseline_diff(
        current_hotspots=hotspots,
        current_dead_code_candidates=dead_code_candidates,
        baseline_report=baseline_report,
        scope_files=current_scope_files,
    )
    repo_verdict = build_repo_verdict(hotspots=hotspots, baseline_diff=baseline_diff)
    summary = build_summary(
        files=files, hotspots=hotspots, dead_code_candidates=dead_code_candidates
    )
    report = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": datetime.now(UTC).isoformat(),
        "scope": {
            "requested_targets": scope_targets,
            "files": current_scope_files,
            "file_count": len(files),
            "repo_root": str(config.repo_root),
        },
        "summary": summary,
        "repo_verdict": repo_verdict,
        "tool_summaries": tool_summaries,
        "hotspots": hotspots,
        "dead_code_candidates": dead_code_candidates,
        "baseline_diff": baseline_diff,
        "recommended_refactor_queue": build_recommended_queue(hotspots),
    }

    write_json(out_dir / "report.json", report)
    (out_dir / "report.md").write_text(render_markdown_report(report), encoding="utf-8")
    if update_baseline:
        if is_partial_scope and baseline_report is None:
            raise RuntimeError(
                "--update-baseline requires an existing baseline when auditing a partial scope."
            )
        write_json(
            baseline_path,
            build_baseline_snapshot(
                report,
                baseline_report=baseline_report if is_partial_scope else None,
                scope_files=current_scope_files if is_partial_scope else None,
            ),
        )

    exit_code = 0
    if fail_on_regression and baseline_diff["has_regressions"]:
        exit_code = 1
    return exit_code, report


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Audit refactor hotspots using ruff, lizard, complexipy, and vulture."
    )
    parser.add_argument(
        "paths",
        nargs="*",
        help="Optional files or directories to audit. Defaults to tool.recoleta_refactor.targets.",
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        help="Override the report output directory.",
    )
    parser.add_argument(
        "--baseline",
        type=Path,
        help="Override the baseline JSON path.",
    )
    parser.add_argument(
        "--update-baseline",
        action="store_true",
        help="Write the current report to the baseline path.",
    )
    parser.add_argument(
        "--fail-on-regression",
        action="store_true",
        help="Exit non-zero when the current scope regresses relative to the baseline.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    config = load_audit_config()
    scope_targets = args.paths or list(config.targets)
    out_dir = (
        args.out_dir.resolve()
        if args.out_dir is not None
        else config.out_dir
    )
    baseline_path = (
        args.baseline.resolve()
        if args.baseline is not None
        else config.baseline
    )
    exit_code, report = run_refactor_audit(
        scope_targets=scope_targets,
        out_dir=out_dir,
        baseline_path=baseline_path,
        update_baseline=bool(args.update_baseline),
        fail_on_regression=bool(args.fail_on_regression),
        config=config,
    )
    print(
        f"[{report['repo_verdict']['status']}] {report['repo_verdict']['summary']} "
        f"Report: {out_dir / 'report.md'}"
    )
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
