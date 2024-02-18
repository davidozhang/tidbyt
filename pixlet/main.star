load("render.star", "render")
load("http.star", "http")

API_URL = "https://davidozhang.pythonanywhere.com/flights-overhead"

def main():
    rep = http.get(API_URL)

    flights = rep.json()["flights"]
    children = []

    if flights:
        flight = flights[0]
        primary_text = "↑ " + flight["callsign"]
        secondary_text = flight["origin_airport_iata"] + " → " + flight["destination_airport_iata"]
        tertiary_text = flight["aircraft_code"]
    else:
        primary_text = "No"
        secondary_text = "Flight"
        tertiary_text = "Overhead"

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
