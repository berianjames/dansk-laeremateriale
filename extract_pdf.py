import re

import fitz


def extract_pdf_text(pdf_path):
    """Extract raw text from PDF file."""
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text


def remove_table_of_contents(text):
    """Remove table of contents by slicing text."""
    text_lines = text.split("\n")
    # Remove first 120 lines (table of contents) and last 3 lines
    text_lines = text_lines[120:-3]
    return "\n".join(text_lines)


def clean_text(text):
    """Apply comprehensive text cleaning for Danish PDF content."""

    # Remove title repetitions
    title_text = "\nLÆREMATERIALE TIL INDFØDSRETSPRØVEN"
    text = text.replace(title_text, "")

    # Remove page numbers and headers
    page_number_pattern = r"\d+\s*/\s*\d+\s*\|\s*KAPITEL\s+\d+\s*–\s*.+"
    text = re.sub(page_number_pattern, "", text)

    # Remove photo and graphic credits
    text = re.sub(r"\n.*(?:Foto|Grafik|Illustration):.*\n", "\n", text)
    text = re.sub(r"\n.*(?:Kilde|Source):.*\n", "\n", text)

    # Remove soft hyphens that break words across lines
    text = text.replace("­", "")

    # Fix hyphenated words split across lines
    hyphenation_pattern = r"(\w+)-\n(\w+)"
    text = re.sub(hyphenation_pattern, r"\1\2", text)

    # Intelligently join lines that belong to the same paragraph
    # The key insight: true paragraph breaks in PDF have empty lines,
    # line wrapping just continues to next line
    lines = text.split("\n")
    paragraph_lines = []
    current_paragraph = []

    i = 0
    while i < len(lines):
        line = lines[i].strip()

        # Empty line indicates paragraph break
        if not line:
            if current_paragraph:
                paragraph_lines.append(" ".join(current_paragraph))
                current_paragraph = []
            paragraph_lines.append("")  # Keep the empty line
            i += 1
            continue

        # Check if this line starts a new structural element
        is_structural = (
            re.match(r"^\d+\.\d+", line)  # Section numbers
            or re.match(r"^[A-ZÆØÅ\s]+$", line)  # All caps headers
            or re.match(r"^•", line)  # Bullet points
            or re.match(r"^Kapitel", line)  # Chapter headings
            or line.endswith(":")  # Lines ending with colon (often headers)
            or (len(line) < 60 and line.isupper())  # Short uppercase lines
        )

        if is_structural:
            # Finish current paragraph if exists
            if current_paragraph:
                paragraph_lines.append(" ".join(current_paragraph))
                current_paragraph = []
            # Add the structural line
            paragraph_lines.append(line)
            i += 1
            continue

        # Regular content line - add to current paragraph
        current_paragraph.append(line)
        i += 1

    # Don't forget the last paragraph
    if current_paragraph:
        paragraph_lines.append(" ".join(current_paragraph))

    text = "\n".join(paragraph_lines)

    # Handle bullet points properly
    text = text.replace(" •", "\n•")

    # Remove excessive whitespace
    text = re.sub(r"\n{3,}", "\n\n", text)  # Max 2 consecutive newlines
    text = re.sub(r" {2,}", " ", text)  # Max 1 space between words

    # Remove standalone numbers or short fragments on their own lines
    text = re.sub(r"\n\d+\s*\n", "\n", text)
    text = re.sub(r"\n[A-ZÆØÅ]{1,3}\s*\n", "\n", text)

    return text


def preserve_section_structure(text):
    """Preserve and format section headings for future chapter extraction."""

    # Format chapter headings (Kapitel X Title) - handle various spacing
    chapter_pattern = r"(Kapitel \d+)\s*\n\s*(.+)\n"
    text = re.sub(chapter_pattern, r"# \1: \2\n\n", text)

    # Format main section headings (X.Y Title) - handle various spacing patterns
    section_pattern = r"\n(\d+)\.(\d+)\s*\n\s*(.+)\n"
    text = re.sub(section_pattern, r"\n## \1.\2 \3\n\n", text)

    # Format subsection headings (X.Y.Z Title)
    subsection_pattern = r"\n(\d+)\.(\d+)\.(\d+) \n(.+)\n"
    text = re.sub(subsection_pattern, r"\n### \1.\2.\3 \4\n\n", text)

    return text


def final_cleanup(text):
    """Final cleanup pass to remove any remaining artifacts."""

    # Remove lines that are mostly uppercase (likely headers we missed)
    lines = text.split("\n")
    cleaned_lines = []

    for line in lines:
        # Skip lines that are mostly uppercase and short (likely artifacts)
        if len(line.strip()) > 0:
            uppercase_ratio = sum(1 for c in line if c.isupper()) / len(line.strip())
            if (
                uppercase_ratio > 0.8
                and len(line.strip()) < 50
                and not line.startswith("#")
            ):
                continue
        cleaned_lines.append(line)

    text = "\n".join(cleaned_lines)

    # Clean up multiple consecutive empty lines
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


def extract_and_clean_pdf(pdf_path, output_path):
    """Main function to extract and clean PDF text."""
    print("Extracting text from PDF...")
    raw_text = extract_pdf_text(pdf_path)

    print("Removing table of contents...")
    text = remove_table_of_contents(raw_text)

    print("Cleaning text...")
    text = clean_text(text)

    print("Preserving section structure...")
    text = preserve_section_structure(text)

    print("Final cleanup...")
    text = final_cleanup(text)

    print(f"Saving cleaned text to {output_path}...")
    with open(output_path, "w", encoding="utf-8") as file:
        file.write(text)

    print(f"✓ Cleaned text saved to {output_path}")
    return text


if __name__ == "__main__":
    pdf_path = "assets/laeremateriale-til-indfoedsretsproeven.pdf"
    output_path = "assets/cleaned_text.md"

    extract_and_clean_pdf(pdf_path, output_path)
