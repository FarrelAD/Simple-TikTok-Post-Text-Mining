import json
import os
import constants
from spellchecker import SpellChecker

# Path
input_path = os.path.join(constants.TOKENIZATION_OUTPUT_DIR, 'tokenization-2025-05-25_17-20-50.json')
kamus_path = constants.DICTIONARY_PATH
output_dir = constants.WORD_REPAIR_OUTPUT_DIR

# Buat folder output kalau belum ada
os.makedirs(output_dir, exist_ok=True)
output_filename = os.path.basename(input_path).replace("tokenization-", "word-repair-")
output_path = os.path.join(output_dir, output_filename)

# Load custom kamus dari file JSON
with open(kamus_path, 'r', encoding='utf-8') as f:
    custom_kamus = json.load(f)

# Inisialisasi spellchecker
spell = SpellChecker(language=None)
spell.word_frequency.load_words(custom_kamus)

# Load data
with open(input_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

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

# Simpan hasilnya
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(repaired_data, f, indent=2, ensure_ascii=False)

print("✅ Perbaikan selesai.")
print(f"Hasil disimpan di: {output_path}")