import json
from pathlib import Path
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
import questionary

from constants import TIMESTAMP, WORD_REPAIR_OUTPUT_DIR, STOPWORD_OUTPUT_DIR
from helpers.io import export_data_to_json

def main() -> None:
    word_repair_files = [str(f) for f in Path(WORD_REPAIR_OUTPUT_DIR).iterdir() if f.is_file()]
    
    selected_file: str = questionary.select("Select word repair file", choices=word_repair_files).ask()
    
    print(f"Selected file: {selected_file}")
    
    with open(selected_file, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    print("\nPreview top 5 word repair data")
    for i in range(5):
        print(f"- {data[i]}")
    
    
    print(f"\nData cleaning is start to process")
    factory = StopWordRemoverFactory()
    stopwords = set(factory.get_stop_words())
    
    cleaned_text = []
    
    for item in data:
        new_list = []
        for word in item:
            if word not in stopwords:
                new_list.append(word)
        
        cleaned_text.append(new_list)
    
    
    print(f"\nPreview result from stopword removal")
    for i in range(5):
        print(f"- {cleaned_text[i]}")

    
    output_file = STOPWORD_OUTPUT_DIR / f"stopword-removal-{TIMESTAMP}.json"
    export_data_to_json(data=cleaned_text, output_file=output_file)

if __name__ == '__main__':
    main()