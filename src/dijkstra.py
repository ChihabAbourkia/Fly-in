import heapq

from src.models.enums import ZoneType
from src.models.graph import Graph
from src.models.zone import Zone


class Dijkstra:

    def _get_neghbors(self, zone: Zone) -> list[Zone]:
        neghbors = []

        for connection in zone.connections:
            if connection.zone1 == zone:
                neghbors.append(connection.zone2)
            else:
                neghbors.append(connection.zone1)

        return neghbors

    def _zone_turn(self, zone: Zone) -> int:
        if zone.zone_type == ZoneType.NORMAL:
            return 1
        elif zone.zone_type == ZoneType.PRIORITY:
            return 1
        elif zone.zone_type == ZoneType.RESTRICTED:
            return 2
        elif zone.zone_type == ZoneType.BLOCKED:
            return -1

        return -1

    def path_finding(
        self,
        graph: Graph,
        start: Zone,
        end: Zone,
    ) -> list[Zone]:

        distance: dict[str, float] = {
            zone.name: float("inf")
            for zone in graph.zones.values()
        }

        previous: dict[str, Zone | None] = {
            zone.name: None
            for zone in graph.zones.values()
        }

        visited: set[str] = set()

        distance[start.name] = 0

        heap: list[tuple[float, str, Zone]] = [
            (0, start.name, start)
        ]

        while heap:

            current_distance, _, current = heapq.heappop(heap)

            if current.name in visited:
                continue

            if current == end:
                break

            visited.add(current.name)

            for neghbor in self._get_neghbors(current):

                if neghbor.name in visited:
                    continue

                zone_turn = self._zone_turn(neghbor)

                if zone_turn == -1:
                    continue

                new_distance = current_distance + zone_turn

                if new_distance < distance[neghbor.name]:
                    distance[neghbor.name] = new_distance
                    previous[neghbor.name] = current

                    heapq.heappush(
                        heap,
                        (new_distance, neghbor.name, neghbor),
                    )

        if distance[end.name] == float("inf"):
            return []

        path: list[Zone] = []
        current: Zone | None = end

        while current is not None:
            path.append(current)
            current = previous[current.name]

        path.reverse()

        return path
