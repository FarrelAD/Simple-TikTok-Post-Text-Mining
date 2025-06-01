import json
import csv
import pandas as pd
from pathlib import Path

def extract_text_to_csv(json_file_path, output_csv_path='extracted_text.csv'):
    """
    Mengambil field 'text' dari file JSON dan menyimpannya ke file CSV
    
    Args:
        json_file_path (str): Path ke file JSON
        output_csv_path (str): Path untuk output file CSV
    """
    
    try:
        # Membaca file JSON
        with open(json_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        print(f"Data berhasil dibaca. Total {len(data)} record ditemukan.")
        
        # Mengekstrak field 'text' dari setiap item
        text_data = []
        for i, item in enumerate(data):
            if 'text' in item:
                text_data.append({
                    'index': i + 1,
                    'text': item['text']
                })
            else:
                print(f"Warning: Item ke-{i+1} tidak memiliki field 'text'")
        
        print(f"Berhasil mengekstrak {len(text_data)} text.")
        
        # Menyimpan ke CSV menggunakan pandas
        df = pd.DataFrame(text_data)
        df.to_csv(output_csv_path, index=False, encoding='utf-8')
        
        print(f"Data berhasil disimpan ke '{output_csv_path}'")
        
        # Menampilkan preview 5 baris pertama
        print("\nPreview 5 baris pertama:")
        print(df.head().to_string(index=False))
        
        return df
        
    except FileNotFoundError:
        print(f"Error: File '{json_file_path}' tidak ditemukan.")
        return None
    except json.JSONDecodeError:
        print(f"Error: File '{json_file_path}' bukan format JSON yang valid.")
        return None
    except Exception as e:
        print(f"Error: {str(e)}")
        return None

# Alternative function menggunakan CSV writer biasa (tanpa pandas)
def extract_text_to_csv_basic(json_file_path, output_csv_path='extracted_text.csv'):
    """
    Versi alternatif tanpa menggunakan pandas
    """
    
    try:
        # Membaca file JSON
        with open(json_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        print(f"Data berhasil dibaca. Total {len(data)} record ditemukan.")
        
        # Menyimpan ke CSV
        with open(output_csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            
            # Header
            writer.writerow(['index', 'text'])
            
            # Data
            text_count = 0
            for i, item in enumerate(data):
                if 'text' in item:
                    writer.writerow([i + 1, item['text']])
                    text_count += 1
                else:
                    print(f"Warning: Item ke-{i+1} tidak memiliki field 'text'")
        
        print(f"Berhasil mengekstrak {text_count} text ke '{output_csv_path}'")
        
    except Exception as e:
        print(f"Error: {str(e)}")

# Penggunaan
if __name__ == "__main__":
    # Path ke file JSON Anda
    json_file = r"data\dataset_tiktok-comments-scraper_2025-05-25_06-21-26-775.json"
    
    # Path output CSV
    output_file = r"data/CSV/tiktok_comments_text.csv"
    
    # Ekstrak text menggunakan pandas (direkomendasikan)
    print("=== Menggunakan Pandas ===")
    df = extract_text_to_csv(json_file, output_file)
    
    # Atau menggunakan versi basic tanpa pandas
    # print("=== Menggunakan CSV Writer Basic ===")
    # extract_text_to_csv_basic(json_file, "tiktok_comments_text_basic.csv")
    
    # Statistik tambahan jika berhasil
    if df is not None:
        print(f"\n=== Statistik ===")
        print(f"Total komentar: {len(df)}")
        print(f"Rata-rata panjang komentar: {df['text'].str.len().mean():.1f} karakter")
        print(f"Komentar terpanjang: {df['text'].str.len().max()} karakter")
        print(f"Komentar terpendek: {df['text'].str.len().min()} karakter")