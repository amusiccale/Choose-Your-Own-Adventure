"""
models.py

Core data structures for the CYOA Compendium Builder.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class Choice:
    text: str
    target_node: Optional[int] = None
    ending_text: Optional[str] = None

    @property
    def is_ending(self) -> bool:
        return self.ending_text is not None


@dataclass
class Node:
    node_id: int
    title: str
    body: str
    choices: List[Choice] = field(default_factory=list)

    def add_choice(self, choice: Choice) -> None:
        self.choices.append(choice)

    @property
    def is_terminal(self) -> bool:
        return len(self.choices) == 0


@dataclass
class Story:
    filename: str
    title: str
    nodes: Dict[int, Node] = field(default_factory=dict)
    start_node: Optional[int] = None

    def add_node(self, node: Node) -> None:
        self.nodes[node.node_id] = node
        if self.start_node is None:
            self.start_node = node.node_id
        else:
            self.start_node = min(self.start_node, node.node_id)

    @property
    def node_count(self) -> int:
        return len(self.nodes)

    @property
    def ending_count(self) -> int:
        count = 0
        for node in self.nodes.values():
            for choice in node.choices:
                if choice.is_ending:
                    count += 1
        return count

    def get_node(self, node_id: int):
        return self.nodes.get(node_id)

    def sorted_nodes(self):
        return [self.nodes[k] for k in sorted(self.nodes)]


@dataclass
class NodePageReference:
    story_title: str
    node_id: int
    page_number: int
    anchor_name: str


@dataclass
class StoryIndex:
    story_title: str
    node_pages: Dict[int, int] = field(default_factory=dict)
    story_start_page: int = 0
    story_index_page: int = 0


@dataclass
class MissingNodeReference:
    story_title: str
    source_node: int
    missing_target: int
    choice_text: str


@dataclass
class Anthology:
    title: str
    stories: List[Story] = field(default_factory=list)
    cover_image: Optional[str] = None

    def add_story(self, story: Story) -> None:
        self.stories.append(story)

    @property
    def total_story_count(self) -> int:
        return len(self.stories)

    @property
    def total_node_count(self) -> int:
        return sum(story.node_count for story in self.stories)

    def sort_by_filename(self) -> None:
        self.stories.sort(key=lambda s: s.filename.lower())
