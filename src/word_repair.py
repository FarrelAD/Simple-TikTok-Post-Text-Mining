import pandas as pd
from pathlib import Path
import re
import questionary
from constants import TIMESTAMP, DATASET_FILE_PATH, TOKENIZATION_OUTPUT_DIR, WORD_REPAIR_OUTPUT_DIR, DATA_CLEANING_OUTPUT_DIR, STOPWORD_OUTPUT_DIR, STEMMING_OUTPUT_DIR, CASE_FOLDING_OUTPUT_DIR, DICTIONARY_PATH
from rapidfuzz import process, fuzz

def main(prev_process: str = None) -> None:
    print("\nWord repair is starting")
    
    SOURCE_DIR = None
    
    if prev_process == "Data cleaning":
        SOURCE_DIR = DATA_CLEANING_OUTPUT_DIR
    elif prev_process == "Stopword removal":
        SOURCE_DIR = STOPWORD_OUTPUT_DIR
    elif prev_process == "Case folding":
        SOURCE_DIR = CASE_FOLDING_OUTPUT_DIR
    elif prev_process == "Word repair":
        SOURCE_DIR = WORD_REPAIR_OUTPUT_DIR
    elif prev_process == "Tokenizing":
        SOURCE_DIR = TOKENIZATION_OUTPUT_DIR
    elif prev_process == "Stemming":
        SOURCE_DIR = STEMMING_OUTPUT_DIR
    else:
        SOURCE_DIR = DATASET_FILE_PATH
    
    if SOURCE_DIR != DATASET_FILE_PATH:
        source_files = [str(f) for f in Path(SOURCE_DIR).iterdir() if f.is_file()]
        
        selected_file: str = questionary.select(f"Select {prev_process} file", choices=source_files).ask()
        
        print(f"Selected file: {selected_file}")
        source_df = pd.read_csv(SOURCE_DIR / selected_file)
    else:
        selected_file = DATASET_FILE_PATH
        source_df = pd.read_csv(selected_file)
    
    
    print("Preview top 20 data")
    print(source_df.head(20))
    
    print("\nLoad dictionary")
    dictionary_df = pd.read_csv(DICTIONARY_PATH / "custom_dictionary.csv")

    # Fungsi koreksi menggunakan RapidFuzz
    # custom_kamus sekarang adalah dict, contoh: { "gw": "saya", "elo": "kamu", ... }

    # Jangan konversi ke set, biarkan tetap dict
    # custom_kamus = {"gue": "saya", ...} sudah dari file JSON

    dictionary_dict = dict(zip(dictionary_df['informal'], dictionary_df['formal']))
    
    pattern = re.compile(r'\b(' + '|'.join(map(re.escape, dictionary_dict.keys())) + r')\b')

    # def word_correction(word: str):
    #     return dictionary_dict.get(key=word, default=word)

    # source_df['text'] = source_df['text'].apply(lambda sentence: [word_correction(word) for word in sentence])
    source_df['text'] = source_df['text'].str.replace(pattern, lambda m: dictionary_dict[m.group(0)], regex=True)

    print(f"\nPreview result from stopword removal")
    print(source_df.head(20))

    
    print("\nConverting result from pandas data frame to CSV file")
    try:
        output_file_name = WORD_REPAIR_OUTPUT_DIR / f"word_repair_{TIMESTAMP}.csv"
        source_df.to_csv(output_file_name, index=False)
        print(f"Word repair CSV file successfully exported as {output_file_name}")
    except Exception as e:
        print("An error occurred while saving the CSV file:", e)
    
    print("Word repair process is done!")

if __name__ == "__main__":
    main(prev_process="Data cleaning")