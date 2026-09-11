#!/usr/bin/env python3
"""Convert a DOCX document to readable, structure-preserving Markdown."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable

from docx import Document
from docx.document import Document as DocumentObject
from docx.oxml.ns import qn
from docx.table import Table
from docx.text.paragraph import Paragraph


def iter_blocks(document: DocumentObject) -> Iterable[Paragraph | Table]:
    for child in document.element.body.iterchildren():
        if child.tag == qn("w:p"):
            yield Paragraph(child, document)
        elif child.tag == qn("w:tbl"):
            yield Table(child, document)


def escape_cell(text: str) -> str:
    return text.replace("|", r"\|").replace("\n", "<br>")


def format_run(run) -> str:
    text = run.text.replace("\n", "  \n")
    if not text:
        return ""
    if run.bold and run.italic:
        return f"***{text}***"
    if run.bold:
        return f"**{text}**"
    if run.italic:
        return f"*{text}*"
    return text


def paragraph_text(paragraph: Paragraph) -> str:
    parts: list[str] = []
    relationships = paragraph.part.rels
    for child in paragraph._p:
        if child.tag == qn("w:r"):
            for run in paragraph.runs:
                if run._r is child:
                    parts.append(format_run(run))
                    break
        elif child.tag == qn("w:hyperlink"):
            label = "".join(node.text or "" for node in child.iter(qn("w:t")))
            rel_id = child.get(qn("r:id"))
            target = relationships[rel_id].target_ref if rel_id in relationships else ""
            parts.append(f"[{label}]({target})" if target else label)
    return "".join(parts).strip()


def list_level(paragraph: Paragraph) -> int:
    ppr = paragraph._p.pPr
    if ppr is not None and ppr.numPr is not None and ppr.numPr.ilvl is not None:
        return int(ppr.numPr.ilvl.val)
    return 0


def table_markdown(table: Table) -> list[str]:
    rows = [[escape_cell(cell.text.strip()) for cell in row.cells] for row in table.rows]
    if not rows:
        return []
    width = max(len(row) for row in rows)
    rows = [row + [""] * (width - len(row)) for row in rows]
    result = ["| " + " | ".join(rows[0]) + " |"]
    result.append("| " + " | ".join(["---"] * width) + " |")
    result.extend("| " + " | ".join(row) + " |" for row in rows[1:])
    return result


def convert(source: Path, destination: Path) -> None:
    document = Document(source)
    output: list[str] = []
    paragraph_index = 0
    previous_was_list = False

    for block in iter_blocks(document):
        if isinstance(block, Table):
            if output and output[-1] != "":
                output.append("")
            output.extend(table_markdown(block))
            output.append("")
            previous_was_list = False
            continue

        text = paragraph_text(block)
        if not text:
            if output and output[-1] != "":
                output.append("")
            previous_was_list = False
            continue

        style = block.style.name if block.style else ""
        line = text
        is_list = style.startswith("List")

        if paragraph_index == 0:
            line = f"# {block.text.strip()}"
        elif paragraph_index == 1:
            line = f"*{block.text.strip().replace(chr(10), '<br>' + chr(10))}*"
        elif style.startswith("Heading"):
            try:
                source_level = int(style.rsplit(" ", 1)[1])
            except (IndexError, ValueError):
                source_level = 1
            line = f"{'#' * min(source_level + 1, 6)} {block.text.strip()}"
        elif is_list:
            marker = "1." if "Number" in style else "-"
            line = f"{'  ' * list_level(block)}{marker} {text}"

        if output and output[-1] != "" and not (is_list and previous_was_list):
            output.append("")
        output.append(line)
        previous_was_list = is_list
        paragraph_index += 1

    while output and output[-1] == "":
        output.pop()
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text("\n".join(output) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("destination", type=Path)
    args = parser.parse_args()
    convert(args.source, args.destination)


if __name__ == "__main__":
    main()
