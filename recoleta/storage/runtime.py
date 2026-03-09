from __future__ import annotations

from recoleta.storage.leases import WorkspaceLeaseStoreMixin
from recoleta.storage.runs import RunStoreMixin


class RuntimeStoreMixin(RunStoreMixin, WorkspaceLeaseStoreMixin):
    pass
