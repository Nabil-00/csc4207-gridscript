#!/usr/bin/env python3
"""Build the GridScript cover page and linked one-page report as one PDF."""
import html
import os
import re

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, PageBreak, Paragraph, Spacer

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MD = os.path.join(ROOT, 'report', 'Group1_Report.md')
OUT = os.path.join(ROOT, 'report', 'Group1_Report.pdf')

W, H = A4
pdfmetrics.registerFont(TTFont('DejaVuSerif', '/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf'))
pdfmetrics.registerFont(TTFont('DejaVuSerif-Bold', '/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf'))
pdfmetrics.registerFont(TTFont('DejaVuSans', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('DejaVuSans-Bold', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'))

PAPER = colors.HexColor('#F6F1E7')
CHARCOAL = colors.HexColor('#28251F')
FOREST = colors.HexColor('#334736')
TERRACOTTA = colors.HexColor('#B9563B')
OCHRE = colors.HexColor('#C79337')
SAGE = colors.HexColor('#D9E0CF')
MUTED = colors.HexColor('#716B60')
styles = {
    'h2': ParagraphStyle('h2', fontName='DejaVuSerif-Bold', fontSize=12, leading=14,
                         textColor=FOREST, spaceBefore=7, spaceAfter=3),
    'body': ParagraphStyle('body', fontName='DejaVuSans', fontSize=9.4, leading=12.4,
                           textColor=CHARCOAL, spaceAfter=3),
    'bullet': ParagraphStyle('bullet', parent=None, fontName='DejaVuSans', fontSize=10.5, leading=14.5,
                             leftIndent=14, bulletIndent=4, spaceAfter=3),
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
    return re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', s)


def draw_cover(canvas, doc):
    """Draw an editorial A4 cover page behind an intentionally empty story page."""
    canvas.saveState()
    canvas.setFillColor(PAPER)
    canvas.rect(0, 0, W, H, fill=1, stroke=0)

    canvas.setFillColor(TERRACOTTA)
    canvas.rect(0, 0, 9 * mm, H, fill=1, stroke=0)

    # Cropped concentric rings give the cover a language-and-logic identity without
    # falling back to a literal grid or dashboard-style decoration.
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
    canvas.drawString(left, H - 62 * mm, 'Design and implementation report')
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
    canvas.drawRightString(W - 18 * mm, H - 10.5 * mm, 'GRIDSCRIPT  |  PROJECT REPORT')
    canvas.setFillColor(MUTED)
    canvas.setFont('DejaVuSans', 7.8)
    canvas.drawCentredString(W / 2, 10 * mm, 'CSC4207  •  Group 1  •  2026')
    canvas.restoreState()


def build():
    # The first page contains only a tiny flowable; draw_cover supplies its artwork.
    story = [Spacer(1, 1), PageBreak()]
    with open(MD) as f:
        lines = f.read().splitlines()
    for line in lines:
        s = line.strip()
        if not s:
            continue
        if s.startswith('# ') or s.startswith('**Group 1:**'):
            continue
        elif s.startswith('## '):
            story.append(Paragraph(md_inline(s[3:]), styles['h2']))
        elif s.startswith('- '):
            story.append(Paragraph(md_inline(s[2:]), styles['bullet'], bulletText='\u2022'))
        else:
            story.append(Paragraph(md_inline(s), styles['body']))

    SimpleDocTemplate(OUT, pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm,
                      topMargin=27 * mm, bottomMargin=17 * mm,
                      title='CSC4207 Group 1 Report: GridScript',
                      author='Group 1').build(story, onFirstPage=draw_cover,
                                               onLaterPages=draw_report_furniture)
    print('wrote', OUT)


if __name__ == '__main__':
    build()
