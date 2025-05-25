import json
import re
from typing import List, Dict, Any

def case_folding(text: str) -> str:
    """
    Melakukan case folding pada teks dengan mengubah semua huruf menjadi lowercase
    dan menangani beberapa normalisasi dasar.
    
    Args:
        text (str): Teks yang akan di-case folding
        
    Returns:
        str: Teks hasil case folding
    """
    if not isinstance(text, str):
        return str(text).lower()
    
    # Ubah ke lowercase
    text = text.lower()
    
    # Normalisasi beberapa karakter khusus
    text = text.replace('–', '-')  # em dash ke hyphen
    text = text.replace('—', '-')  # en dash ke hyphen
    text = text.replace(''', "'")  # smart quote ke regular quote
    text = text.replace(''', "'")
    text = text.replace('"', '"')  # smart double quote
    text = text.replace('"', '"')
    
    return text

def process_single_comment(comment_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Melakukan case folding pada field 'text' dalam satu komentar.
    
    Args:
        comment_data (dict): Data komentar individual
        
    Returns:
        dict: Data komentar dengan field text yang sudah di-case folding
    """
    processed_comment = comment_data.copy()
    
    # Case folding pada field text
    if 'text' in processed_comment and processed_comment['text']:
        processed_comment['text'] = case_folding(processed_comment['text'])
    
    # Case folding pada field uniqueId jika diperlukan
    if 'uniqueId' in processed_comment and processed_comment['uniqueId']:
        processed_comment['uniqueId'] = case_folding(processed_comment['uniqueId'])
    
    return processed_comment

def process_comments_case_folding(comments: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Melakukan case folding pada semua komentar dalam list.
    
    Args:
        comments (list): List berisi data komentar
        
    Returns:
        list: List komentar dengan text yang sudah di-case folding
    """
    processed_comments = []
    
    for comment in comments:
        processed_comment = process_single_comment(comment)
        processed_comments.append(processed_comment)
    
    return processed_comments

def process_large_json_case_folding(input_file: str, 
                                   output_file: str = None,
                                   batch_size: int = 1000) -> List[Dict[str, Any]]:
    """
    Memuat data JSON besar dari file, melakukan case folding dengan batch processing.
    
    Args:
        input_file (str): Path file input JSON
        output_file (str): Path file output JSON (opsional)
        batch_size (int): Ukuran batch untuk processing
        
    Returns:
        list: Data yang sudah diproses (kosong jika file terlalu besar)
    """
    try:
        print(f"Memuat data dari: {input_file}")
        
        # Baca file JSON
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        total_comments = len(data)
        print(f"Total komentar: {total_comments}")
        
        processed_data = []
        
        # Proses dalam batch untuk efisiensi memori
        for i in range(0, total_comments, batch_size):
            batch = data[i:i + batch_size]
            print(f"Memproses batch {i//batch_size + 1}/{(total_comments-1)//batch_size + 1}")
            
            processed_batch = process_comments_case_folding(batch)
            processed_data.extend(processed_batch)
        
        print(f"Case folding selesai untuk {len(processed_data)} komentar")
        
        # Simpan ke file jika output_file diberikan
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(processed_data, f, ensure_ascii=False, indent=2)
            print(f"Hasil case folding disimpan ke: {output_file}")
        
        return processed_data
        
    except FileNotFoundError:
        print(f"File {input_file} tidak ditemukan!")
        return []
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return []
    except MemoryError:
        print("File terlalu besar untuk dimuat ke memori. Pertimbangkan untuk memecah file.")
        return []
    except Exception as e:
        print(f"Error: {e}")
        return []

def load_and_process_json(input_file: str, output_file: str = None) -> List[Dict[str, Any]]:
    """
    Fungsi wrapper untuk kompatibilitas - memanggil process_large_json_case_folding.
    
    Args:
        input_file (str): Path file input JSON
        output_file (str): Path file output JSON (opsional)
        
    Returns:
        list: Data yang sudah diproses
    """
    return process_large_json_case_folding(input_file, output_file)

# Contoh penggunaan
if __name__ == "__main__":
    # Path file Anda yang besar
    input_path = "Simple-Instagram-Post-Text-Mining/data/dataset_tiktok-comments-scraper_2025-05-25_06-21-26-775.json"
    output_path = "Simple-Instagram-Post-Text-Mining/data/case_folded_dataset.json"
    
    # Proses case folding untuk file besar
    print("=== MEMULAI CASE FOLDING UNTUK FILE BESAR ===")
    result = process_large_json_case_folding(
        input_path, 
        output_path,
        batch_size=500  # Sesuaikan dengan kapasitas memori
    )
    
    # Tampilkan contoh hasil jika berhasil
    if result and len(result) > 0:
        print("\n=== CONTOH HASIL CASE FOLDING ===")
        for i, comment in enumerate(result[:3]):  # Tampilkan 3 contoh pertama
            print(f"Komentar {i+1}:")
            print(f"Text: {comment.get('text', 'N/A')}")
            print(f"UniqueId: {comment.get('uniqueId', 'N/A')}")
            print("-" * 50)
    
    # Data sampel untuk testing lokal (jika file besar tidak tersedia)
    sample_data = [{
        "videoWebUrl": "https://www.tiktok.com/@kumparan/video/7507890376124992786",
        "submittedVideoUrl": "https://www.tiktok.com/@kumparan/video/7507890376124992786",
        "input": "https://www.tiktok.com/@kumparan/video/7507890376124992786",
        "cid": "7508169969612620562",
        "createTime": 1748132065,
        "createTimeISO": "2025-05-25T00:14:25.000Z",
        "text": "Tokenku MSIH di 1530 beli dri bulan Januari Februari pas Diskon, pemakaian biasanya sebulan 150rb, kayaknya awet deh beli diskonan Januari kemarin bsa smpai 10 bln ke depan g beli token, ada yg sama?",
        "diggCount": 0,
        "likedByAuthor": False,
        "pinnedByAuthor": False,
        "repliesToId": None,
        "replyCommentTotal": 1,
        "uid": "6796934464549471234",
        "uniqueId": "NANA_arshero",
        "avatarThumbnail": "https://p16-sign-useast2a.tiktokcdn.com/tos-useast2a-avt-0068-giso/d30221e4c9af3ea1e98f4db693348075~tplv-tiktokx-cropcenter:100:100.jpg"
    }]
    
    print("\n=== TESTING DENGAN DATA SAMPEL ===")
    # Proses case folding untuk sample data
    sample_result = process_comments_case_folding(sample_data)
    
    # Tampilkan hasil sample
    for comment in sample_result:
        print(f"Original text: Tokenku MSIH di 1530 beli dri bulan Januari...")
        print(f"Case folded text: {comment['text']}")
        print(f"Original uniqueId: NANA_arshero")
        print(f"Case folded uniqueId: {comment['uniqueId']}")
        print("-" * 50)