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
from typing import Any, Callable, Iterable, Literal, cast

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
_VULTURE_IGNORED_DECORATORS = frozenset(
    {
        "field_validator",
        "model_validator",
        "field_serializer",
        "model_serializer",
    }
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
    vulture_ignored_lines_by_path: dict[str, frozenset[int]]

    @classmethod
    def from_files(cls, *, repo_root: Path, files: list[Path]) -> ScopeLookup:
        rel_paths = [relative_path(path, repo_root) for path in files]
        grouped: dict[str, list[str]] = defaultdict(list)
        qualified_names_by_path: dict[str, frozenset[str]] = {}
        qualified_names_by_path_and_leaf: dict[str, dict[str, tuple[str, ...]]] = {}
        qualified_names_by_path_and_line: dict[str, dict[int, str]] = {}
        vulture_ignored_lines_by_path: dict[str, frozenset[int]] = {}
        for rel_path in rel_paths:
            grouped[Path(rel_path).name].append(rel_path)
            path = repo_root / rel_path
            symbol_index = build_symbol_index(path)
            qualified_names_by_path[rel_path] = frozenset(
                symbol_index["qualified_names"]
            )
            qualified_names_by_path_and_leaf[rel_path] = symbol_index["by_leaf"]
            qualified_names_by_path_and_line[rel_path] = symbol_index["by_line"]
            vulture_ignored_lines_by_path[rel_path] = frozenset(
                symbol_index["vulture_ignored_lines"]
            )
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
            vulture_ignored_lines_by_path=vulture_ignored_lines_by_path,
        )


@dataclass(frozen=True)
class RefactorAuditRunRequest:
    scope_targets: list[str]
    out_dir: Path
    baseline_path: Path
    update_baseline: bool
    fail_on_regression: bool
    config: AuditConfig


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


@dataclass(frozen=True)
class AuditScopeState:
    files: list[Path]
    current_scope_files: list[str]
    is_partial_scope: bool
    lookup: ScopeLookup
    raw_dir: Path


@dataclass(frozen=True)
class AuditToolRunResult:
    ruff_signals: list[HotspotSignal]
    lizard_signals: list[HotspotSignal]
    complexipy_signals: list[HotspotSignal]
    dead_code_candidates: list[dict[str, Any]]


@dataclass(frozen=True)
class _DiffRegressionContext:
    current_items_by_id: dict[str, dict[str, Any]]
    baseline_items_by_id: dict[str, dict[str, Any]]
    kind: str
    summarize: Callable[[dict[str, Any]], dict[str, Any]]
    regression_reasons: Callable[[dict[str, Any], dict[str, Any]], list[str]]


@dataclass(frozen=True)
class _AuditReportContext:
    request: RefactorAuditRunRequest
    scope_state: AuditScopeState
    hotspots: list[dict[str, Any]]
    dead_code_candidates: list[dict[str, Any]]
    tool_summaries: dict[str, dict[str, Any]]
    baseline_diff: dict[str, Any]
    repo_verdict: dict[str, Any]


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


@dataclass
class _SymbolIndexBuffers:
    qualified_names: list[str]
    by_leaf: dict[str, list[str]]
    by_line: dict[int, str]
    vulture_ignored_lines: set[int]


def build_symbol_index(path: Path) -> dict[str, Any]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    buffers = _SymbolIndexBuffers(
        qualified_names=[],
        by_leaf=defaultdict(list),
        by_line={},
        vulture_ignored_lines=set(),
    )

    def walk(node: ast.AST, prefix: str = "", parent_kind: str | None = None) -> None:
        body = getattr(node, "body", None)
        if not isinstance(body, list):
            return
        for child in body:
            if isinstance(child, ast.ClassDef):
                qualified = _qualified_symbol_name(
                    prefix=prefix,
                    parent_kind=parent_kind,
                    child_name=child.name,
                    child_kind="class",
                )
                walk(child, qualified, "class")
                continue
            if isinstance(child, ast.AsyncFunctionDef | ast.FunctionDef):
                qualified = _qualified_symbol_name(
                    prefix=prefix,
                    parent_kind=parent_kind,
                    child_name=child.name,
                    child_kind="function",
                )
                _record_function_symbol(
                    node=child,
                    qualified=qualified,
                    buffers=buffers,
                )
                walk(child, qualified, "function")

    walk(tree)
    return {
        "qualified_names": tuple(sorted(buffers.qualified_names)),
        "by_leaf": {
            leaf: tuple(sorted(values))
            for leaf, values in sorted(buffers.by_leaf.items())
        },
        "by_line": dict(sorted(buffers.by_line.items())),
        "vulture_ignored_lines": tuple(sorted(buffers.vulture_ignored_lines)),
    }


