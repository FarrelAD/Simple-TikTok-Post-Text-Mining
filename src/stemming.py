import json
from datetime import datetime
from pathlib import Path
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from constants import STEMMING_OUTPUT_DIR, TOKENIZATION_OUTPUT_DIR
import questionary

factory = StemmerFactory()
stemmer = factory.create_stemmer()
TIMESTAMP = datetime.now().strftime("%Y%m%d-%H%M%S")

def main():
    tokenization_files = [str(f) for f in Path(TOKENIZATION_OUTPUT_DIR).iterdir() if f.is_file()]

    if not tokenization_files:
        print("Tidak ada file tokenisasi di folder:", TOKENIZATION_OUTPUT_DIR)
        return

    selected_file = questionary.select(
        "Pilih file hasil tokenisasi untuk diproses stemming:",
        choices=tokenization_files
    ).ask()

    print(f"File terpilih: {selected_file}")

    with open(selected_file, "r", encoding="utf-8") as file:
        data = json.load(file)

    stemmed_comments = []
    for item in data:
        original = " ".join(item)
        stemmed = stemmer.stem(original)
        stemmed_comments.append(stemmed)

    print("\nPreview result from stemming:")
    for i in range(min(5, len(stemmed_comments))):
        print(f"- {stemmed_comments[i]}")

    STEMMING_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_file = STEMMING_OUTPUT_DIR / f"stemming-{TIMESTAMP}.json"

    print(f"\nMenyimpan hasil ke:\n{output_file}")
    try:
        with open(output_file, "w", encoding="utf-8") as file:
            json.dump(stemmed_comments, file, ensure_ascii=False, indent=2)
        print("File berhasil disimpan.")
    except Exception as e:
        print(f"Gagal menyimpan file: {e}")

if __name__ == "__main__":
    main()
