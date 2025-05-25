import json
import re
import string
from typing import List, Dict, Any

def remove_urls(text: str) -> str:
    """Menghapus URL dari teks."""
    url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    return re.sub(url_pattern, '', text)

def remove_mentions(text: str) -> str:
    """Menghapus mention (@username) dari teks."""
    mention_pattern = r'@\w+'
    return re.sub(mention_pattern, '', text)

def remove_hashtags(text: str) -> str:
    """Menghapus hashtag (#tag) dari teks."""
    hashtag_pattern = r'#\w+'
    return re.sub(hashtag_pattern, '', text)

def remove_extra_whitespace(text: str) -> str:
    """Menghapus spasi berlebihan dan karakter whitespace."""
    # Hapus tab, newline, dan whitespace lainnya
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def remove_special_characters(text: str, keep_punctuation: bool = True) -> str:
    """
    Menghapus karakter khusus, dengan opsi mempertahankan tanda baca.
    
    Args:
        text (str): Teks input
        keep_punctuation (bool): Jika True, tanda baca dasar akan dipertahankan
    """
    if keep_punctuation:
        # Hanya hapus karakter non-ASCII dan beberapa karakter khusus
        text = re.sub(r'[^\w\s.,!?;:()"\'-]', '', text)
    else:
        # Hapus semua karakter kecuali huruf, angka, dan spasi
        text = re.sub(r'[^\w\s]', '', text)
    
    return text

def normalize_text(text: str) -> str:
    """
    Normalisasi teks dengan berbagai perbaikan umum.
    """
    if not isinstance(text, str):
        return str(text)
    
    # Perbaiki singkatan umum dalam bahasa Indonesia
    replacements = {
        ' yg ': ' yang ',
        ' dg ': ' dengan ',
        ' ga ': ' tidak ',
        ' gak ': ' tidak ',
        ' g ': ' tidak ',
        ' dr ': ' dari ',
        ' dri ': ' dari ',
        ' ke ': ' ke ',
        ' dgn ': ' dengan ',
        ' sbg ': ' sebagai ',
        ' utk ': ' untuk ',
        ' krn ': ' karena ',
        ' krna ': ' karena ',
        ' tp ': ' tetapi ',
        ' tpi ': ' tetapi ',
        ' smua ': ' semua ',
        ' sma ': ' sama ',
        ' bgt ': ' banget ',
        ' bgt ': ' banget ',
        ' bs ': ' bisa ',
        ' bsa ': ' bisa ',
        ' jg ': ' juga ',
        ' jga ': ' juga ',
        ' klo ': ' kalau ',
        ' kalo ': ' kalau ',
        ' gmn ': ' gimana ',
        ' gmana ': ' gimana ',
        ' msih ': ' masih ',
        ' smpai ': ' sampai ',
        ' bln ': ' bulan ',
        ' thn ': ' tahun ',
        ' rb ': ' ribu '
    }
    
    # Terapkan replacements
    for old, new in replacements.items():
        text = text.replace(old, new)
    
    return text

def remove_numbers(text: str) -> str:
    """Menghapus angka dari teks."""
    return re.sub(r'\d+', '', text)

def remove_single_characters(text: str) -> str:
    """Menghapus karakter tunggal yang terpisah."""
    return re.sub(r'\b\w\b', '', text)

def clean_text_comprehensive(text: str, 
                           remove_urls_flag: bool = True,
                           remove_mentions_flag: bool = True, 
                           remove_hashtags_flag: bool = True,
                           remove_numbers_flag: bool = False,
                           normalize_flag: bool = True,
                           remove_special_chars: bool = True,
                           keep_punctuation: bool = True) -> str:
    """
    Pembersihan teks komprehensif dengan berbagai opsi.
    
    Args:
        text (str): Teks yang akan dibersihkan
        remove_urls_flag (bool): Hapus URL
        remove_mentions_flag (bool): Hapus mention
        remove_hashtags_flag (bool): Hapus hashtag  
        remove_numbers_flag (bool): Hapus angka
        normalize_flag (bool): Normalisasi singkatan
        remove_special_chars (bool): Hapus karakter khusus
        keep_punctuation (bool): Pertahankan tanda baca
        
    Returns:
        str: Teks yang sudah dibersihkan
    """
    if not isinstance(text, str) or not text.strip():
        return ""
    
    # Proses pembersihan berurutan
    if remove_urls_flag:
        text = remove_urls(text)
    
    if remove_mentions_flag:
        text = remove_mentions(text)
        
    if remove_hashtags_flag:
        text = remove_hashtags(text)
    
    if normalize_flag:
        text = normalize_text(text)
    
    if remove_special_chars:
        text = remove_special_characters(text, keep_punctuation)
    
    if remove_numbers_flag:
        text = remove_numbers(text)
    
    # Bersihkan spasi berlebihan
    text = remove_extra_whitespace(text)
    
    # Hapus karakter tunggal
    text = remove_single_characters(text)
    
    # Bersihkan spasi lagi setelah penghapusan karakter tunggal
    text = remove_extra_whitespace(text)
    
    return text

