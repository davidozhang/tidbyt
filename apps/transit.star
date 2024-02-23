load("render.star", "render")
load("encoding/base64.star", "base64")

def main():
    children = [
        render.Text(content="Transit App", color="#999"),
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
