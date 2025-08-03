import os
import re


def load_cleaned_text(file_path):
    """Load the cleaned markdown text."""
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


def extract_chapters(text):
    """Extract individual chapters from the cleaned text."""
    chapters = {}

    # Split by chapter headings (# Kapitel X: Title)
    chapter_pattern = r"(# Kapitel \d+:.*?)(?=# Kapitel \d+:|$)"
    chapter_matches = re.findall(chapter_pattern, text, re.DOTALL)

    for chapter_text in chapter_matches:
        # Extract chapter number and title
        title_match = re.match(r"# Kapitel (\d+): (.+)", chapter_text.split("\n")[0])
        if title_match:
            chapter_num = int(title_match.group(1))
            chapter_title = title_match.group(2).strip()
            chapters[chapter_num] = {
                "title": chapter_title,
                "content": chapter_text.strip(),
            }

    return chapters


def extract_sections(chapter_content):
    """Extract sections (X.Y) from a chapter."""
    sections = {}

    # Split by section headings (## X.Y Title)
    section_pattern = r"(## \d+\.\d+.*?)(?=## \d+\.\d+|$)"
    section_matches = re.findall(section_pattern, chapter_content, re.DOTALL)

    for section_text in section_matches:
        # Extract section number
        title_match = re.match(r"## (\d+)\.(\d+) (.+)", section_text.split("\n")[0])
        if title_match:
            section_num = f"{title_match.group(1)}.{title_match.group(2)}"
            section_title = title_match.group(3).strip()
            sections[section_num] = {
                "title": section_title,
                "content": section_text.strip(),
            }

    return sections


def save_chapters_separately(chapters, output_dir="assets/chapters"):
    """Save each chapter to a separate file."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for chapter_num, chapter_data in chapters.items():
        filename = f"chapter_{chapter_num:02d}_{chapter_data['title'][:30].replace(' ', '_').lower()}.md"
        # Clean filename of special characters
        filename = re.sub(r"[^\w\-_\.]", "", filename)

        file_path = os.path.join(output_dir, filename)
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(chapter_data["content"])

        print(f"Saved Chapter {chapter_num}: {chapter_data['title']} → {filename}")


def save_sections_separately(chapters, output_dir="assets/sections"):
    """Save each section to a separate file."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for chapter_num, chapter_data in chapters.items():
        sections = extract_sections(chapter_data["content"])

        for section_num, section_data in sections.items():
            filename = f"section_{section_num}_{section_data['title'][:30].replace(' ', '_').lower()}.md"
            # Clean filename of special characters
            filename = re.sub(r"[^\w\-_\.]", "", filename)

            file_path = os.path.join(output_dir, filename)
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(section_data["content"])

            print(f"Saved Section {section_num}: {section_data['title']} → {filename}")


def main():
    """Main function to extract chapters and sections."""
    input_path = "assets/cleaned_text.md"

    print("Loading cleaned text...")
    text = load_cleaned_text(input_path)

    print("Extracting chapters...")
    chapters = extract_chapters(text)

    print(f"Found {len(chapters)} chapters:")
    for num, data in chapters.items():
        print(f"  Chapter {num}: {data['title']}")

    print("\nSaving chapters separately...")
    save_chapters_separately(chapters)

    print("\nSaving sections separately...")
    save_sections_separately(chapters)

    print("\n✓ Chapter and section extraction complete!")


if __name__ == "__main__":
    main()
