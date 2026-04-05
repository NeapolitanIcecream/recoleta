from __future__ import annotations

from dataclasses import dataclass
import hashlib
from pathlib import Path
from typing import Any

from loguru import logger


@dataclass(frozen=True, slots=True)
class VectorRow:
    chunk_id: int
    doc_id: int
    doc_type: str
    chunk_index: int
    kind: str
    text_hash: str
    text_preview: str
    event_start_ts: float
    event_end_ts: float
    vector: list[float]


@dataclass(frozen=True, slots=True)
class VectorSearchRequest:
    query_vector: list[float]
    where: str
    limit: int
    metric: str = "cosine"
    refine_factor: int = 10
    nprobes: int = 20
    select_columns: list[str] | None = None


@dataclass(frozen=True, slots=True)
class VectorIndexBuildRequest:
    build_vector_index: bool = True
    vector_index_type: str = "IVF_HNSW_SQ"
    vector_metric: str = "cosine"
    vector_num_partitions: int | None = None
    vector_num_sub_vectors: int | None = None
    vector_m: int = 20
    vector_ef_construction: int = 300
    build_scalar_indices: bool = True
    scalar_columns: list[tuple[str, str]] | None = None
    replace: bool = True
    strict: bool = False


def _coerce_vector_search_request(
    *,
    request: VectorSearchRequest | None = None,
    legacy_kwargs: dict[str, Any] | None = None,
) -> VectorSearchRequest:
    if request is not None:
        return request
    values = dict(legacy_kwargs or {})
    return VectorSearchRequest(
        query_vector=[float(value) for value in values["query_vector"]],
        where=str(values["where"]),
        limit=int(values["limit"]),
        metric=str(values.get("metric") or "cosine"),
        refine_factor=int(values.get("refine_factor") or 10),
        nprobes=int(values.get("nprobes") or 20),
        select_columns=(
            list(values["select_columns"])
            if values.get("select_columns") is not None
            else None
        ),
    )


def _coerce_vector_index_build_request(
    *,
    request: VectorIndexBuildRequest | None = None,
    legacy_kwargs: dict[str, Any] | None = None,
) -> VectorIndexBuildRequest:
    if request is not None:
        return request
    values = dict(legacy_kwargs or {})
    return VectorIndexBuildRequest(
        build_vector_index=bool(values.get("build_vector_index", True)),
        vector_index_type=str(values.get("vector_index_type") or "IVF_HNSW_SQ"),
        vector_metric=str(values.get("vector_metric") or "cosine"),
        vector_num_partitions=values.get("vector_num_partitions"),
        vector_num_sub_vectors=values.get("vector_num_sub_vectors"),
        vector_m=int(values.get("vector_m") or 20),
        vector_ef_construction=int(values.get("vector_ef_construction") or 300),
        build_scalar_indices=bool(values.get("build_scalar_indices", True)),
        scalar_columns=(
            list(values["scalar_columns"])
            if values.get("scalar_columns") is not None
            else None
        ),
        replace=bool(values.get("replace", True)),
        strict=bool(values.get("strict", False)),
    )


def _default_scalar_index_plan() -> list[tuple[str, str]]:
    return [
        ("chunk_id", "BTREE"),
        ("doc_id", "BTREE"),
        ("event_start_ts", "BTREE"),
        ("event_end_ts", "BTREE"),
        ("doc_type", "BITMAP"),
        ("kind", "BITMAP"),
    ]


def _vector_index_error(*, exc: Exception) -> dict[str, str]:
    return {
        "kind": "vector",
        "error_type": type(exc).__name__,
        "error_message": str(exc),
    }


def _scalar_index_error(
    *,
    column: str,
    index_type: str,
    exc: Exception,
) -> dict[str, str]:
    return {
        "kind": "scalar",
        "column": str(column),
        "index_type": str(index_type),
        "error_type": type(exc).__name__,
        "error_message": str(exc),
    }


def _record_index_build_error(
    *,
    error: dict[str, str],
    exc: Exception,
    errors: list[dict[str, str]],
    log: Any,
    strict: bool,
) -> None:
    errors.append(error)
    if error["kind"] == "vector":
        log.warning(
            "Vector index build failed error_type={} error={}",
            error["error_type"],
            error["error_message"],
        )
    else:
        log.warning(
            "Scalar index build failed column={} index_type={} error_type={} error={}",
            error["column"],
            error["index_type"],
            error["error_type"],
            error["error_message"],
        )
    if strict:
        raise exc


