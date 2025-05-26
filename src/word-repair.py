import json
import os
from pathlib import Path
import questionary
from constants import TOKENIZATION_OUTPUT_DIR, WORD_REPAIR_OUTPUT_DIR, DICTIONARY_PATH 
from rapidfuzz import process, fuzz

# List semua file hasil tokenisasi
input_path_files = [str(f) for f in Path(TOKENIZATION_OUTPUT_DIR).iterdir() if f.is_file()]

# Pilih file
selected_file: str = questionary.select("Select tokenization file", choices=input_path_files).ask()

# Path kamus dan output
kamus_path = DICTIONARY_PATH / "custom-kamus.json"
output_dir = WORD_REPAIR_OUTPUT_DIR

# Buat folder output jika belum ada
os.makedirs(output_dir, exist_ok=True)

# Buat nama file output dari file yang dipilih
output_filename = os.path.basename(selected_file).replace("tokenization-", "word-repair-")
output_path = os.path.join(output_dir, output_filename)

# Load custom kamus dari file JSON
with open(kamus_path, 'r', encoding='utf-8') as f:
    custom_kamus = json.load(f)

# Siapkan daftar kata dari kamus
kamus_kata = set(custom_kamus)  # gunakan set untuk pencarian cepat

# Load data tokenisasi
with open(selected_file, 'r', encoding='utf-8') as file:
    data = json.load(file)

# Fungsi koreksi menggunakan RapidFuzz
# custom_kamus sekarang adalah dict, contoh: { "gw": "saya", "elo": "kamu", ... }

# Jangan konversi ke set, biarkan tetap dict
# custom_kamus = {"gue": "saya", ...} sudah dari file JSON

def koreksi_kata(kata, kamus_dict):
    return kamus_dict.get(kata, kata)

# Perbaikan
repaired_data = []
for kalimat in data:
    hasil = [koreksi_kata(kata, custom_kamus) for kata in kalimat]
    repaired_data.append(hasil)

# Proses perbaikan
repaired_data = []
for kalimat in data:
    hasil = [koreksi_kata(kata, custom_kamus) for kata in kalimat]
    repaired_data.append(hasil)

# Simpan hasil perbaikan
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(repaired_data, f, indent=2, ensure_ascii=False)

print("✅ Perbaikan selesai.")
print(f"Hasil disimpan di: {output_path}")
