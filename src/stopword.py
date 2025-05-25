import json
import os

# Path - Diperbaiki untuk konsistensi
input_path = r"D:\KULIAH\SEMESTER4\AI\Simple-TikTok-Post-Text-Mining\data\preprocessed-data\word-repair\word-repair-2025-05-25_17-20-50.json"
stopwords_path = r"D:\KULIAH\SEMESTER4\AI\Simple-TikTok-Post-Text-Mining\data\dictionary\custom-kamus.json"  # Perbaiki path
output_dir = r"D:\KULIAH\SEMESTER4\AI\Simple-TikTok-Post-Text-Mining\data\preprocessed-data\stopword-removal"  # Nama folder konsisten

# Buat folder output kalau belum ada
os.makedirs(output_dir, exist_ok=True)
output_filename = os.path.basename(input_path).replace("word-repair-", "stopword-removal-")  # Perbaiki replace
output_path = os.path.join(output_dir, output_filename)

# Cek apakah file input ada
if not os.path.exists(input_path):
    print(f"❌ Error: File input tidak ditemukan: {input_path}")
    exit(1)

# Cek apakah file stopwords ada
if not os.path.exists(stopwords_path):
    print(f"❌ Error: File stopwords tidak ditemukan: {stopwords_path}")
    exit(1)

try:
    # Load stopwords dari file JSON
    with open(stopwords_path, 'r', encoding='utf-8') as f:
        stopwords_data = json.load(f)

    # Konversi stopwords ke set untuk pencarian yang lebih cepat
    if isinstance(stopwords_data, list):
        stopwords_set = set(word.lower() for word in stopwords_data)  # Konversi ke lowercase
    elif isinstance(stopwords_data, dict):
        stopwords_set = set(word.lower() for word in stopwords_data.keys())  # Konversi ke lowercase
    else:
        raise ValueError("Format stopwords tidak didukung. Harus berupa list atau dict.")

    print(f"📚 Loaded {len(stopwords_set)} stopwords")

    # Load data tokenisasi
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print(f"📄 Loaded {len(data)} kalimat untuk diproses")

    # Hapus stop words
    filtered_data = []
    removed_words_count = 0
    total_words_count = 0

    for kalimat in data:
        hasil = []
        for kata in kalimat:
            total_words_count += 1
            # Cek apakah kata bukan stopword (case insensitive)
            if kata.lower() not in stopwords_set:
                hasil.append(kata)
            else:
                removed_words_count += 1
        
        # Hanya tambahkan kalimat jika masih ada kata setelah filtering
        if hasil:
            filtered_data.append(hasil)

    # Simpan hasilnya
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(filtered_data, f, indent=2, ensure_ascii=False)

    # Statistik
    remaining_words = total_words_count - removed_words_count
    print("\n✅ Stop word removal selesai.")
    print(f"📊 Statistik:")
    print(f"   - Total kata awal: {total_words_count:,}")
    print(f"   - Stop words dihapus: {removed_words_count:,}")
    print(f"   - Kata tersisa: {remaining_words:,}")
    if total_words_count > 0:
        print(f"   - Persentase dihapus: {removed_words_count/total_words_count*100:.1f}%")
    print(f"   - Kalimat awal: {len(data):,}")
    print(f"   - Kalimat tersisa: {len(filtered_data):,}")
    print(f"📁 Hasil disimpan di: {output_path}")

except FileNotFoundError as e:
    print(f"❌ Error: File tidak ditemukan - {e}")
except json.JSONDecodeError as e:
    print(f"❌ Error: Format JSON tidak valid - {e}")
except Exception as e:
    print(f"❌ Error: {e}")