import json
import os
from pathlib import Path
import questionary
from constants import TOKENIZATION_OUTPUT_DIR, WORD_REPAIR_OUTPUT_DIR, DICTIONARY_PATH 
from spellchecker import SpellChecker

# List semua file hasil tokenisasi
input_path_files = [str(f) for f in Path(TOKENIZATION_OUTPUT_DIR).iterdir() if f.is_file()]

# Pilih file
selected_file: str = questionary.select("Select tokenization file", choices=input_path_files).ask()

# Path kamus dan output
kamus_path = DICTIONARY_PATH/ "custom-kamus-old.json"
output_dir = WORD_REPAIR_OUTPUT_DIR

# Buat folder output jika belum ada
os.makedirs(output_dir, exist_ok=True)

# Buat nama file output dari file yang dipilih
output_filename = os.path.basename(selected_file).replace("tokenization-", "word-repair-")
output_path = os.path.join(output_dir, output_filename)

# Load custom kamus dari file JSON
with open(kamus_path, 'r', encoding='utf-8') as f:
    custom_kamus = json.load(f)

# Inisialisasi spellchecker
spell = SpellChecker(language=None)
spell.word_frequency.load_words(custom_kamus)

# Load data tokenisasi
with open(selected_file, 'r', encoding='utf-8') as file:
    data = json.load(file)

# Perbaiki kata
repaired_data = []
for kalimat in data:
    hasil = []
    for kata in kalimat:
        if kata in spell:
            hasil.append(kata)
        else:
            koreksi = spell.correction(kata)
            hasil.append(koreksi if koreksi else kata)
    repaired_data.append(hasil)

# Simpan hasil perbaikan
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(repaired_data, f, indent=2, ensure_ascii=False)

print("✅ Perbaikan selesai.")
print(f"Hasil disimpan di: {output_path}")