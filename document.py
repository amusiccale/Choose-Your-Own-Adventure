"""
document.py

Minimal tested foundation for the PDF subsystem.
Designed to work with later builder.py and flowables.py modules.
"""

from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate
from reportlab.lib.units import inch


class CompendiumDocTemplate(BaseDocTemplate):
    """
    6x9 trade paperback document template.

    Provides:
        - page numbering
        - header/footer hooks
        - TOC entry collection
        - page map collection
    """

    def __init__(self, filename, title='Collected Choose Your Own Adventures', **kwargs):

        self.book_title = title
        self.current_story_title = ''

        self.page_map = {}
        self.toc_entries = []

        super().__init__(
            filename,
            pagesize=(6 * inch, 9 * inch),
            leftMargin=0.75 * inch,
            rightMargin=0.60 * inch,
            topMargin=0.70 * inch,
            bottomMargin=0.70 * inch,
            **kwargs
        )

        frame = Frame(
            self.leftMargin,
            self.bottomMargin,
            self.width,
            self.height,
            id='normal'
        )

        template = PageTemplate(
            id='compendium',
            frames=[frame],
            onPage=self._draw_header_footer
        )

        self.addPageTemplates([template])

    def register_toc_entry(self, level, text, page_number):
        self.toc_entries.append((level, text, page_number))

    def register_page(self, key, page_number):
        self.page_map[key] = page_number

    def set_story_title(self, title):
        self.current_story_title = title or ''

    def _draw_header_footer(self, canvas, doc):

        canvas.saveState()

        if self.current_story_title:
            canvas.setFont('Times-Roman', 9)
            canvas.drawCentredString(
                doc.pagesize[0] / 2,
                doc.pagesize[1] - 0.45 * inch,
                self.current_story_title
            )

        canvas.setFont('Times-Roman', 9)
        canvas.drawCentredString(
            doc.pagesize[0] / 2,
            0.40 * inch,
            str(canvas.getPageNumber())
        )

        canvas.restoreState()
