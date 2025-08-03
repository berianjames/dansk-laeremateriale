import nltk.data
from nltk.tokenize.punkt import PunktParameters, PunktSentenceTokenizer


def setup_danish_tokenizer():
    """Set up NLTK Danish tokenizer with custom abbreviations."""
    try:
        nltk.data.find("tokenizers/punkt")
    except LookupError:
        print("Downloading NLTK punkt tokenizer...")
        nltk.download("punkt")

    # Load Danish tokenizer
    tokenizer = nltk.data.load("tokenizers/punkt/PY3/danish.pickle")

    # Add custom abbreviations for better Danish sentence detection
    punkt_params = PunktParameters()
    abbreviations = [
        # Numbers
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "10",
        # Common Danish abbreviations
        "mio",
        "mia",
        "kr",
        "dkk",
        "ca",
        "fx",
        "osv",
        "dvs",
        "bl.a",
        "m.v",
        "m.m",
        "m.fl",
        "evt",
        "etc",
        "jf",
        "jvf",
        "inkl",
        "ekskl",
        # Titles and addresses
        "dr",
        "prof",
        "cand",
        "mag",
        "ph.d",
        "mr",
        "mrs",
        "ms",
        # Months (abbreviated)
        "jan",
        "feb",
        "mar",
        "apr",
        "maj",
        "jun",
        "jul",
        "aug",
        "sep",
        "okt",
        "nov",
        "dec",
    ]
    punkt_params.abbrev_types = set(abbreviations)

    return PunktSentenceTokenizer(punkt_params)


def load_text(file_path):
    """Load text from file."""
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


def tokenize_text(text, tokenizer):
    """Tokenize text into sentences using the provided tokenizer."""
    sentences = tokenizer.tokenize(text)

    # Filter out very short sentences (likely artifacts)
    filtered_sentences = []
    for sentence in sentences:
        sentence = sentence.strip()
        if len(sentence) > 10 and not sentence.startswith(
            "#"
        ):  # Skip headers and very short fragments
            filtered_sentences.append(sentence)

    return filtered_sentences


def save_sentences(sentences, output_path):
    """Save sentences to output file."""
    with open(output_path, "w", encoding="utf-8") as file:
        for sentence in sentences:
            file.write(sentence + "\n")


def tokenize_cleaned_text(input_path, output_path):
    """Main function to tokenize cleaned text into sentences."""
    print(f"Loading text from {input_path}...")
    text = load_text(input_path)

    print("Setting up Danish tokenizer...")
    tokenizer = setup_danish_tokenizer()

    print("Tokenizing text into sentences...")
    sentences = tokenize_text(text, tokenizer)

    print(f"Saving {len(sentences)} sentences to {output_path}...")
    save_sentences(sentences, output_path)

    print(f"✓ Sentences saved to {output_path}")
    return sentences


if __name__ == "__main__":
    input_path = "assets/cleaned_text.md"
    output_path = "assets/sentences.txt"

    tokenize_cleaned_text(input_path, output_path)
