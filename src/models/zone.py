from dataclasses import dataclass, field
from typing import Optional
from .enums import ZoneType
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
    # connections: list[Connection]=field(default_factory=list)
    # occupancy: int = 0