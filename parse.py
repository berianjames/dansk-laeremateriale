import re

import fitz
import nltk.data
from nltk.tokenize.punkt import PunktParameters, PunktSentenceTokenizer

# Extract raw text from PDF
doc = fitz.open("assets/laeremateriale-til-indfoedsretsproeven.pdf")
text = ""
for page in doc:
    text += page.get_text()

# Remove table of contents
text = text.split("\n")
text = text[120:-3]
text = "\n".join(text)

# Remove irrelevant text
title_text = "\nLÆREMATERIALE TIL INDFØDSRETSPRØVEN"
text = text.replace(title_text, "")

# Remove page numbers
page_number_pattern = r"\d+\s*/\s*\d+\s*\|\s*KAPITEL\s+\d+\s*–\s*.+"
text = re.sub(page_number_pattern, "", text)

# Tidy section headings
chapter_head_pattern = r"(Kapitel \d+)\n(.+)\n"
section_head_pattern = r"\n(\d+)\.(\d+) \n(.+)\n"
subsection_head_pattern = r"\n(\d+)\.(\d+)\.(\d+) \n(.+)\n"
chapter_replacement = r"\1 \2\n"
section_replacement = r"\n\1.\2 \3\n"
subsection_replacement = r"\n\1.\2.\3 \4\n"
text = re.sub(chapter_head_pattern, chapter_replacement, text)
text = re.sub(section_head_pattern, section_replacement, text)
text = re.sub(subsection_head_pattern, subsection_replacement, text)

# Remove hyphenations
hypenation_pattern = r"(\w+)-\n(\w+)"
replacement = r"\1\2"
text = re.sub(hypenation_pattern, replacement, text)

# Paragraph breaks and newlines
text = text.replace(" \n\n", " ")
text = text.replace(" \n", " ")
text = text.replace(" •", "\n•")
# text = re.sub(r"\n• (.+?)\n", r"\1, ", text)
text = re.sub(r"\n.*(?:Foto|Grafik):.*\n", "\n", text)  # Remove photo credits
text = re.sub(r"Kapitel \d+\s{2}.+", "\n", text)  # Remove chapter headings
text = re.sub(r"\d+\.\d+(?:\.\d+)?.+\n", "", text)  # Remove section headings
text = re.sub(r"\n[^a-z\n]+\n", "", text)  # Remove headings without lowercase letters
text = text.replace("\n\n", "\n")  # .replace(". ", ".\n")

# Tokenize text into sentences
try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt")

# Load Danish tokenizer for modification
tokenizer = nltk.data.load("tokenizers/punkt/PY3/danish.pickle")
punkt_params = PunktParameters()
abbreviations = ["1", "2", "3", "4", "mio", "mia"]
punkt_params.abbrev_types = set(abbreviations)
new_tokenizer = PunktSentenceTokenizer(punkt_params)
sentences = new_tokenizer.tokenize(text)

# Save sentences to output.txt (overwrites existing file)
with open("assets/sentences_raw.txt", "w") as file:
    # file.write(text)
    for sentence in sentences:
        file.write(sentence + "\n")