def clean_single_comment(comment_data: Dict[str, Any], **cleaning_options) -> Dict[str, Any]:
    """
    Membersihkan data dalam satu komentar.
    
    Args:
        comment_data (dict): Data komentar individual
        **cleaning_options: Opsi pembersihan untuk clean_text_comprehensive
        
    Returns:
        dict: Data komentar yang sudah dibersihkan
    """
    cleaned_comment = comment_data.copy()
    
    # Bersihkan field text
    if 'text' in cleaned_comment and cleaned_comment['text']:
        cleaned_comment['text'] = clean_text_comprehensive(
            cleaned_comment['text'], **cleaning_options
        )
        
        # Hapus komentar yang kosong setelah pembersihan
        if not cleaned_comment['text'].strip():
            cleaned_comment['text'] = ""
    
    return cleaned_comment

def clean_comments_data(comments: List[Dict[str, Any]], 
                       remove_empty: bool = True,
                       **cleaning_options) -> List[Dict[str, Any]]:
    """
    Membersihkan semua komentar dalam list.
    
    Args:
        comments (list): List berisi data komentar
        remove_empty (bool): Hapus komentar dengan teks kosong
        **cleaning_options: Opsi pembersihan
        
    Returns:
        list: List komentar yang sudah dibersihkan
    """
    cleaned_comments = []
    
    for comment in comments:
        cleaned_comment = clean_single_comment(comment, **cleaning_options)
        
        # Tambahkan hanya jika teks tidak kosong (jika remove_empty=True)
        if remove_empty:
            if cleaned_comment.get('text', '').strip():
                cleaned_comments.append(cleaned_comment)
        else:
            cleaned_comments.append(cleaned_comment)
    
    return cleaned_comments

def process_large_json_file(input_file: str, 
                           output_file: str = None,
                           batch_size: int = 1000,
                           **cleaning_options) -> List[Dict[str, Any]]:
    """
    Memproses file JSON besar dengan batch processing untuk efisiensi memori.
    
    Args:
        input_file (str): Path file input JSON
        output_file (str): Path file output JSON
        batch_size (int): Ukuran batch untuk processing
        **cleaning_options: Opsi pembersihan
        
    Returns:
        list: Data yang sudah diproses (atau kosong jika file sangat besar)
    """
    try:
        print(f"Memuat data dari: {input_file}")
        
        # Baca file JSON
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        total_comments = len(data)
        print(f"Total komentar: {total_comments}")
        
        cleaned_data = []
        
        # Proses dalam batch
        for i in range(0, total_comments, batch_size):
            batch = data[i:i + batch_size]
            print(f"Memproses batch {i//batch_size + 1}/{(total_comments-1)//batch_size + 1}")
            
            cleaned_batch = clean_comments_data(batch, **cleaning_options)
            cleaned_data.extend(cleaned_batch)
        
        print(f"Pembersihan selesai. Komentar yang tersisa: {len(cleaned_data)}")
        
        # Simpan hasil jika output_file diberikan
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(cleaned_data, f, ensure_ascii=False, indent=2)
            print(f"Hasil disimpan ke: {output_file}")
        
        return cleaned_data
        
    except FileNotFoundError:
        print(f"File {input_file} tidak ditemukan!")
        return []
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return []
    except MemoryError:
        print("File terlalu besar untuk dimuat ke memori. Gunakan streaming processing.")
        return []
    except Exception as e:
        print(f"Error: {e}")
        return []

# Contoh penggunaan
if __name__ == "__main__":
    # Path file Anda
    input_path = "Simple-Instagram-Post-Text-Mining/data/dataset_tiktok-comments-scraper_2025-05-25_06-21-26-775.json"
    output_path = "Simple-Instagram-Post-Text-Mining/data/cleaned_dataset.json"
    
    # Opsi pembersihan
    cleaning_config = {
        'remove_urls_flag': True,
        'remove_mentions_flag': True, 
        'remove_hashtags_flag': False,  # Mungkin hashtag penting untuk analisis
        'remove_numbers_flag': False,   # Angka mungkin penting (harga, jumlah, dll)
        'normalize_flag': True,
        'remove_special_chars': True,
        'keep_punctuation': True
    }
    
    # Proses file
    result = process_large_json_file(
        input_path, 
        output_path,
        batch_size=500,  # Sesuaikan dengan kapasitas memori
        **cleaning_config
    )
    
    # Tampilkan contoh hasil jika data tidak terlalu besar
    if result and len(result) > 0:
        print("\n=== CONTOH HASIL PEMBERSIHAN ===")
        for i, comment in enumerate(result[:3]):  # Tampilkan 3 contoh pertama
            print(f"Komentar {i+1}:")
            print(f"Text: {comment.get('text', 'N/A')}")
            print(f"Author: {comment.get('uniqueId', 'N/A')}")
            print("-" * 50)