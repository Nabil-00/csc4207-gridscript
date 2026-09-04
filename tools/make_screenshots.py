#!/usr/bin/env python3
"""
Generates terminal-style screenshots of GridScript test runs and demos
for the project report and video walkthroughs.

Run:  python3 make_screenshots.py
Out:  report/screenshots/*.png
"""
import os
import re
import subprocess
import sys

from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(ROOT, 'report', 'screenshots')
FONT_PATH = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'
FONT_BOLD = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf'

FONT_SIZE = 16
LINE_H = 22
PAD_X = 16
PAD_Y = 14
BAR_H = 36
MAX_COLS = 100

BG = (30, 30, 40)
BAR_BG = (52, 54, 66)
FG = (204, 208, 220)
GREEN = (98, 200, 120)
RED = (235, 90, 90)
CYAN = (90, 190, 220)
YELLOW = (220, 190, 90)
DIM = (120, 124, 140)

ANSI_COLORS = {
    '92': GREEN, '91': RED, '96': CYAN, '93': YELLOW,
    '1': None, '0': None,
}


def strip_or_apply(line):
    """Convert a raw ANSI line into list of (text, color, bold) segments."""
    segments = []
    color = FG
    bold = False
    pos = 0
    pattern = re.compile(r'\x1b\[(\d+(?:;\d+)*)m')
    for m in pattern.finditer(line):
        text = line[pos:m.start()]
        if text:
            segments.append((text, color, bold))
        for code in m.group(1).split(';'):
            if code == '0':
                color, bold = FG, False
            elif code == '1':
                bold = True
            elif code in ANSI_COLORS and ANSI_COLORS[code]:
                color = ANSI_COLORS[code]
        pos = m.end()
    text = line[pos:]
    if text:
        segments.append((text, color, bold))
    return segments


def wrap_line(line, cols):
    if len(line) <= cols:
        return [line]
    out = []
    while len(line) > cols:
        out.append(line[:cols])
        line = line[cols:]
    out.append(line)
    return out


def render_terminal(title, raw_text, out_path):
    lines = []
    for raw in raw_text.split('\n'):
        clean = raw.replace('\x1b[?25l', '').replace('\x1b[?25h', '')
        clean = re.sub(r'\x1b\[[0-9;]*[A-HJKSTfhlmsu]', lambda m: m.group(0) if m.group(0).endswith('m') else '', clean)
        clean = clean.replace('\x1b[0K', '')
        for seg in clean.split('\r'):
            for wl in wrap_line(seg, MAX_COLS):
                lines.append(wl)

    font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
    font_title = ImageFont.truetype(FONT_BOLD, 13)
    char_w = font.getbbox('M')[2] - font.getbbox('M')[0]
    width = max(640, char_w * MAX_COLS + PAD_X * 2)
    height = BAR_H + PAD_Y + len(lines) * LINE_H + PAD_Y

    img = Image.new('RGB', (width, height), BG)
    draw = ImageDraw.Draw(img)

    draw.rectangle([0, 0, width, BAR_H], fill=BAR_BG)
    for i, c in enumerate([(255, 95, 86), (255, 189, 46), (39, 201, 63)]):
        cx = PAD_X + i * 22
        cy = BAR_H // 2
        draw.ellipse([cx, cy - 7, cx + 14, cy + 7], fill=c)
    tw = draw.textlength(title, font=font_title)
    draw.text(((width - tw) // 2, (BAR_H - 16) // 2), title, font=font_title, fill=(170, 174, 190))

    y = BAR_H + PAD_Y
    for line in lines:
        x = PAD_X
        for text, color, bold in strip_or_apply(line):
            f = ImageFont.truetype(FONT_BOLD if bold else FONT_PATH, FONT_SIZE)
            draw.text((x, y), text, font=f, fill=color)
            x += draw.textlength(text, font=f)
        y += LINE_H

    img.save(out_path)
    print(f"  saved {os.path.relpath(out_path, ROOT)}")


def run_cmd(cmd, cwd=ROOT):
    proc = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True, timeout=60)
    out = proc.stdout + proc.stderr
    out = out.replace(f'[{proc.returncode}]', '')
    return out.rstrip('\n')


DEMOS = [
    ("run_tests: full suite", "python3 run_tests.py"),
    ("unit tests: lexer", None),
    ("unit tests: parser", None),
    ("unit tests: interpreter", None),
    ("patrol.gsc: while + if + built-ins", "python3 gridscript.py tests/valid/patrol.gsc"),
    ("shadowing.gsc: static scoping demo", "python3 gridscript.py tests/valid/shadowing.gsc"),
    ("recursion.gsc: factorial", "python3 gridscript.py tests/valid/recursion.gsc"),
    ("lexer output: --tokens", "python3 gridscript.py --tokens tests/valid/patrol.gsc | head -24"),
    ("parser output: --ast", "python3 gridscript.py --ast tests/valid/scale.gsc | head -40"),
    ("syntax errors caught", None),
    ("runtime errors caught", None),
]


def build_unit_suite_shells():
    """Split the unit test file into lexer / parser / interpreter runs."""
    import test_interpreter  # noqa: E402
    return None


def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    for title, cmd in DEMOS:
        if cmd is None:
            continue
        print(f"rendering: {title}")
        out = run_cmd(cmd)
        slug = re.sub(r'[^a-z0-9]+', '_', title.lower()).strip('_')[:50]
        render_terminal(title, out, os.path.join(OUT_DIR, f"{slug}.png"))

    # Error demos: build them from single files so output is readable
    print("rendering: syntax errors caught")
    parts = []
    for name, label in [('bad_char', 'lex error'), ('missing_then', 'parse error'), ('unmatched_paren', 'parse error')]:
        out = run_cmd(f"python3 gridscript.py tests/invalid/{name}.gsc")
        parts.append(f"$ python3 gridscript.py tests/invalid/{name}.gsc   # {label}\n{out}")
    render_terminal("syntax errors caught", "\n\n".join(parts), os.path.join(OUT_DIR, 'syntax_errors_caught.png'))

    print("rendering: runtime errors caught")
    parts = []
    for name, label in [('undefined_var', 'name error'), ('divide_by_zero', 'arith error'),
                        ('if_not_bool', 'type error'), ('type_error_add', 'type error')]:
        out = run_cmd(f"python3 gridscript.py tests/invalid/{name}.gsc")
        parts.append(f"$ python3 gridscript.py tests/invalid/{name}.gsc   # {label}\n{out}")
    render_terminal("runtime errors caught", "\n\n".join(parts), os.path.join(OUT_DIR, 'runtime_errors_caught.png'))

    print("\nAll screenshots in report/screenshots/")


if __name__ == '__main__':
    sys.exit(main())