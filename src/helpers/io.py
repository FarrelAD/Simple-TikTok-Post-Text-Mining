import json
from pathlib import Path


def read_json_file(
        file_path: Path, 
        encoding: str = 'utf-8'
    ) -> any:
    if not file_path.exists():
        print("ERROR: File not found!")
        return []
        
    with open(file_path, 'r', encoding=encoding) as file:
        data = json.load(file)
    
    return data

def export_data_to_json(
        data: list,
        output_file: Path
    ) -> None:
    print("\nConvert data to JSON file")
    
    try:
        with open(output_file, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False)
        print("\nData successfully convert to JSON file!")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")