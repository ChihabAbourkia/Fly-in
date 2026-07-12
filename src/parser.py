from src.models.graph import Graph
from .costum_errors import ParseError
from src.models.zone import Zone
from src.models.enums import ZoneType

class Parser:
    def parse(self, filename: str) -> Graph:
        graph = Graph()
        with open(filename, "r", encoding="utf-8")as file:

            for line_number, line in enumerate(file, start=1):
                line = line.strip()
                if not line:
                    continue
                if line.startswith("#"):
                    continue
                if line.startswith("nb_drones:"):
                    self._parse_nb_drones(line, line_number, graph)
                elif line.startswith("start_hub:"):
                    self._parse_zone(line, line_number, graph, is_start=True)
                elif line.startswith("end_hub:"):
                    self._parse_zone(line, line_number, graph, is_end=True)
                elif line.startswith("hub:"):
                    self._parse_zone(line, line_number, graph)
                # elif line.startswith("connection:"):
                #     self._parse_connection(line, line_number, graph)
                # else:
                #     raise ParseError(...)

        return graph

    def _parse_nb_drones(self, line: str, line_number: int, graph: Graph, ) -> None:

        value = line.removeprefix("nb_drones:").strip()
        try:
            nb = int(value)
        except ValueError :
            raise ParseError(f"Line {line_number}: invalid number of drones")
        if nb <= 0:
            raise ParseError(
                f"Line {line_number}: number of drones must be positive."
                )
        graph.nb_drones = nb

    def _parse_metadata(self, zone: Zone, metadata: str, line_number: int, ) -> None:
        splited_data = metadata.split()
        for i in splited_data:
           key, value  = i.split("=", 1)
           if key == "color":
               zone.color = value
           elif key == "zone":
               try:
                   zone.zone_type = ZoneType(value)
               except ValueError:
                   raise ParseError(
                       f"Line {line_number}: invalid zone type '{value}'."
                       )
           elif key == "max_drones":
               try:
                   max_drones = int(value)
               except ValueError:
                   raise ParseError(f"Line {line_number} : invalid drones number {value}. ")
               if max_drones <= 0:
                  raise ParseError(
                      f"Line {line_number}: max_drones must be a positive integer."
                      )
               zone.max_drones = max_drones
           else:
               raise ParseError(
                   f"Line {line_number}: unknown metadata '{key}'."
    )

    def _parse_zone(self,line: str,line_number: int,graph: Graph,is_start: bool = False,is_end: bool = False,) -> None:
        prefix = ""
        if is_start :
            prefix = "start_hub:"
        elif is_end :
            prefix = "end_hub:"
        else:
            prefix = "hub:"

        zone_infos = line.removeprefix(prefix).strip()
        metadata = None
        if "[" in zone_infos:
            before, metadata = zone_infos.split("[", 1)
            before = before.strip()
            metadata = metadata.rstrip("]")
        else:
            before = zone_infos
        parts = before.split()
        if len(parts) != 3:
            raise ParseError(f"Line: {line_number} : not enough infos!!! ")
        name = parts[0]
        if graph.get_zone(name) is not None:
             raise ParseError(
                 f"Line {line_number}: duplicate zone '{name}'."
                 )
        try:
            x = int(parts[1])
            y = int(parts[2])
        except ValueError:
            raise ParseError(f"Line {line_number} : invalid zone coordinates")
        zone = Zone(name= name, x = x,y = y)
        if is_start:
            graph.start = zone
        elif is_end:
            graph.end = zone
        if metadata is not None:
            self._parse_metadata(zone, metadata, line_number)
        graph.add_zone(zone)



parser = Parser()
graph = parser.parse("maps/medium/01_dead_end_trap.txt")
print(graph)
