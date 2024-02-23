load("render.star", "render")
load("http.star", "http")

DEFAULT_LAT = 47.712380
DEFAULT_LNG = -122.316400
DEFAULT_RADIUS = 5000

FALLBACK_LAT = 47.4436
FALLBACK_LNG = -122.2961
FALLBACK_RADIUS = 10000

DIRECTION_TO_SYMBOL_MAPPING = {
    "N": "↑",
    "E": "→",
    "W": "←",
    "S": "↓",
    "NE": "↗",
    "NW": "↖",
    "SE": "↘",
    "SW": "↙"
}

def main():
    children = []
    nearby = True
    resp = http.get("https://davidozhang.pythonanywhere.com/flights?lat=" + str(DEFAULT_LAT) + "&lng=" + str(DEFAULT_LNG) + "&radius=" + str(DEFAULT_RADIUS))
    flights = resp.json()["flights"]

    if not flights:
        nearby = False
        resp = http.get("https://davidozhang.pythonanywhere.com/flights?lat=" + str(FALLBACK_LAT) + "&lng=" + str(FALLBACK_LNG) + "&radius=" + str(FALLBACK_RADIUS) + "&lat4dir=" + str(DEFAULT_LAT) + "&lng4dir="+str(DEFAULT_LNG))
        flights = resp.json()["flights"]

    if flights:
        flight = flights[0]

        direction_symbol = DIRECTION_TO_SYMBOL_MAPPING[flight['direction']]
        primary_text = direction_symbol

        # Add extra direction symbol to indicate flight is nearby
        if nearby:
            primary_text += direction_symbol

        primary_text += " " + flight["callsign"]
        secondary_text = flight["origin_airport_iata"] + " → " + flight["destination_airport_iata"]
        if not flight["on_ground"]:
            tertiary_text = flight["aircraft_code"] + " " + flight["altitude"] + " " + flight["ground_speed"]
        else:
            tertiary_text = flight["aircraft_code"] + " ON GROUND"
    else:
        primary_text = "No"
        secondary_text = "Flights"
        tertiary_text = "Found"

    if primary_text:
        children.append(render.Text(content=primary_text, color="#999"))
    if secondary_text:
        children.append(render.Text(content=secondary_text, color="#999"))
    if tertiary_text:
        children.append(
            render.Marquee(
                child=render.Text(content=tertiary_text, color="#999"),
                width=64,
                offset_start=32,
                offset_end=-48,
                align="center"
            )
        )

    return render.Root(
        child=render.Box(  # This Box exists to provide vertical centering
            render.Column(
                expanded=True,
                main_align="center",  # Controls horizontal alignment
                cross_align="center",  # Controls vertical alignment
                children=children,
            ),
        ),
    )
