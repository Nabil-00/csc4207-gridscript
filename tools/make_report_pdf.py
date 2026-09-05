#!/usr/bin/env python3
"""Build the submission-ready Group 1 report PDF: 2-page report + figure appendix."""
import html
import os
import re

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Image,
                                HRFlowable, KeepTogether)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MD = os.path.join(ROOT, 'report', 'Group1_Report.md')
OUT = os.path.join(ROOT, 'report', 'Group1_Report.pdf')
SHOTS = os.path.join(ROOT, 'report', 'vscode_shots')

FIGURES = [
    ('01_full_test_suite.png', 'Figure 1: the full integration suite passing, 17 of 17.'),
    ('06_tokens_demo.png', 'Figure 2: lexer token output for the patrol program.'),
    ('07_ast_demo.png', 'Figure 3: parser AST output for a function definition.'),
    ('03_patrol_demo.png', 'Figure 4: the patrol program running end to end.'),
    ('04_shadowing_demo.png', 'Figure 5: static scoping proof, 100, 7, 100.'),
    ('10_runtime_error.png', 'Figure 6: an invalid program rejected with its exact message.'),
    ('11_failed_test_caught.png', 'Figure 7: the suite catching a deliberate regression (red FAIL with diff).'),
]

W, H = A4
styles = {
    'title': ParagraphStyle('title', fontName='Helvetica-Bold', fontSize=17, leading=21, spaceAfter=4),
    'group': ParagraphStyle('group', fontName='Helvetica', fontSize=9, leading=12, spaceAfter=8),
    'h2': ParagraphStyle('h2', fontName='Helvetica-Bold', fontSize=12, leading=15, spaceBefore=10, spaceAfter=4),
    'body': ParagraphStyle('body', fontName='Helvetica', fontSize=10.5, leading=14.5, spaceAfter=5, alignment=4),
    'bullet': ParagraphStyle('bullet', parent=None, fontName='Helvetica', fontSize=10.5, leading=14.5,
                             leftIndent=14, bulletIndent=4, spaceAfter=3),
    'caption': ParagraphStyle('caption', fontName='Helvetica-Oblique', fontSize=9, leading=12,
                              spaceBefore=3, spaceAfter=10, alignment=1),
    'appendix': ParagraphStyle('appendix', fontName='Helvetica-Bold', fontSize=14, leading=17,
                               spaceBefore=6, spaceAfter=8),
}


def md_inline(s):
    s = html.escape(s)
    return re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', s)


def build():
    story = []
    with open(MD) as f:
        lines = f.read().splitlines()
    for line in lines:
        s = line.strip()
        if not s:
            continue
        if s.startswith('# '):
            story.append(Paragraph(md_inline(s[2:]), styles['title']))
            story.append(HRFlowable(width='100%', thickness=1, spaceAfter=6))
        elif s.startswith('**Group 1:**'):
            story.append(Paragraph(md_inline(s), styles['group']))
        elif s.startswith('## '):
            story.append(Paragraph(md_inline(s[3:]), styles['h2']))
        elif s.startswith('- '):
            story.append(Paragraph(md_inline(s[2:]), styles['bullet'], bulletText='\u2022'))
        else:
            story.append(Paragraph(md_inline(s), styles['body']))

    story.append(Spacer(1, 6))
    story.append(HRFlowable(width='100%', thickness=1, spaceAfter=6))
    story.append(Paragraph('Appendix A: test evidence', styles['appendix']))

    max_w = W - 2 * 20 * mm
    for fname, caption in FIGURES:
        path = os.path.join(SHOTS, fname)
        img = Image(path)
        scale = max_w / img.imageWidth
        img.drawWidth = max_w
        img.drawHeight = img.imageHeight * scale
        story.append(KeepTogether([img, Paragraph(html.escape(caption), styles['caption'])]))

    def footer(canvas, doc):
        canvas.saveState()
        canvas.setFont('Helvetica', 8)
        canvas.drawCentredString(W / 2, 12 * mm, f'GridScript, CSC4207 Group 1  |  page {doc.page}')
        canvas.restoreState()

    SimpleDocTemplate(OUT, pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm,
                      topMargin=18 * mm, bottomMargin=18 * mm,
                      title='CSC4207 Group 1 Report: GridScript',
                      author='Group 1').build(story, onFirstPage=footer, onLaterPages=footer)
    print('wrote', OUT)


if __name__ == '__main__':
    build()
