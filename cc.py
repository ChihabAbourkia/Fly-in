# from  src.models.graph import Graph
# from src.costum_errors import ParseError

# class Parser:
def parse( filename: str):
    # graph = Graph()
    with open(filename, "r", encoding="utf-8")as file:

        for line_number, line in enumerate(file, start=1):
            line = line.strip()
            if not line:
                continue
            if line.startswith("#"):
                continue
            if line.startswith("nb_drones:"):
               _parse_nb_drones(line, line_number)
            # elif line.startswith("start_hub:"):
            #     self._parse_zone(line, line_number, graph, is_start=True)
            # elif line.startswith("end_hub:"):
            #     self._parse_zone(line, line_number, graph, is_end=True)
            # elif line.startswith("hub:"):
            #     self._parse_zone(line, line_number, graph)
            # elif line.startswith("connection:"):
            #     self._parse_connection(line, line_number, graph)
            # else:
            #     raise ParseError(...)

    # return graph

def _parse_nb_drones(line, line_number )-> None:
    value = line.removeprefix("nb_drones:").strip()
    try:
        nb = int(value)
    except ValueError :
        raise ValueError(f"Line {line_number}: invalid number of drones")
    if nb <= 0:
        raise ValueError("Error: negative value!!")
    print(nb)

parse("maps/easy/01_linear_path.txt")

    # graph.nb_drones = nb
