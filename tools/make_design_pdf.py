#!/usr/bin/env python3
"""Build the GridScript design document PDF in the report template's style.

Same visual language as tools/make_report_pdf.py (cover page, PAPER/FOREST/
TERRACOTTA palette, DejaVu faces), extended to render the design doc's tables,
code blocks, and h3 headings. Prose is reproduced verbatim.
"""
import html
import os
import re

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (SimpleDocTemplate, PageBreak, Paragraph, Spacer,
                                Table, TableStyle, KeepTogether, Preformatted)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MD = os.path.join(ROOT, 'GridScript_Design_Document.md')
OUT = os.path.join(ROOT, 'report', 'GridScript_Design_Document.pdf')

W, H = A4
DJ = '/usr/share/fonts/truetype/dejavu/'
pdfmetrics.registerFont(TTFont('DejaVuSerif', DJ + 'DejaVuSerif.ttf'))
pdfmetrics.registerFont(TTFont('DejaVuSerif-Bold', DJ + 'DejaVuSerif-Bold.ttf'))
pdfmetrics.registerFont(TTFont('DejaVuSans', DJ + 'DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('DejaVuSans-Bold', DJ + 'DejaVuSans-Bold.ttf'))
pdfmetrics.registerFont(TTFont('DejaVuMono', DJ + 'DejaVuSansMono.ttf'))

PAPER = colors.HexColor('#F6F1E7')
CHARCOAL = colors.HexColor('#28251F')
FOREST = colors.HexColor('#334736')
TERRACOTTA = colors.HexColor('#B9563B')
OCHRE = colors.HexColor('#C79337')
SAGE = colors.HexColor('#D9E0CF')
MUTED = colors.HexColor('#716B60')
CODE_BG = colors.HexColor('#EFE9DA')

styles = {
    'h2': ParagraphStyle('h2', fontName='DejaVuSerif-Bold', fontSize=13, leading=15,
                         textColor=FOREST, spaceBefore=10, spaceAfter=4),
    'h3': ParagraphStyle('h3', fontName='DejaVuSerif-Bold', fontSize=10.5, leading=13,
                         textColor=FOREST, spaceBefore=7, spaceAfter=3),
    'body': ParagraphStyle('body', fontName='DejaVuSans', fontSize=9.4, leading=12.6,
                           textColor=CHARCOAL, spaceAfter=4),
    'bullet': ParagraphStyle('bullet', fontName='DejaVuSans', fontSize=9.4, leading=12.6,
                             leftIndent=14, bulletIndent=4, spaceAfter=3),
    'cell': ParagraphStyle('cell', fontName='DejaVuSans', fontSize=8.2, leading=10.5,
                           textColor=CHARCOAL),
    'cellhead': ParagraphStyle('cellhead', fontName='DejaVuSans-Bold', fontSize=8.2,
                               leading=10.5, textColor=PAPER),
    'code': ParagraphStyle('code', fontName='DejaVuMono', fontSize=7.8, leading=10.6,
                           textColor=CHARCOAL, leftIndent=6),
}

MEMBERS = [
    ('Nabil Ismail Abdulkadir', 'UG22CSC1047', 'Interpreter and semantics'),
    ('Ahmad Auwal Abubakar', 'UG22CSC1075', 'Parser and grammar'),
    ('Abubakar Muhammad Sulaiman', 'UG22CSC1046', 'Lexer and token rules'),
    ('Rukayya Musbahu Imam', 'UG22CSC1040', 'AST and lexical scoping'),
    ('Muhammad Salisu', 'UG20CSC1005', 'Tests and report'),
]


def md_inline(s):
    s = html.escape(s)
    s = re.sub(r'\[([^\]]+)\]\((https?://[^)\s]+)\)',
               r'<a href="\2" color="#9b3f2b"><u>\1</u></a>', s)
    s = re.sub(r'`([^`]+)`', r'<font name="Courier">\1</font>', s)
    s = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', s)
    return re.sub(r'(?<![*\w])\*([^<>*\n]+)\*(?![*\w])', r'<i>\1</i>', s)


def is_separator(cells):
    return all(re.fullmatch(r':?-{2,}:?', c.strip()) for c in cells)


def split_row(line):
    return [c.strip() for c in line.strip().strip('|').split('|')]


def cell_text(cell):
    return re.sub(r'[*`]', '', cell)


def make_table(rows, usable):
    from reportlab.pdfbase.pdfmetrics import stringWidth
    widths = [0.0] * len(rows[0])
    for r, row in enumerate(rows):
        font = 'DejaVuSans-Bold' if r == 0 else 'DejaVuSans'
        for i, cell in enumerate(row):
            widths[i] = max(widths[i], stringWidth(cell_text(cell), font, 8.2) + 14)
    total = sum(widths)
    col_w = [w if total <= usable else usable * (w / total) for w in widths]
    data = [[Paragraph(md_inline(c) if i else md_inline(c), styles['cellhead'] if r == 0 else styles['cell'])
             for i, c in enumerate(row)] for r, row in enumerate(rows)]
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), FOREST),
        ('GRID', (0, 0), (-1, -1), 0.5, SAGE),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ])
    return KeepTogether(Table(data, colWidths=col_w, style=style, hAlign='LEFT'))


