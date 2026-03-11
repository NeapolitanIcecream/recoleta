from __future__ import annotations

from recoleta.storage.leases import WorkspaceLeaseStoreMixin
from recoleta.storage.runs import RunStoreMixin
from recoleta.storage.source_states import SourcePullStateStoreMixin


class RuntimeStoreMixin(
    RunStoreMixin,
    WorkspaceLeaseStoreMixin,
    SourcePullStateStoreMixin,
):
    pass
