"""Hand-authored neofetch-style info card SVG with staggered fade-in lines."""

OUT = "assets/info-card.svg"

WIDTH = 480
LINE_H = 26
PAD_TOP = 30
GREEN = "#39d353"
DIM = "#8b949e"
WHITE = "#e6edf3"
BG = "#0d1117"

LINES = [
    ("hardik@github", "header"),
    ("-" * 30, "dim"),
    ("OS", "MERN Stack Enthusiast"),
    ("Role", "Full Stack Developer (Learning)"),
    ("Stack", "React, Node.js, Express, MongoDB"),
    ("Tools", "Git, VS Code, Vercel, Railway"),
    ("Status", "Open to collaborating on Full Stack projects"),
    ("Contact", "hardiksrivastava.dev@gmail.com"),
]

HEIGHT = PAD_TOP + LINE_H * len(LINES) + 20


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;")


def build():
    parts = []
    parts.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" '
        f'viewBox="0 0 {WIDTH} {HEIGHT}">'
    )
    parts.append(f'<rect width="100%" height="100%" rx="10" fill="{BG}" stroke="#30363d"/>')
    parts.append(
        '<style>text{font-family:"Courier New",monospace;font-size:15px;}'
        f'.k{{fill:{GREEN};font-weight:bold;}} .v{{fill:{WHITE};}} '
        f'.h{{fill:{GREEN};font-weight:bold;font-size:17px;}} .d{{fill:{DIM};}}</style>'
    )

    y = PAD_TOP
    for i, (key, val) in enumerate(LINES):
        delay = i * 0.12
        if val == "header":
            content = f'<tspan class="h">{esc(key)}</tspan>'
        elif val == "dim":
            content = f'<tspan class="d">{esc(key)}</tspan>'
        else:
            content = f'<tspan class="k">{esc(key)}:</tspan> <tspan class="v">{esc(val)}</tspan>'
        parts.append(
            f'<text x="20" y="{y}" opacity="0">'
            f'<animate attributeName="opacity" from="0" to="1" '
            f'begin="{delay:.2f}s" dur="0.5s" fill="freeze"/>'
            f"{content}</text>"
        )
        y += LINE_H

    parts.append("</svg>")
    return "\n".join(parts)


if __name__ == "__main__":
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(build())
    print(f"wrote {OUT}")
