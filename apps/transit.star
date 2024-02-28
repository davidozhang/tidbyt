load("render.star", "render")
load("http.star", "http")

DEFAULT_STOP_ID = "1_38962"

def main():
    children = []
    resp = http.get("https://davidozhang.pythonanywhere.com/transit?stop_id=" + str(DEFAULT_STOP_ID))
    json = resp.json()
    arrival_times = json["arrival_times"]
    stop_name = json["stop_name"]

    if not arrival_times:
        primary_text = "No"
        secondary_text = "Buses"
        tertiary_text = "Found"
    else:
        primary_text = stop_name
        tertiary_text = ""

        secondary_text = arrival_times[0]["route"]
        arrival_time = arrival_times[0]["arrival_time"]
        if arrival_time == 0:
            secondary_text += ": NOW"
        else:
            secondary_text += ": " + str(arrival_times[0]["arrival_time"]) + " min"

        if not arrival_times[0]["predicted"]:
            secondary_text += "˙"

        if len(arrival_times) > 1:
            tertiary_text = arrival_times[1]["route"]
            arrival_time = arrival_times[1]["arrival_time"]
            if arrival_time == 0:
                tertiary_text += ": NOW"
            else:
                tertiary_text += ": " + str(arrival_times[1]["arrival_time"]) + " min"

            if not arrival_times[1]["predicted"]:
                tertiary_text += "˙"

    if primary_text:
        children.append(
            render.Marquee(
                child=render.Text(content=primary_text, color="#999"),
                width=64,
                align="center"
            )
        )
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
