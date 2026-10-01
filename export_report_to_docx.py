#!/usr/bin/env python3
"""Build final_report.docx from final_report.md. Requires: pip install python-docx"""
from __future__ import annotations

import re
from pathlib import Path

from docx import Document
from docx.enum.text import WD_LINE_SPACING
from docx.shared import Pt
from docx.oxml.ns import qn
from docx.oxml import OxmlElement


def add_hyperlink(paragraph, url: str, text: str) -> None:
    """Insert a hyperlink into a paragraph (python-docx helper)."""
    part = paragraph.part
    r_id = part.relate_to(
        url,
        "http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink",
        is_external=True,
    )
    hyperlink = OxmlElement("w:hyperlink")
    hyperlink.set(qn("r:id"), r_id)
    new_run = OxmlElement("w:r")
    rPr = OxmlElement("w:rPr")
    u = OxmlElement("w:u")
    u.set(qn("w:val"), "single")
    rPr.append(u)
    color = OxmlElement("w:color")
    color.set(qn("w:val"), "0563C1")
    rPr.append(color)
    new_run.append(rPr)
    t = OxmlElement("w:t")
    t.text = text
    new_run.append(t)
    hyperlink.append(new_run)
    paragraph._p.append(hyperlink)


def split_inline(text: str) -> list[tuple[str, dict]]:
    """Split into segments with style flags: bold, italic, code."""
    if not text:
        return [("", {})]
    segments: list[tuple[str, dict]] = []
    pos = 0
    # Order: **bold**, `code`, *italic* (single asterisk not **)
    pattern = re.compile(
        r"\*\*(.+?)\*\*|`([^`]+)`|\*([^*]+)\*",
        re.DOTALL,
    )
    for m in pattern.finditer(text):
        if m.start() > pos:
            segments.append((text[pos : m.start()], {}))
        if m.group(1) is not None:
            segments.append((m.group(1), {"bold": True}))
        elif m.group(2) is not None:
            segments.append((m.group(2), {"code": True}))
        else:
            segments.append((m.group(3), {"italic": True}))
        pos = m.end()
    if pos < len(text):
        segments.append((text[pos:], {}))
    return segments or [("", {})]


def add_paragraph_with_inline(doc: Document, text: str, style: str | None = None) -> None:
    text = text.strip()
    if not text:
        return
    p = doc.add_paragraph(style=style)
    # Pure URL line -> hyperlink only
    if re.fullmatch(r"https?://\S+", text):
        add_hyperlink(p, text, text)
        return
    for chunk, fmt in split_inline(text):
        if not chunk:
            continue
        run = p.add_run(chunk)
        if fmt.get("bold"):
            run.bold = True
        if fmt.get("italic"):
            run.italic = True
        if fmt.get("code"):
            run.font.name = "Consolas"
            run.font.size = Pt(10)
    # If line has URL at end after space
    m = re.search(r"(https?://\S+)\s*$", text)
    if m and not re.fullmatch(r"https?://\S+", text):
        url = m.group(1)
        # Rebuild: simpler — append hyperlink run for trailing URL in references
        pass  # keep inline parsing only; references often have URL on own line already


def main() -> None:
    root = Path(__file__).resolve().parent
    md_path = root / "final_report.md"
    out_path = root / "final_report.docx"

    lines = md_path.read_text(encoding="utf-8").splitlines()

    doc = Document()
    style = doc.styles["Normal"]
    style.font.name = "Calibri"
    style.font.size = Pt(11)
    style.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE

    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if not stripped:
            i += 1
            continue

        if stripped == "---":
            i += 1
            continue

        # ATX headings
        if stripped.startswith("#"):
            level = len(stripped) - len(stripped.lstrip("#"))
            title = stripped[level:].strip()
            # Map # -> Title, ## -> 1, etc. Word: 0=Title, 1=Heading 1
            if level == 1:
                doc.add_heading(title, level=1)
            else:
                doc.add_heading(title, level=min(level, 3))
            i += 1
            continue

        # Bullet list
        if stripped.startswith("- "):
            text = stripped[2:].strip()
            p = doc.add_paragraph(style="List Bullet")
            for chunk, fmt in split_inline(text):
                if not chunk:
                    continue
                run = p.add_run(chunk)
                if fmt.get("bold"):
                    run.bold = True
                if fmt.get("italic"):
                    run.italic = True
                if fmt.get("code"):
                    run.font.name = "Consolas"
            i += 1
            continue

        # Numbered list (1. ...)
        num_m = re.match(r"^(\d+)\.\s+(.*)$", stripped)
        if num_m:
            text = num_m.group(2)
            p = doc.add_paragraph(style="List Number")
            for chunk, fmt in split_inline(text):
                if not chunk:
                    continue
                run = p.add_run(chunk)
                if fmt.get("bold"):
                    run.bold = True
                if fmt.get("italic"):
                    run.italic = True
                if fmt.get("code"):
                    run.font.name = "Consolas"
            i += 1
            continue

        # Default paragraph (may be multi-line until blank)
        buf = [stripped]
        i += 1
        while i < len(lines):
            nxt = lines[i].strip()
            if not nxt or nxt == "---" or nxt.startswith("#") or nxt.startswith("- ") or re.match(r"^\d+\.\s", nxt):
                break
            buf.append(nxt)
            i += 1
        combined = " ".join(buf)
        add_paragraph_with_inline(doc, combined)
        continue

    doc.save(str(out_path))
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
