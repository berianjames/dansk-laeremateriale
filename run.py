import fitz
import nltk

doc = fitz.open("assets/laeremateriale-til-indfoedsretsproeven.pdf")
text = ""
for page in doc:
    text += page.get_text()

try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt")

sentences = nltk.sent_tokenize(text, language="danish")

# Save sentences to output.txt (overwrites existing file)
with open("assets/output.txt", "w") as file:
    file.write(text)
    # for sentence in sentences:
    #     file.write(sentence + "\n")
