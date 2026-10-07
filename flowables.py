"""
flowables.py

Custom ReportLab flowables for anchors, bookmarks,
and navigation used by the CYOA Compendium Builder.
"""

from reportlab.platypus import Flowable, PageBreak, Paragraph


class AnchorFlowable(Flowable):
    def __init__(self, anchor_name):
        super().__init__()
        self.anchor_name = anchor_name

    def wrap(self, availWidth, availHeight):
        return (0, 0)

    def draw(self):
        try:
            self.canv.bookmarkPage(self.anchor_name)
        except Exception:
            pass


class StoryStartAnchor(AnchorFlowable):
    pass


class StoryIndexAnchor(AnchorFlowable):
    pass


class NodeAnchor(AnchorFlowable):
    pass


class AppendixAnchor(AnchorFlowable):
    pass


class NodePageBreak(PageBreak):
    """Semantic page break: each node begins on a fresh page."""
    pass


class PDFNavigationFactory:

    @staticmethod
    def story_beginning_link(bookmarks, story_title, styles):
        dest = bookmarks.story_beginning_destination(story_title)
        return Paragraph(
            bookmarks.build_internal_link(
                dest,
                'Return to Story Beginning'
            ),
            styles['FooterNav']
        )

    @staticmethod
    def story_index_link(bookmarks, story_title, styles):
        dest = bookmarks.story_index_destination(story_title)
        return Paragraph(
            bookmarks.build_internal_link(
                dest,
                'Return to Story Index'
            ),
            styles['FooterNav']
        )


class PageMapMarker(Flowable):
    def __init__(self, key):
        super().__init__()
        self.key = key

    def wrap(self, availWidth, availHeight):
        return (0, 0)

    def draw(self):
        pass