def _qualified_symbol_name(
    *,
    prefix: str,
    parent_kind: str | None,
    child_name: str,
    child_kind: Literal["class", "function"],
) -> str:
    if not prefix:
        return child_name
    if child_kind == "class" or parent_kind == "class":
        return f"{prefix}::{child_name}"
    return f"{prefix}.{child_name}"


def _record_function_symbol(
    *,
    node: ast.FunctionDef | ast.AsyncFunctionDef,
    qualified: str,
    buffers: _SymbolIndexBuffers,
) -> None:
    buffers.qualified_names.append(qualified)
    buffers.by_line[int(node.lineno)] = qualified
    buffers.by_leaf[node.name].append(qualified)
    if _has_vulture_ignored_decorator(node):
        buffers.vulture_ignored_lines.update(_vulture_ignored_line_span(node))


def _has_vulture_ignored_decorator(
    node: ast.FunctionDef | ast.AsyncFunctionDef,
) -> bool:
    return any(
        _decorator_base_name(decorator) in _VULTURE_IGNORED_DECORATORS
        for decorator in node.decorator_list
    )


def _decorator_base_name(node: ast.AST) -> str:
    if isinstance(node, ast.Call):
        return _decorator_base_name(node.func)
    if isinstance(node, ast.Name):
        return str(node.id)
    if isinstance(node, ast.Attribute):
        return str(node.attr)
    return ""


