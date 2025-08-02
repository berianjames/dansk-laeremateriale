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

## Running the Project

To run the project, ensure that the [source PDF](https://siri.dk/media/10915/laeremateriale-til-indfoedsretsproeven.pdf) is in the `assets` directory. Then, execute:

1. Parse the PDF into sentences:
    ```
    uv run python parse.py
    ```

2. Translate the sentences (requires OpenAI API key):
    ```
    uv run python translate.py
    ```

This will generate processed text files in the `assets` directory.
