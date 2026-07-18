from __future__ import annotations
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.models.zone import Zone



@dataclass
class Drone:
    id: int
    current_zone: Zone
    path: list[Zone] = field(default_factory=list)
    path_index: int = 0