def make_code_block(lines, usable):
    # Preformatted draws text literally (no entity decoding), so pass raw lines.
    para = Preformatted('\n'.join(lines), styles['code'])
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), CODE_BG),
        ('BOX', (0, 0), (-1, -1), 0.6, SAGE),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ])
    return Table([[para]], colWidths=[usable], style=style, hAlign='LEFT')


def draw_cover(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(PAPER)
    canvas.rect(0, 0, W, H, fill=1, stroke=0)

    canvas.setFillColor(TERRACOTTA)
    canvas.rect(0, 0, 9 * mm, H, fill=1, stroke=0)

    canvas.setLineWidth(1.5)
    for radius, color in ((60 * mm, TERRACOTTA), (48 * mm, OCHRE), (36 * mm, FOREST)):
        canvas.setStrokeColor(color)
        canvas.circle(W + 17 * mm, H - 37 * mm, radius, fill=0, stroke=1)

    left = 26 * mm
    canvas.setFillColor(CHARCOAL)
    canvas.setFont('DejaVuSerif-Bold', 43)
    canvas.drawString(left, H - 51 * mm, 'GridScript')
    canvas.setFillColor(FOREST)
    canvas.setFont('DejaVuSans', 14.5)
    canvas.drawString(left, H - 62 * mm, 'Design document')
    canvas.setStrokeColor(TERRACOTTA)
    canvas.setLineWidth(2.5)
    canvas.line(left, H - 71 * mm, left + 40 * mm, H - 71 * mm)
    canvas.setFillColor(MUTED)
    canvas.setFont('DejaVuSerif', 12.5)
    canvas.drawString(left, H - 82 * mm, 'A small interpreter for scripting a 2D game actor')

    canvas.setFillColor(FOREST)
    canvas.setFont('DejaVuSerif-Bold', 15)
    canvas.drawString(left, H - 112 * mm, 'Contributors')
    canvas.setStrokeColor(FOREST)
    canvas.setLineWidth(0.8)
    canvas.line(left, H - 117 * mm, W - 20 * mm, H - 117 * mm)

    row_top = H - 126 * mm
    row_h = 18 * mm
    for index, (name, reg_no, role) in enumerate(MEMBERS):
        y = row_top - index * row_h
        canvas.setFillColor(CHARCOAL)
        canvas.setFont('DejaVuSans-Bold', 10)
        canvas.drawString(left, y, name)
        canvas.setFillColor(MUTED)
        canvas.setFont('DejaVuSans', 8.1)
        canvas.drawString(left, y - 5 * mm, reg_no)
        canvas.setFillColor(FOREST)
        canvas.setFont('DejaVuSans-Bold', 8.8)
        canvas.drawRightString(W - 20 * mm, y - 1 * mm, role)
        if index < len(MEMBERS) - 1:
            canvas.setStrokeColor(SAGE)
            canvas.setLineWidth(0.55)
            canvas.line(left, y - 9 * mm, W - 20 * mm, y - 9 * mm)

    canvas.setFillColor(FOREST)
    canvas.rect(9 * mm, 0, W - 9 * mm, 27 * mm, fill=1, stroke=0)
    canvas.setFillColor(PAPER)
    canvas.setFont('DejaVuSans-Bold', 9)
    canvas.drawString(left, 16 * mm, 'CSC 4207  •  ORGANIZATION OF PROGRAMMING LANGUAGES')
    canvas.setFont('DejaVuSans', 8.2)
    canvas.drawString(left, 9 * mm, 'Group 1  •  2026 project submission')
    canvas.restoreState()


def draw_report_furniture(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(PAPER)
    canvas.rect(0, 0, W, H, fill=1, stroke=0)
    canvas.setFillColor(FOREST)
    canvas.rect(0, H - 16 * mm, W, 16 * mm, fill=1, stroke=0)
    canvas.setFillColor(TERRACOTTA)
    canvas.rect(18 * mm, H - 16 * mm, 30 * mm, 1.4 * mm, fill=1, stroke=0)
    canvas.setFillColor(PAPER)
    canvas.setFont('DejaVuSans-Bold', 8.4)
    canvas.drawRightString(W - 18 * mm, H - 10.5 * mm, 'GRIDSCRIPT  |  DESIGN DOCUMENT')
    canvas.setFillColor(MUTED)
    canvas.setFont('DejaVuSans', 7.8)
    canvas.drawCentredString(W / 2, 10 * mm, 'CSC4207  •  Group 1  •  2026')
    canvas.restoreState()


def build():
    usable = W - 36 * mm
    story = [Spacer(1, 1), PageBreak()]
    with open(MD) as f:
        lines = f.read().splitlines()

    i, n = 0, len(lines)
    in_code = False
    code_lines = []
    table_rows = []

    def flush_table():
        if table_rows:
            story.append(make_table(table_rows, usable))
            story.append(Spacer(1, 4))
            table_rows.clear()

    while i < n:
        line = lines[i]
        s = line.strip()

        if s.startswith('```'):
            if in_code:
                story.append(make_code_block(code_lines, usable))
                story.append(Spacer(1, 5))
                code_lines = []
                in_code = False
            else:
                flush_table()
                in_code = True
            i += 1
            continue
        if in_code:
            code_lines.append(line.rstrip())
            i += 1
            continue
        if not s:
            flush_table()
            i += 1
            continue
        if s == '---':
            flush_table()
            i += 1
            continue
        if s.startswith('|'):
            cells = split_row(s)
            if not is_separator(cells):
                table_rows.append(cells)
            i += 1
            continue
        flush_table()
        if s.startswith('# '):
            pass
        elif s.startswith('## GridScript:'):
            pass
        elif s.startswith('## '):
            story.append(Paragraph(md_inline(s[3:]), styles['h2']))
        elif s.startswith('### '):
            story.append(Paragraph(md_inline(s[4:]), styles['h3']))
        elif s.startswith('- '):
            story.append(Paragraph(md_inline(s[2:]), styles['bullet'], bulletText='\u2022'))
        else:
            story.append(Paragraph(md_inline(s), styles['body']))
        i += 1
    flush_table()

    SimpleDocTemplate(OUT, pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm,
                      topMargin=27 * mm, bottomMargin=17 * mm,
                      title='CSC4207 Group 1 Design Document: GridScript',
                      author='Group 1').build(story, onFirstPage=draw_cover,
                                              onLaterPages=draw_report_furniture)
    print('wrote', OUT)


if __name__ == '__main__':
    build()
