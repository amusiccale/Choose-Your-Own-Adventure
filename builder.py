"""
builder.py
Phase 1 anthology builder (draft merged version).
"""

from reportlab.platypus import Paragraph, PageBreak, Spacer

try:
    from reportlab.platypus import Image as RLImage
except ImportError:
    RLImage = None

from styles import build_styles
from bookmarks import BookmarkManager
from flowables import (
    StoryStartAnchor,
    StoryIndexAnchor,
    NodeAnchor,
    NodePageBreak,
    PDFNavigationFactory,
)
from document import CompendiumDocTemplate


class CompendiumBuilder:

    def __init__(self):

        self.styles = build_styles()
        self.pending_endings = []

        self.bookmarks = BookmarkManager()

        #
        # Phase 2 page mapping
        #
        self.node_page_map = {}

        self.story_page_map = {}

    def record_page(
        self,
        key,
        page_number,
    ):

        if key in self.story_page_map:
            self.story_page_map[key] = page_number

        if key in self.node_page_map:
            self.node_page_map[key] = page_number
        

    def build_pdf(self, anthology, output_file):
        doc = CompendiumDocTemplate(output_file, title=anthology.title)
        story_flowables = []

        self._build_cover(anthology, story_flowables)
        self._build_placeholder_toc(anthology, story_flowables)

        for story in anthology.stories:
            self._build_story(story, story_flowables)

        self._build_appendix(anthology, story_flowables)
        doc.build(story_flowables)

    def _build_cover(self, anthology, flowables):
        if anthology.cover_image and RLImage:
            try:
                flowables.append(RLImage(anthology.cover_image, width=288, height=288))
            except Exception:
                pass

        flowables.append(Paragraph(anthology.title, self.styles['BookTitle']))
        flowables.append(PageBreak())

    def _build_placeholder_toc(self, anthology, flowables):
        flowables.append(Paragraph('Contents', self.styles['StoryTitle']))
        for story in anthology.stories:
            flowables.append(Paragraph(story.title, self.styles['Body']))
        flowables.append(PageBreak())

    def _build_ending_pages(
            self,
            story,
            flowables,
        ):

        for ending_story, anchor, text in self.pending_endings:

            if ending_story != story.title:
                continue

            flowables.append(
                NodePageBreak()
            )

            flowables.append(
                NodeAnchor(anchor)
            )

            flowables.append(
                Paragraph(
                    "THE END",
                    self.styles["Ending"]
                )
            )

            flowables.append(
                Paragraph(
                    text,
                    self.styles["Body"]
                )
            )

            flowables.append(
                Spacer(1, 18)
            )

            flowables.append(
                PDFNavigationFactory
                .story_beginning_link(
                    self.bookmarks,
                    story.title,
                    self.styles
                )
            )

            flowables.append(
                PDFNavigationFactory
                .story_index_link(
                    self.bookmarks,
                    story.title,
                    self.styles
                )
            )
                
    def _build_story(self, story, flowables):
        anchor = self.bookmarks.story_start_anchor(story.title)
        flowables.append(StoryStartAnchor(anchor))
        self.story_page_map[
            story.title
        ] = None

        flowables.append(Paragraph(story.title, self.styles['StoryTitle']))
        flowables.append(Paragraph(f'Original File: {story.filename}', self.styles['StoryMeta']))
        flowables.append(Paragraph(f'Nodes: {story.node_count}', self.styles['StoryMeta']))
        flowables.append(Paragraph(f'Endings: {story.ending_count}', self.styles['StoryMeta']))
        flowables.append(PageBreak())

        for node in story.sorted_nodes():

            self._build_node(
                story,
                node,
                flowables
            )

        self._build_ending_pages(
            story,
            flowables
        )

        self._build_story_index(
            story,
            flowables
        )

    def _build_node(self, story, node, flowables):
        flowables.append(NodePageBreak())

        node_anchor = self.bookmarks.node_anchor(story.title, node.node_id)
        flowables.append(NodeAnchor(node_anchor))
        self.node_page_map[
            (
                story.title,
                node.node_id
            )
        ] = None

        flowables.append(Paragraph(f'Node {node.node_id}: {node.title}', self.styles['NodeHeading']))
        flowables.append(Paragraph(node.body or '', self.styles['Body']))
        flowables.append(Spacer(1, 8))

        for choice in node.choices:
            self._build_choice(story, choice, flowables)

        flowables.append(Spacer(1, 18))
        flowables.append(PDFNavigationFactory.story_beginning_link(self.bookmarks, story.title, self.styles))
        flowables.append(PDFNavigationFactory.story_index_link(self.bookmarks, story.title, self.styles))

    def _build_choice(self, story, choice, flowables):
        if choice.is_ending:
            ending_id = len(
                self.pending_endings
            ) + 1

            ending_anchor = (
                f"ending::{story.title}::{ending_id}"
            )

            self.pending_endings.append(
                (
                    story.title,
                    ending_anchor,
                    choice.ending_text
                )
            )

            text = self.bookmarks.build_internal_link(
                ending_anchor,
                (
                    f"{choice.text}"
                    f" ..... Page ?"
                )
            )

        else:
            anchor = self.bookmarks.node_anchor(
                story.title,
                choice.target_node
            )

            target_page = self.node_page_map.get(
                (
                    story.title,
                    choice.target_node
                )
            )

            if target_page:

                label = (
                    f"{choice.text}"
                    f" ..... Page {target_page}"
                )

            else:

                label = (
                    f"{choice.text}"
                    f" ..... Page ?"
                )

            text = self.bookmarks.build_internal_link(
                anchor,
                label
            )

        flowables.append(Paragraph(text, self.styles['Choice']))

    def _build_story_index(self, story, flowables):
        flowables.append(PageBreak())
        flowables.append(StoryIndexAnchor(self.bookmarks.story_index_anchor(story.title)))
        flowables.append(Paragraph('Story Index', self.styles['StoryTitle']))

        for node in story.sorted_nodes():

            anchor = self.bookmarks.node_anchor(
                story.title,
                node.node_id
            )

            page_number = self.node_page_map.get(
                (
                    story.title,
                    node.node_id
                )
            )

            if page_number:

                label = (
                    f"Node "
                    f"{node.node_id}"
                    f" - "
                    f"{node.title}"
                    f" ..... "
                    f"{page_number}"
                )

            else:

                label = (
                    f"Node "
                    f"{node.node_id}"
                    f" - "
                    f"{node.title}"
                    f" ..... ?"
                )

            flowables.append(
                Paragraph(
                    self.bookmarks.build_internal_link(
                        anchor,
                        label
                    ),
                    self.styles['IndexEntry']
                )
            )

    def _build_appendix(self, anthology, flowables):
        flowables.append(PageBreak())
        flowables.append(Paragraph('Appendix', self.styles['StoryTitle']))

        for story in anthology.stories:
            flowables.append(Paragraph(story.title, self.styles['NodeHeading']))

            for node in story.sorted_nodes():
                anchor = self.bookmarks.node_anchor(story.title, node.node_id)
                flowables.append(
                    Paragraph(
                        self.bookmarks.build_internal_link(anchor, f'Node {node.node_id} - {node.title}'),
                        self.styles['IndexEntry']
                    )
                )
