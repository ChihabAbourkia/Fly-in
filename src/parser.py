from src.models.graph import Graph
from .costum_errors import ParseError
from src.models.zone import Zone
from src.models.enums import ZoneType
from src.models.connection import Connection

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
                elif line.startswith("connection:"):
                    self._parse_connection(line, line_number, graph)
                else:
                    raise ParseError(
                        f"Line {line_number}: unknown statement."
                        )
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

    def _parse_metadata(self, zone: Zone, metadata: str, line_number: int, is_end: bool = False, is_start: bool = False, ) -> None:
        splited_data = metadata.split()
        for i in splited_data:
           if "=" not in i:
               raise ParseError(
                   f"Line {line_number}: expected key=value in metadata."
                   )

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
               if is_start or is_end:
                   continue
               else:
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
            raise ParseError(f"Line {line_number}: expected 'name x y'.")
        name = parts[0]
        if "-" in name:
            raise ParseError(
                f"Line {line_number}: zone names cannot contain '-'."
                )
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
            self._parse_metadata(zone, metadata, line_number, is_end , is_start)
        graph.add_zone(zone)

    def _parse_capacity_link(self , line_number : int, connection: Connection, max_capacity: str):
        try:
                value =  int(max_capacity)
                # print(value)
        except ValueError:
                raise ParseError(f"Line {line_number} : invalid capacity link value.")
        if value <= 0:
                raise ParseError(f"Line {line_number} : Negative capacity number.")

        connection.max_link_capacity = value

    def _exist_connecion(self, graph: Graph, zone1_obj: Zone, zone2_obj: Zone)->bool:
        for connection in graph.connections:
            if ((zone1_obj == connection.zone1 and zone2_obj == connection.zone2)
                or (zone1_obj == connection.zone2 and zone2_obj == connection.zone1 )):
                return True
        return False

    def _parse_connection(self ,line : str, line_number : int, graph: Graph):
        connrction_info = line.removeprefix("connection:").strip()
        max_link_capacity = None
        if "[" in connrction_info:
            zones, capacity = connrction_info.split("[")
            capacity = capacity.rstrip("]")
            if "="  not in capacity:
                raise ParseError(f"Line {line_number} expected key=value.")
            key, max_link_capacity = capacity.split("=",1)
            key = key.strip()
            max_link_capacity = max_link_capacity.strip()
            if key  != "max_link_capacity":
                raise ParseError(f"Line {line_number}: invalid key {key}.")
        else:
            zones = connrction_info
        parts = zones.split("-")
        if len(parts) != 2:
            raise ParseError(
                f"Line {line_number}: invalid connection format."
                )
        zone1 = parts[0].strip()
        zone2 = parts[1].strip()
        zone1_obj = graph.get_zone(zone1)
        zone2_obj = graph.get_zone(zone2)
        if zone1_obj is None or zone2_obj is None:
            raise ParseError(
                f"Line {line_number}: connection references an unknown zone."
                )
        if self._exist_connecion(graph, zone1_obj, zone2_obj):
            raise ParseError( f"Line {line_number}: duplicate connection."
                             )
        connection = Connection(zone1= zone1_obj, zone2= zone2_obj)
        if max_link_capacity is not None:
            self._parse_capacity_link( line_number, connection, max_link_capacity)

        graph.add_connection(connection)








parser = Parser()
graph = parser.parse("maps/medium/02_circular_loop.txt")

for zone in graph.zones.values():
    for connection in zone.connections:
        print(connection.max_link_capacity)
# for zone in graph.zones.values():
#     print(f"\n{zone.name}:")
#     for connection in zone.connections:
#         if connection.zone1 == zone:
#             nighbor =  connection.zone2
#         else:
#             nighbor = connection.zone1

#         print(f"--> {nighbor.name}")
