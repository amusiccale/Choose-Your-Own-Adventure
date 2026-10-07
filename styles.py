"""
pdf/styles.py

Centralized ReportLab style definitions for the
CYOA Compendium Builder.
"""

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


DEFAULT_BODY_FONT = "Times-Roman"
DEFAULT_TITLE_FONT = "Times-Bold"


def register_optional_fonts():
    """
    Placeholder for future Garamond registration.

    Falls back safely to built-in fonts to maximize
    cross-platform compatibility.
    """
    return



def build_styles():
    styles = getSampleStyleSheet()

    styles.add(
        ParagraphStyle(
            name="BookTitle",
            parent=styles["Title"],
            fontName=DEFAULT_TITLE_FONT,
            fontSize=26,
            leading=30,
            alignment=1,
            spaceAfter=24,
        )
    )

    styles.add(
        ParagraphStyle(
            name="StoryTitle",
            parent=styles["Title"],
            fontName=DEFAULT_TITLE_FONT,
            fontSize=22,
            leading=26,
            alignment=1,
            spaceAfter=18,
        )
    )

    styles.add(
        ParagraphStyle(
            name="NodeHeading",
            parent=styles["Heading1"],
            fontName=DEFAULT_TITLE_FONT,
            fontSize=16,
            leading=20,
            spaceAfter=12,
        )
    )

    styles.add(
        ParagraphStyle(
            name="StoryMeta",
            parent=styles["Normal"],
            fontSize=11,
            leading=14,
            alignment=1,
            textColor=colors.darkslategray,
        )
    )

    styles.add(
        ParagraphStyle(
            name="Body",
            parent=styles["BodyText"],
            fontName=DEFAULT_BODY_FONT,
            fontSize=11,
            leading=15,
            spaceAfter=8,
        )
    )

    styles.add(
        ParagraphStyle(
            name="Choice",
            parent=styles["BodyText"],
            fontName=DEFAULT_BODY_FONT,
            fontSize=11,
            leading=15,
            leftIndent=18,
            spaceBefore=3,
            spaceAfter=3,
        )
    )

    styles.add(
        ParagraphStyle(
            name="Ending",
            parent=styles["Heading2"],
            alignment=1,
            textColor=colors.darkred,
        )
    )

    styles.add(
        ParagraphStyle(
            name="IndexEntry",
            parent=styles["Normal"],
            fontSize=10,
            leading=12,
        )
    )

    styles.add(
        ParagraphStyle(
            name="FooterNav",
            parent=styles["Normal"],
            alignment=1,
            fontSize=9,
            textColor=colors.blue,
        )
    )

    return styles
