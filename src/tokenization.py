import json
from pathlib import Path
import questionary

from constants import TIMESTAMP, DATA_CLEANING_OUTPUT_DIR, TOKENIZATION_OUTPUT_DIR

def main() -> None:
    data_cleaning_files = [str(f) for f in Path(DATA_CLEANING_OUTPUT_DIR).iterdir() if f.is_file()]
    
    selected_file: str = questionary.select("Select data cleaning file", choices=data_cleaning_files).ask()
    
    print(f"Selected file: {selected_file}")
    
    with open(selected_file, 'r', encoding='utf-8') as file:
        data = json.load(file)
        
    print("\nPreview top 5 case folding data")
    for i in range(5):
        print(f"- {data[i]}")
    
    print(f"\nTokenization is start to process")
    for i in range(len(data)):
        data[i] = data[i].split()
    
    print(f"\nPreview result from tokenization")
    for i in range(5):
        print(f"- {data[i]}")
    
    print("\nConvert list of string to JSON file")
    output_file = TOKENIZATION_OUTPUT_DIR / f"tokenization-{TIMESTAMP}.json"
    
    try:
        with open(output_file, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False)
        print("\nList of string successfully convert to JSON file!")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == '__main__':
    main()