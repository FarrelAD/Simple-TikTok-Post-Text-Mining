import json
from pathlib import Path
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import questionary

from constants import TIMESTAMP, STEMMING_OUTPUT_DIR, STOPWORD_OUTPUT_DIR
from helpers.io import export_data_to_json

factory = StemmerFactory()
stemmer = factory.create_stemmer()

def main():
    stopword_files = [str(f) for f in Path(STOPWORD_OUTPUT_DIR).iterdir() if f.is_file()]

    if not stopword_files:
        print("No file found in :", STOPWORD_OUTPUT_DIR)
        return

    selected_file = questionary.select(
        "Select the file output from stopword removal to process in stemming",
        choices=stopword_files
    ).ask()

    print(f"Selected file: {selected_file}")

    with open(selected_file, "r", encoding="utf-8") as file:
        data = json.load(file)
    
    print("\nPreview top 5 stopword removal data")
    for i in range(5):
        print(f"- {data[i]}")

    stemmed_comments = []
    
    for item in data:
        new_list = []
        for word in item:
            new_list.append(stemmer.stem(word))
        
        stemmed_comments.append(new_list)

    print("\nPreview result from stemming:")
    for i in range(min(5, len(stemmed_comments))):
        print(f"- {stemmed_comments[i]}")
    
    output_file = STEMMING_OUTPUT_DIR / f"stemming-{TIMESTAMP}.json"
    export_data_to_json(data=stemmed_comments, output_file=output_file)

if __name__ == "__main__":
    main()
