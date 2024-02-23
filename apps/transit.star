load("render.star", "render")

def main():
    children = [
        render.Text(content="Transit", color="#999"),
        render.Text(content="App", color="#999"),
        render.Text(content="WIP", color="#999")
    ]

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
