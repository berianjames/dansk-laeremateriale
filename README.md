# Project Title

A brief description of what this project does and who it's for.

## Installation

This project uses a conda environment for managing dependencies. To set up the environment and install the project, follow these steps:

1. Clone the repository:
    ```
    git clone https://github.com/berianjames/dansk-laeremateriale.git
    ```
2. Navigate to the project directory:
    ```
    cd dansk-laeremateriale
    ```
3. Create a new conda environment:
    ```
    conda create --name laeremateriale python=3.10
    ```
4. Activate the conda environment:
    ```
    conda activate laeremateriale
    ```
5. Install the project in editable mode:
    ```
    pip install -e .
    ```

## Running the Project

To run the project, ensure that the [source PDF](https://siri.dk/media/10915/laeremateriale-til-indfoedsretsproeven.pdf) is in the `assets` directory. Then, execute:

    ```
    python run.py
    ```

This will generate an `output.txt` file in the project directory.
