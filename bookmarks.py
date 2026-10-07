"""
pdf/bookmarks.py

Bookmark and anchor management for the
CYOA Compendium Builder.

This module centralizes anchor naming so hyperlinks,
TOC entries, story indexes, and appendix entries
all point to consistent destinations.
"""

from dataclasses import dataclass
from typing import Dict, Tuple


@dataclass
class AnchorRecord:
    name: str
    story_title: str
    page_number: int = 0


class BookmarkManager:

    def __init__(self):
        self._anchors: Dict[str, AnchorRecord] = {}

    # ----------------------------------
    # Story Anchors
    # ----------------------------------

    def story_start_anchor(self, story_title: str) -> str:
        return f"story_start::{self._clean(story_title)}"

    def story_index_anchor(self, story_title: str) -> str:
        return f"story_index::{self._clean(story_title)}"

    def story_toc_anchor(self, story_title: str) -> str:
        return f"toc_story::{self._clean(story_title)}"

    # ----------------------------------
    # Node Anchors
    # ----------------------------------

    def node_anchor(self, story_title: str, node_id: int) -> str:
        return (
            f"node::{self._clean(story_title)}::{node_id}"
        )

    # ----------------------------------
    # Appendix Anchors
    # ----------------------------------

    def appendix_story_anchor(self, story_title: str) -> str:
        return f"appendix::{self._clean(story_title)}"

    # ----------------------------------
    # Registration
    # ----------------------------------

    def register_anchor(
        self,
        anchor_name: str,
        story_title: str,
        page_number: int,
    ) -> None:

        self._anchors[anchor_name] = AnchorRecord(
            name=anchor_name,
            story_title=story_title,
            page_number=page_number,
        )

    def has_anchor(self, anchor_name: str) -> bool:
        return anchor_name in self._anchors

    def page_for_anchor(self, anchor_name: str):

        record = self._anchors.get(anchor_name)

        if not record:
            return None

        return record.page_number

    # ----------------------------------
    # Convenience Links
    # ----------------------------------

    def node_destination(
        self,
        story_title: str,
        node_id: int,
    ) -> str:

        return self.node_anchor(
            story_title,
            node_id,
        )

    def story_beginning_destination(
        self,
        story_title: str,
    ) -> str:

        return self.story_start_anchor(
            story_title
        )

    def story_index_destination(
        self,
        story_title: str,
    ) -> str:

        return self.story_index_anchor(
            story_title
        )

    # ----------------------------------
    # PDF-Friendly Links
    # ----------------------------------

    def build_internal_link(
        self,
        destination_anchor: str,
        text: str,
    ) -> str:

        return (
            f'<link href="#{destination_anchor}">{text}</link>'
        )

    # ----------------------------------
    # Utilities
    # ----------------------------------

    @staticmethod
    def _clean(text: str) -> str:

        safe = []

        for ch in text:

            if ch.isalnum():
                safe.append(ch.lower())
            else:
                safe.append('_')

        return ''.join(safe)
