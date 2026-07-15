from dataclasses import dataclass, field
from .connection import Connection
from typing import Optional
from .zone import Zone

@dataclass
class Graph:
    """Represents the complete drone network."""
    nb_drones: int = 0

    zones: dict[str, Zone] = field(default_factory=dict)
    connections: list[Connection]= field(default_factory=list)
    start: Optional[Zone] = None
    end: Optional[Zone] = None

    def add_zone(self, zone: Zone) -> None:
        """Add a zone to the graph."""
        self.zones[zone.name] = zone

    def add_connection(self, connection: Connection)-> None:
        """Add a connection to the graph."""
        self.connections.append(connection)
        connection.zone1.connections.append(connection)
        connection.zone2.connections.append(connection)

    def get_zone(self, name: str) -> Optional[Zone]:
        """Return a zone by its name."""
        return self.zones.get(name)
