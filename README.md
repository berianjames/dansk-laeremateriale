# Dansk Laeremateriale

Danish learning material processing and translation tools for processing the Danish citizenship test study material.

## Installation

This project uses [uv](https://docs.astral.sh/uv/) for fast Python package and project management. To set up the project, follow these steps:

1. Install uv (if not already installed):
    ```
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```

2. Clone the repository:
    ```
    git clone https://github.com/berianjames/dansk-laeremateriale.git
    ```

3. Navigate to the project directory:
    ```
    cd dansk-laeremateriale
    ```

4. Create a virtual environment and install dependencies:
    ```
    uv sync
    ```

## Usage

Ensure that the [source PDF](https://siri.dk/media/10915/laeremateriale-til-indfoedsretsproeven.pdf) is in the `assets` directory.

### Text Processing Workflow

The text processing is split into separate modules for better organization:

1. **Extract and clean PDF text:**
    ```bash
    uv run python extract_pdf.py
    ```
    - Extracts text from the PDF
    - Removes headers, page numbers, and artifacts
    - Fixes paragraph breaks and hyphenated words
    - Preserves section structure with markdown headings
    - **Output:** `assets/cleaned_text.md`

2. **Tokenize into sentences:**
    ```bash
    uv run python sentence_tokenizer.py
    ```
    - Uses Danish language sentence tokenizer
    - Filters out short fragments and headers
    - **Output:** `assets/sentences.txt`

3. **Extract chapters and sections (optional):**
    ```bash
    uv run python extract_chapters.py
    ```
    - Splits text by chapters (Kapitel 1, 2, etc.)
    - Extracts individual sections (1.1, 1.2, etc.)
    - **Output:** `assets/chapters/` and `assets/sections/` directories

### Translation

Translate the processed sentences (requires OpenAI API key):
```bash
uv run python translate.py
```

### Generated Files

After running the text processing workflow, you'll have:
- `assets/cleaned_text.md` - Clean text with markdown structure
- `assets/sentences.txt` - Individual sentences for translation
- `assets/chapters/` - Individual chapter files
- `assets/sections/` - Individual section files (1.1, 1.2, etc.)
