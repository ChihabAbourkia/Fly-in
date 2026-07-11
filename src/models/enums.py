from enum import Enum

class ZoneType(Enum):
    """Available zone types."""
    NORMAL = "normal"
    PRIORITY = "priority"
    RESTRICTED = "restricted"
    BLOCKED = "blocked"