def _vector_index_stats(
    *,
    table: Any,
    request: VectorIndexBuildRequest,
    log: Any,
    errors: list[dict[str, str]],
) -> dict[str, Any] | None:
    if not request.build_vector_index:
        return None
    try:
        table.create_index(  # type: ignore[no-untyped-call]
            metric=str(request.vector_metric),
            index_type=str(request.vector_index_type),
            num_partitions=request.vector_num_partitions,
            num_sub_vectors=request.vector_num_sub_vectors,
            m=int(request.vector_m),
            ef_construction=int(request.vector_ef_construction),
            replace=bool(request.replace),
        )
        return {
            "built": True,
            "metric": str(request.vector_metric),
            "index_type": str(request.vector_index_type),
        }
    except Exception as exc:  # noqa: BLE001
        error = _vector_index_error(exc=exc)
        _record_index_build_error(
            error=error,
            exc=exc,
            errors=errors,
            log=log,
            strict=request.strict,
        )
        return {
            "built": False,
            "metric": str(request.vector_metric),
            "index_type": str(request.vector_index_type),
        }


def _scalar_index_stats(
    *,
    table: Any,
    request: VectorIndexBuildRequest,
    scalar_plan: list[tuple[str, str]],
    log: Any,
    errors: list[dict[str, str]],
) -> dict[str, Any] | None:
    if not request.build_scalar_indices:
        return None
    built = 0
    attempted = 0
    for column, index_type in scalar_plan:
        attempted += 1
        try:
            table.create_scalar_index(  # type: ignore[no-untyped-call]
                str(column),
                replace=bool(request.replace),
                index_type=str(index_type),
            )
            built += 1
        except Exception as exc:  # noqa: BLE001
            error = _scalar_index_error(
                column=str(column),
                index_type=str(index_type),
                exc=exc,
            )
            _record_index_build_error(
                error=error,
                exc=exc,
                errors=errors,
                log=log,
                strict=request.strict,
            )
    return {
        "built_total": built,
        "attempted_total": attempted,
        "columns": [{"column": column, "index_type": index_type} for column, index_type in scalar_plan],
    }


def _table_indices_total(table: Any) -> int:
    try:
        return len(list(table.list_indices()))  # type: ignore[no-untyped-call]
    except Exception:
        return 0


