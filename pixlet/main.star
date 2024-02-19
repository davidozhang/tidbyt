load("render.star", "render")
load("http.star", "http")

DEFAULT_LAT = 47.712380
DEFAULT_LNG = -122.316400
DEFAULT_RADIUS = 5000

# Fallback to SEATAC
FALLBACK_LAT = 47.4484
FALLBACK_LNG = -122.3086
FALLBACK_RADIUS = 5000

def main():
    children = []
    overhead = True
    resp = http.get("https://davidozhang.pythonanywhere.com/flights?lat=" + str(DEFAULT_LAT) + "&lng=" + str(DEFAULT_LNG) + "&radius=" + str(DEFAULT_RADIUS))
    flights = resp.json()["flights"]

    if not flights:
        overhead = False
        resp = http.get("https://davidozhang.pythonanywhere.com/flights?lat=" + str(FALLBACK_LAT) + "&lng=" + str(FALLBACK_LNG) + "&radius=" + str(FALLBACK_RADIUS))
        flights = resp.json()["flights"]

    if flights:
        flight = flights[0]
        primary_text = ""
        if overhead:
            primary_text = "↑ "
        primary_text += flight["callsign"]
        secondary_text = flight["origin_airport_iata"] + " → " + flight["destination_airport_iata"]
        tertiary_text = flight["aircraft_code"]
    else:
        primary_text = "No"
        secondary_text = "Flights"
        tertiary_text = "Found"

    if primary_text:
        children.append(render.Text(content=primary_text, color="#999"))
    if secondary_text:
        children.append(render.Text(content=secondary_text, color="#999"))
    if tertiary_text:
        children.append(render.Text(content=tertiary_text, color="#999"))

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
