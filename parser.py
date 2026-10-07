"""
parser.py

Parser for builder-generated CYOA text files.
"""

import os
import re
from typing import List, Tuple

from models import (
    Story,
    Node,
    Choice,
    MissingNodeReference,
)

NODE_SPLIT_RE = re.compile(r"\n(?=# NODE:)")
NODE_ID_RE = re.compile(r'^# NODE:\s*(\d+)', re.M)
TITLE_RE = re.compile(r'^Title:\s*(.+)$', re.M)
DECISION_RE = re.compile(r'^DECISION:\s*(\d+)', re.M)
ENDING_RE = re.compile(r'^\s*-\s*(.*?)\s*->\s*END:\s*"(.*)"\s*$', re.I)
TARGET_RE = re.compile(r'^\s*-\s*(.*?)\s*->\s*(\d+)\s*$')


class ParseResult:
    def __init__(self, story: Story, missing_refs: List[MissingNodeReference]):
        self.story = story
        self.missing_refs = missing_refs


def parse_story_file(path: str) -> ParseResult:
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        text = f.read()

    lines = text.splitlines()
    title = 'Untitled Adventure'
    start_idx = 0

    for i, line in enumerate(lines):
        if line.strip():
            title = line.strip()
            start_idx = i + 1
            break

    story = Story(filename=os.path.basename(path), title=title)

    content = "\n".join(lines[start_idx:]).strip()
    blocks = [b.strip() for b in NODE_SPLIT_RE.split(content) if b.strip()]

    for block in blocks:
        m = NODE_ID_RE.search(block)
        if not m:
            continue

        node_id = int(m.group(1))

        title_match = TITLE_RE.search(block)
        node_title = title_match.group(1).strip() if title_match else f'Node {node_id}'

        dec_match = DECISION_RE.search(block)

        body = ''
        if title_match and dec_match:
            body = block[title_match.end():dec_match.start()].strip()

        node = Node(node_id=node_id, title=node_title, body=body)

        if dec_match:
            choice_lines = block[dec_match.end():].splitlines()

            for line in choice_lines:
                line = line.strip()
                if not line.startswith('-'):
                    continue

                end_match = ENDING_RE.match(line)
                if end_match:
                    node.add_choice(
                        Choice(
                            text=end_match.group(1).strip(),
                            ending_text=end_match.group(2).strip(),
                        )
                    )
                    continue

                target_match = TARGET_RE.match(line)
                if target_match:
                    node.add_choice(
                        Choice(
                            text=target_match.group(1).strip(),
                            target_node=int(target_match.group(2)),
                        )
                    )

        story.add_node(node)

    missing = []
    existing_ids = set(story.nodes.keys())

    for node in story.nodes.values():
        for choice in node.choices:
            if choice.target_node is not None:
                if choice.target_node not in existing_ids:
                    missing.append(
                        MissingNodeReference(
                            story_title=story.title,
                            source_node=node.node_id,
                            missing_target=choice.target_node,
                            choice_text=choice.text,
                        )
                    )

    return ParseResult(story, missing)


def parse_story_files(paths: List[str]) -> Tuple[List[Story], List[MissingNodeReference]]:
    stories = []
    missing_refs = []

    for path in sorted(paths, key=lambda p: os.path.basename(p).lower()):
        result = parse_story_file(path)
        stories.append(result.story)
        missing_refs.extend(result.missing_refs)

    return stories, missing_refs