class LanceVectorStore:
    def __init__(
        self,
        *,
        db_dir: Path,
        table_name: str = "chunk_vectors",
    ) -> None:
        self.db_dir = Path(db_dir).expanduser().resolve()
        self.db_dir.mkdir(parents=True, exist_ok=True)
        self.table_name = str(table_name or "").strip() or "chunk_vectors"
        self._db: Any | None = None
        self._table: Any | None = None

    def _connect(self) -> Any:
        if self._db is None:
            import lancedb

            self._db = lancedb.connect(str(self.db_dir))
        return self._db

    def _open_table(self) -> Any:
        if self._table is not None:
            return self._table

        db = self._connect()
        try:
            self._table = db.open_table(self.table_name)
            return self._table
        except Exception:
            # Create on first write.
            self._table = None
            raise

    def try_open_table(self) -> Any | None:
        try:
            return self._open_table()
        except Exception:
            return None

    def ensure_table(self, *, bootstrap_row: VectorRow | None = None) -> None:
        try:
            _ = self._open_table()
            return
        except Exception:
            pass

        if bootstrap_row is None:
            # We intentionally create the table only when we have real data.
            return

        db = self._connect()
        row = self._row_to_dict(bootstrap_row)
        try:
            self._table = db.create_table(self.table_name, [row])
        except Exception:
            # In case of races, try open again.
            self._table = db.open_table(self.table_name)

    @staticmethod
    def _row_to_dict(row: VectorRow) -> dict[str, Any]:
        return {
            "chunk_id": int(row.chunk_id),
            "doc_id": int(row.doc_id),
            "doc_type": str(row.doc_type),
            "chunk_index": int(row.chunk_index),
            "kind": str(row.kind),
            "text_hash": str(row.text_hash),
            "text_preview": str(row.text_preview),
            "event_start_ts": float(row.event_start_ts),
            "event_end_ts": float(row.event_end_ts),
            "vector": [float(v) for v in row.vector],
        }

    def upsert_rows(self, *, rows: list[VectorRow]) -> int:
        if not rows:
            return 0

        self.ensure_table(bootstrap_row=rows[0])
        try:
            table = self._open_table()
        except Exception as exc:  # noqa: BLE001
            log = logger.bind(module="rag.vector_store")
            log.warning(
                "Failed to open LanceDB table error_type={} error={}",
                type(exc).__name__,
                str(exc),
            )
            raise

        payload = [self._row_to_dict(row) for row in rows]
        table.merge_insert(
            "chunk_id"
        ).when_matched_update_all().when_not_matched_insert_all().execute(  # type: ignore[no-untyped-call]
            payload
        )
        return len(payload)

    def fetch_existing_hashes(self, *, chunk_ids: list[int]) -> dict[int, str]:
        """Best-effort batch read of existing (chunk_id -> text_hash)."""
        normalized: list[int] = []
        seen: set[int] = set()
        for raw in chunk_ids:
            try:
                cid = int(raw)
            except Exception:
                continue
            if cid <= 0 or cid in seen:
                continue
            seen.add(cid)
            normalized.append(cid)
        if not normalized:
            return {}

        table = self.try_open_table()
        if table is None:
            return {}

        # Batch WHERE with IN, keep chunks reasonably sized.
        out: dict[int, str] = {}
        batch_size = 400
        for i in range(0, len(normalized), batch_size):
            batch = normalized[i : i + batch_size]
            ids = ", ".join(str(cid) for cid in batch)
            where = f"chunk_id IN ({ids})"
            rows = (
                table.search()
                .where(where)  # type: ignore[no-untyped-call]
                .select(["chunk_id", "text_hash"])
                .limit(len(batch))
                .to_list()
            )
            for row in rows:
                try:
                    out[int(row.get("chunk_id") or 0)] = str(row.get("text_hash") or "")
                except Exception:
                    continue
        return out

    def search(
        self,
        request: VectorSearchRequest | None = None,
        **legacy_kwargs: Any,
    ) -> list[dict[str, Any]]:
        resolved_request = _coerce_vector_search_request(
            request=request,
            legacy_kwargs=legacy_kwargs,
        )
        normalized_limit = max(1, min(int(resolved_request.limit), 50))
        try:
            table = self._open_table()
        except Exception:
            return []

        query = (
            table.search([float(v) for v in resolved_request.query_vector])
            .metric(resolved_request.metric)
            .where(resolved_request.where)
        )  # type: ignore[no-untyped-call]
        query = (
            query.refine_factor(int(resolved_request.refine_factor))
            .nprobes(int(resolved_request.nprobes))
            .limit(normalized_limit)
        )  # type: ignore[no-untyped-call]
        if resolved_request.select_columns:
            query = query.select(resolved_request.select_columns)  # type: ignore[no-untyped-call]
        rows = query.to_list()  # type: ignore[no-untyped-call]
        return [dict(row) for row in rows]

    def build_indices(
        self,
        request: VectorIndexBuildRequest | None = None,
        **legacy_kwargs: Any,
    ) -> dict[str, Any]:
        """Build vector/scalar indices for the current table.

        This is a best-effort operation by default; set strict=True to raise on errors.
        """

        resolved_request = _coerce_vector_index_build_request(
            request=request,
            legacy_kwargs=legacy_kwargs,
        )
        log = logger.bind(module="rag.vector_store", table=self.table_name)
        table = self.try_open_table()
        if table is None:
            return {
                "table_exists": False,
                "vector_index": None,
                "scalar_indices": None,
                "errors": [],
            }

        errors: list[dict[str, str]] = []
        scalar_plan = resolved_request.scalar_columns or _default_scalar_index_plan()
        vector_stats = _vector_index_stats(
            table=table,
            request=resolved_request,
            log=log,
            errors=errors,
        )
        scalar_stats = _scalar_index_stats(
            table=table,
            request=resolved_request,
            scalar_plan=scalar_plan,
            log=log,
            errors=errors,
        )
        indices_total = _table_indices_total(table)

        out = {
            "table_exists": True,
            "vector_index": vector_stats,
            "scalar_indices": scalar_stats,
            "indices_total": indices_total,
            "errors": errors,
        }
        log.info(
            "Index build done vector_built={} scalar_built={} errors={} indices_total={}",
            bool(vector_stats and vector_stats.get("built")),
            int((scalar_stats or {}).get("built_total") or 0),
            len(errors),
            indices_total,
        )
        return out


def _vector_dims_from_schema(table: Any) -> int:
    try:
        schema = getattr(table, "schema", None)
        if schema is None:
            return 0
        field = schema.field("vector")
        dtype = field.type
        size = getattr(dtype, "list_size", None)
        if isinstance(size, int) and size > 0:
            return size
    except Exception:
        return 0
    return 0


def embedding_table_name(
    *, embedding_model: str, embedding_dimensions: int | None
) -> str:
    """Generate a stable LanceDB table name for a specific embedding configuration."""

    model = str(embedding_model or "").strip() or "unknown"
    dims = "auto" if embedding_dimensions is None else str(int(embedding_dimensions))
    fingerprint = hashlib.sha256(f"{model}|{dims}".encode("utf-8")).hexdigest()[:16]
    return f"chunk_vectors_{fingerprint}"
