from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional,TYPE_CHECKING
from .enums import ZoneType
if TYPE_CHECKING:
    from .connection import Connection


@dataclass
class Zone:
    """Represents a zone (hub) in the drone network."""
    name: str
    x: int
    y: int
    color: Optional[str] = None
    zone_type: ZoneType = ZoneType.NORMAL
    max_drones: int = 1
    connections: list[Connection]=field(default_factory=list)
    occupancy: int = 0
