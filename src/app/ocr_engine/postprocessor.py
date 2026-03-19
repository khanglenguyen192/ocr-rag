"""
Result postprocessor — merge multi-page OCR output into final Markdown.
"""
import re


def merge_pages(page_texts: list[str]) -> str:
    """
    Merge OCR results from multiple pages into a single Markdown document.
    Each page is separated by a horizontal rule with page number annotation.
    """
    if not page_texts:
        return ""

    if len(page_texts) == 1:
        return page_texts[0].strip()

    parts: list[str] = []
    for i, text in enumerate(page_texts, start=1):
        parts.append(f"<!-- Trang {i} -->\n\n{text.strip()}")

    return "\n\n---\n\n".join(parts)


def clean_markdown(text: str) -> str:
    """
    Light post-processing on raw model output:
    - Strip leading/trailing whitespace
    - Normalize multiple blank lines to maximum 2
    - Remove trailing spaces on each line
    """
    if not text:
        return ""

    # Remove trailing whitespace per line
    lines = [line.rstrip() for line in text.splitlines()]
    text = "\n".join(lines)

    # Collapse 3+ consecutive blank lines → 2
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()

