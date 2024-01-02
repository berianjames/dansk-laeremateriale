from openai import OpenAI

client = OpenAI()

with open("assets/sentences_fixed.txt", "r") as f:
    sentences = [line.strip() for line in f.readlines()]


def translate_sentence(sentence):
    prompt = f"Translate the following sentence from Danish to English: `{sentence}`"
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt},
        ],
    )
    return response.choices[0].message.content.strip().replace('"', "")


for sentence in sentences:
    with open("assets/translation.txt", "a") as f:
        f.write(f"{translate_sentence(sentence)}\n")