def _vulture_ignored_line_span(
    node: ast.FunctionDef | ast.AsyncFunctionDef,
) -> set[int]:
    if not node.decorator_list:
        return {int(node.lineno)}
    start_line = min(
        int(getattr(decorator, "lineno", node.lineno))
        for decorator in node.decorator_list
    )
    end_line = int(node.lineno)
    return set(range(start_line, end_line + 1))


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
        ranked = [value for value in severities.values() if value is not None]
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
        rel_path = resolve_reported_path(
            str(item.get("path") or item.get("file_name")), lookup
        )
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
        line_number = int(match.group("line"))
        if line_number in lookup.vulture_ignored_lines_by_path.get(
            rel_path, frozenset()
        ):
            continue
        symbol = match.group("symbol")
        kind = match.group("kind")
        candidates.append(
            {
                "id": f"{rel_path}::{kind}::{symbol}",
                "file": rel_path,
                "line": line_number,
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
    if rel_path.startswith("recoleta/sources") or rel_path.startswith(
        "recoleta/extract"
    ):
        return "sources"
    if (
        rel_path.startswith("recoleta/site")
        or rel_path.startswith("recoleta/publish")
        or rel_path.startswith("recoleta/presentation")
        or rel_path.startswith("recoleta/trend_materialize")
    ):
        return "site/render"
    return "other"


def _classify_hotspot(values: list[HotspotSignal]) -> str:
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
        return "refactor_now"
    if (
        any(signal.severity in {"high", "critical"} for signal in values)
        or len(distinct_warning_plus) >= 2
    ):
        return "refactor_soon"
    return "monitor"


def _hotspot_metrics_by_tool(values: list[HotspotSignal]) -> dict[str, dict[str, int]]:
    metrics_by_tool: dict[str, dict[str, int]] = {}
    for signal in values:
        existing = metrics_by_tool.setdefault(signal.tool, {})
        for key, value in signal.metrics.items():
            existing[key] = max(existing.get(key, value), value)
    return metrics_by_tool


def _hotspot_signal_payload(values: list[HotspotSignal]) -> list[dict[str, Any]]:
    return [
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
    ]


def _aggregate_hotspot_record(
    *,
    hotspot_id: str,
    values: list[HotspotSignal],
) -> dict[str, Any]:
    line_candidates = [signal.line for signal in values if signal.line is not None]
    return {
        "id": hotspot_id,
        "file": values[0].file,
        "symbol": max((signal.symbol for signal in values), key=len),
        "line": min(line_candidates) if line_candidates else None,
        "classification": _classify_hotspot(values),
        "subsystem": infer_subsystem(values[0].file),
        "tool_count": len({signal.tool for signal in values}),
        "tools": sorted({signal.tool for signal in values}),
        "metrics": _hotspot_metrics_by_tool(values),
        "signals": _hotspot_signal_payload(values),
    }


def aggregate_hotspots(signals: list[HotspotSignal]) -> list[dict[str, Any]]:
    grouped: dict[str, list[HotspotSignal]] = defaultdict(list)
    for signal in signals:
        grouped[signal.symbol_key].append(signal)

    hotspots = [
        _aggregate_hotspot_record(hotspot_id=hotspot_id, values=values)
        for hotspot_id, values in grouped.items()
    ]
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
                    1 for item in items if item["classification"] == "refactor_now"
                ),
                "refactor_soon": sum(
                    1 for item in items if item["classification"] == "refactor_soon"
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
                    1 for item in items if item["classification"] == "refactor_now"
                ),
                "refactor_soon": sum(
                    1 for item in items if item["classification"] == "refactor_soon"
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
        return _empty_baseline_diff()

    baseline_hotspots = _baseline_items_by_id(
        baseline_report=baseline_report,
        key="hotspots",
        scoped_files=scoped_files,
    )
    current_hotspots_by_id = {item["id"]: item for item in current_hotspots}
    baseline_dead_code = _baseline_items_by_id(
        baseline_report=baseline_report,
        key="dead_code_candidates",
        scoped_files=scoped_files,
    )
    current_dead_code_by_id = {
        item["id"]: item for item in current_dead_code_candidates
    }

    diff_items = {"new": [], "worsened": [], "resolved": []}
    _collect_item_regressions(
        diff_items=diff_items,
        context=_DiffRegressionContext(
            current_items_by_id=current_hotspots_by_id,
            baseline_items_by_id=baseline_hotspots,
            kind="hotspot",
            summarize=summarize_hotspot,
            regression_reasons=hotspot_regression_reasons,
        ),
    )
    _collect_resolved_items(
        diff_items=diff_items,
        current_items_by_id=current_hotspots_by_id,
        baseline_items_by_id=baseline_hotspots,
        kind="hotspot",
        summarize=summarize_hotspot,
    )
    _collect_item_regressions(
        diff_items=diff_items,
        context=_DiffRegressionContext(
            current_items_by_id=current_dead_code_by_id,
            baseline_items_by_id=baseline_dead_code,
            kind="dead_code",
            summarize=summarize_dead_code,
            regression_reasons=dead_code_regression_reasons,
        ),
    )
    _collect_resolved_items(
        diff_items=diff_items,
        current_items_by_id=current_dead_code_by_id,
        baseline_items_by_id=baseline_dead_code,
        kind="dead_code",
        summarize=summarize_dead_code,
    )
    _sort_diff_items(diff_items)

    return {
        "baseline_available": True,
        "baseline_path": baseline_report.get("_baseline_path"),
        "has_regressions": bool(diff_items["new"] or diff_items["worsened"]),
        "new": diff_items["new"],
        "worsened": diff_items["worsened"],
        "resolved": diff_items["resolved"],
    }


def _empty_baseline_diff() -> dict[str, Any]:
    return {
        "baseline_available": False,
        "baseline_path": None,
        "has_regressions": False,
        "new": [],
        "worsened": [],
        "resolved": [],
    }


def _baseline_items_by_id(
    *,
    baseline_report: dict[str, Any],
    key: str,
    scoped_files: set[str],
) -> dict[str, dict[str, Any]]:
    return {
        item["id"]: item
        for item in baseline_report.get(key, [])
        if item.get("file") in scoped_files
    }


def _collect_item_regressions(
    *,
    diff_items: dict[str, list[dict[str, Any]]],
    context: _DiffRegressionContext,
) -> None:
    for item_id, item in context.current_items_by_id.items():
        previous = context.baseline_items_by_id.get(item_id)
        if previous is None:
            diff_items["new"].append(
                {
                    "kind": context.kind,
                    "id": item_id,
                    "file": item["file"],
                    "symbol": item["symbol"],
                    "after": context.summarize(item),
                }
            )
            continue
        reasons = context.regression_reasons(previous, item)
        if reasons:
            diff_items["worsened"].append(
                {
                    "kind": context.kind,
                    "id": item_id,
                    "file": item["file"],
                    "symbol": item["symbol"],
                    "before": context.summarize(previous),
                    "after": context.summarize(item),
                    "reasons": reasons,
                }
            )


def _collect_resolved_items(
    *,
    diff_items: dict[str, list[dict[str, Any]]],
    current_items_by_id: dict[str, dict[str, Any]],
    baseline_items_by_id: dict[str, dict[str, Any]],
    kind: str,
    summarize: Callable[[dict[str, Any]], dict[str, Any]],
) -> None:
    for item_id, item in baseline_items_by_id.items():
        if item_id in current_items_by_id:
            continue
        diff_items["resolved"].append(
            {
                "kind": kind,
                "id": item_id,
                "file": item["file"],
                "symbol": item["symbol"],
                "before": summarize(item),
            }
        )


def _sort_diff_items(diff_items: dict[str, list[dict[str, Any]]]) -> None:
    for key in diff_items:
        diff_items[key].sort(
            key=lambda item: (item["kind"], item["file"], item["symbol"])
        )


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
    if (
        HOTSPOT_CLASSIFICATION_RANK[current["classification"]]
        > HOTSPOT_CLASSIFICATION_RANK[previous["classification"]]
    ):
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
        item["kind"] == "hotspot" and item["after"]["classification"] == "refactor_now"
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
            lines.append(f"- `{item['kind']}` {item['file']} :: {item['symbol']}")

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


def _coerce_refactor_audit_run_request(
    *,
    request: RefactorAuditRunRequest | None = None,
    legacy_kwargs: dict[str, Any] | None = None,
) -> RefactorAuditRunRequest:
    if request is not None:
        return request
    values = dict(legacy_kwargs or {})
    return RefactorAuditRunRequest(
        scope_targets=list(values["scope_targets"]),
        out_dir=Path(values["out_dir"]),
        baseline_path=Path(values["baseline_path"]),
        update_baseline=bool(values["update_baseline"]),
        fail_on_regression=bool(values["fail_on_regression"]),
        config=values["config"],
    )


def _prepare_audit_scope(request: RefactorAuditRunRequest) -> AuditScopeState:
    files = collect_python_files(
        repo_root=request.config.repo_root,
        targets=request.scope_targets,
        exclude_patterns=request.config.exclude,
    )
    default_scope_files = collect_python_files(
        repo_root=request.config.repo_root,
        targets=list(request.config.targets),
        exclude_patterns=request.config.exclude,
    )
    if not files:
        raise RuntimeError("No Python files matched the requested scope.")
    lookup = ScopeLookup.from_files(repo_root=request.config.repo_root, files=files)
    request.out_dir.mkdir(parents=True, exist_ok=True)
    raw_dir = request.out_dir / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)
    current_scope_files = [
        relative_path(path, request.config.repo_root) for path in files
    ]
    full_scope_file_set = {
        relative_path(path, request.config.repo_root) for path in default_scope_files
    }
    return AuditScopeState(
        files=files,
        current_scope_files=current_scope_files,
        is_partial_scope=set(current_scope_files) != full_scope_file_set,
        lookup=lookup,
        raw_dir=raw_dir,
    )


def _run_ruff_audit(
    *,
    file_args: list[str],
    raw_dir: Path,
    lookup: ScopeLookup,
    config: AuditConfig,
) -> list[HotspotSignal]:
    completed = run_command(
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
    raw_path = raw_dir / "ruff.json"
    raw_path.write_text(completed.stdout or "[]", encoding="utf-8")
    return parse_ruff_findings(
        raw_text=completed.stdout,
        lookup=lookup,
        config=config,
    )


def _run_lizard_audit(
    *,
    file_args: list[str],
    raw_dir: Path,
    lookup: ScopeLookup,
    config: AuditConfig,
) -> list[HotspotSignal]:
    completed = run_command(
        ["lizard", *file_args, "-l", "python", "--csv"],
        cwd=config.repo_root,
        allowed_returncodes={0, 1},
    )
    raw_path = raw_dir / "lizard.csv"
    raw_path.write_text(completed.stdout, encoding="utf-8")
    return parse_lizard_findings(
        raw_text=completed.stdout,
        lookup=lookup,
        config=config,
    )


def _run_complexipy_audit(
    *,
    file_args: list[str],
    raw_dir: Path,
    lookup: ScopeLookup,
    config: AuditConfig,
) -> list[HotspotSignal]:
    raw_path = raw_dir / "complexipy.json"
    with tempfile.TemporaryDirectory(
        dir=raw_dir,
        prefix="complexipy-run-",
    ) as complexipy_temp_dir:
        temp_dir_path = Path(complexipy_temp_dir)
        completed = run_command(
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
        generated = list(temp_dir_path.glob("complexipy_results_*.json"))
        if not generated:
            raise RuntimeError(
                "complexipy did not emit a JSON report. "
                + (completed.stderr.strip() or completed.stdout.strip())
            )
        latest = max(generated, key=lambda path: path.stat().st_mtime_ns)
        raw_path.write_text(
            latest.read_text(encoding="utf-8"),
            encoding="utf-8",
        )
    return parse_complexipy_findings(
        raw_text=raw_path.read_text(encoding="utf-8"),
        lookup=lookup,
        config=config,
    )


def _run_vulture_audit(
    *,
    file_args: list[str],
    raw_dir: Path,
    lookup: ScopeLookup,
    config: AuditConfig,
) -> list[dict[str, Any]]:
    completed = run_command(
        [
            "vulture",
            *file_args,
            "--min-confidence",
            str(config.vulture.review_candidate_min),
        ],
        cwd=config.repo_root,
        allowed_returncodes={0, 3},
    )
    raw_path = raw_dir / "vulture.txt"
    raw_path.write_text(completed.stdout, encoding="utf-8")
    return parse_vulture_candidates(
        raw_text=completed.stdout,
        lookup=lookup,
        config=config,
    )


def _run_audit_tools(
    scope_state: AuditScopeState,
    request: RefactorAuditRunRequest,
) -> AuditToolRunResult:
    file_args = [str(path) for path in scope_state.files]
    return AuditToolRunResult(
        ruff_signals=_run_ruff_audit(
            file_args=file_args,
            raw_dir=scope_state.raw_dir,
            lookup=scope_state.lookup,
            config=request.config,
        ),
        lizard_signals=_run_lizard_audit(
            file_args=file_args,
            raw_dir=scope_state.raw_dir,
            lookup=scope_state.lookup,
            config=request.config,
        ),
        complexipy_signals=_run_complexipy_audit(
            file_args=file_args,
            raw_dir=scope_state.raw_dir,
            lookup=scope_state.lookup,
            config=request.config,
        ),
        dead_code_candidates=_run_vulture_audit(
            file_args=file_args,
            raw_dir=scope_state.raw_dir,
            lookup=scope_state.lookup,
            config=request.config,
        ),
    )


def _load_baseline_report(baseline_path: Path) -> dict[str, Any] | None:
    if not baseline_path.exists():
        return None
    baseline_report = json.loads(baseline_path.read_text(encoding="utf-8"))
    baseline_report["_baseline_path"] = str(baseline_path)
    return baseline_report


def _build_audit_report(
    context: _AuditReportContext,
) -> dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "generated_at": datetime.now(UTC).isoformat(),
        "scope": {
            "requested_targets": context.request.scope_targets,
            "files": context.scope_state.current_scope_files,
            "file_count": len(context.scope_state.files),
            "repo_root": str(context.request.config.repo_root),
        },
        "summary": build_summary(
            files=context.scope_state.files,
            hotspots=context.hotspots,
            dead_code_candidates=context.dead_code_candidates,
        ),
        "repo_verdict": context.repo_verdict,
        "tool_summaries": context.tool_summaries,
        "hotspots": context.hotspots,
        "dead_code_candidates": context.dead_code_candidates,
        "baseline_diff": context.baseline_diff,
        "recommended_refactor_queue": build_recommended_queue(context.hotspots),
    }


def _write_audit_outputs(*, out_dir: Path, report: dict[str, Any]) -> None:
    write_json(out_dir / "report.json", report)
    (out_dir / "report.md").write_text(render_markdown_report(report), encoding="utf-8")


def _maybe_update_baseline(
    *,
    request: RefactorAuditRunRequest,
    scope_state: AuditScopeState,
    baseline_report: dict[str, Any] | None,
    report: dict[str, Any],
) -> None:
    if not request.update_baseline:
        return
    if scope_state.is_partial_scope and baseline_report is None:
        raise RuntimeError(
            "--update-baseline requires an existing baseline when auditing a partial scope."
        )
    write_json(
        request.baseline_path,
        build_baseline_snapshot(
            report,
            baseline_report=baseline_report if scope_state.is_partial_scope else None,
            scope_files=scope_state.current_scope_files
            if scope_state.is_partial_scope
            else None,
        ),
    )


def run_refactor_audit(
    request: RefactorAuditRunRequest | None = None,
    **legacy_kwargs: Any,
) -> tuple[int, dict[str, Any]]:
    resolved_request = _coerce_refactor_audit_run_request(
        request=request,
        legacy_kwargs=legacy_kwargs,
    )
    scope_state = _prepare_audit_scope(resolved_request)
    tool_run = _run_audit_tools(scope_state, resolved_request)
    hotspots = aggregate_hotspots(
        tool_run.ruff_signals + tool_run.lizard_signals + tool_run.complexipy_signals
    )
    tool_summaries = build_tool_summaries(
        ruff_signals=tool_run.ruff_signals,
        lizard_signals=tool_run.lizard_signals,
        complexipy_signals=tool_run.complexipy_signals,
        dead_code_candidates=tool_run.dead_code_candidates,
    )
    baseline_report = _load_baseline_report(resolved_request.baseline_path)
    baseline_diff = build_baseline_diff(
        current_hotspots=hotspots,
        current_dead_code_candidates=tool_run.dead_code_candidates,
        baseline_report=baseline_report,
        scope_files=scope_state.current_scope_files,
    )
    repo_verdict = build_repo_verdict(hotspots=hotspots, baseline_diff=baseline_diff)
    report = _build_audit_report(
        _AuditReportContext(
            request=resolved_request,
            scope_state=scope_state,
            hotspots=hotspots,
            dead_code_candidates=tool_run.dead_code_candidates,
            tool_summaries=tool_summaries,
            baseline_diff=baseline_diff,
            repo_verdict=repo_verdict,
        )
    )
    _write_audit_outputs(out_dir=resolved_request.out_dir, report=report)
    _maybe_update_baseline(
        request=resolved_request,
        scope_state=scope_state,
        baseline_report=baseline_report,
        report=report,
    )
    exit_code = int(
        bool(resolved_request.fail_on_regression and baseline_diff["has_regressions"])
    )
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
    out_dir = args.out_dir.resolve() if args.out_dir is not None else config.out_dir
    baseline_path = (
        args.baseline.resolve() if args.baseline is not None else config.baseline
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
