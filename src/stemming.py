import json
import os
from datetime import datetime
from pathlib import Path
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

# Inisialisasi stemmer
factory = StemmerFactory()
stemmer = factory.create_stemmer()

# Path ke file JSON input
INPUT_FILE = r"C:\Kuliah\Semester 4\Kecerdasan Artificial\Simple-TikTok-Post-Text-Mining\data\preprocessed-data\tokenization\tokenization-2025-05-25_17-20-50.json"

# Path ke direktori output stemming
OUTPUT_DIR = Path(r"C:\Kuliah\Semester 4\Kecerdasan Artificial\Simple-TikTok-Post-Text-Mining\data\preprocessed-data\stemming")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Buat timestamp untuk nama file
TIMESTAMP = datetime.now().strftime("%Y%m%d-%H%M%S")

def main():
    # Cek file input
    if not os.path.exists(INPUT_FILE):
        print(f"File tidak ditemukan: {INPUT_FILE}")
        return

    # Baca data JSON
    with open(INPUT_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)

    # Proses stemming
    stemmed_comments = []
    for item in data:
        original = " ".join(item)
        stemmed = stemmer.stem(original)
        stemmed_comments.append(stemmed)

    # Preview 5 hasil pertama
    print("\nPreview result from stemming:")
    for i in range(min(5, len(stemmed_comments))):
        print(f"- {stemmed_comments[i]}")

    # Simpan hasil ke file JSON
    output_file = OUTPUT_DIR / f"stemming-{TIMESTAMP}.json"
    print(f"\nMenyimpan hasil ke:\n{output_file}")

    try:
        with open(output_file, "w", encoding="utf-8") as file:
            json.dump(stemmed_comments, file, ensure_ascii=False, indent=2)
        print("File berhasil disimpan.")
    except Exception as e:
        print(f"Gagal menyimpan file: {e}")

if __name__ == "__main__":
    main()
