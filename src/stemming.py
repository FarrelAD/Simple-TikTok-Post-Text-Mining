import pandas as pd
from pathlib import Path
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import questionary

from constants import TIMESTAMP, DATASET_FILE_PATH, STEMMING_OUTPUT_DIR, STOPWORD_OUTPUT_DIR, DATA_CLEANING_OUTPUT_DIR, CASE_FOLDING_OUTPUT_DIR, WORD_REPAIR_OUTPUT_DIR, TOKENIZATION_OUTPUT_DIR

factory = StemmerFactory()
stemmer = factory.create_stemmer()

def main(prev_process: str = None):
    print("\nStemming is starting")
    
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
        sources_files = [str(f) for f in Path(SOURCE_DIR).iterdir() if f.is_file()]
        
        selected_file: str = questionary.select(f"Select {prev_process} file", choices=sources_files).ask()
        
        print(f"Selected file: {selected_file}")
        source_df = pd.read_csv(SOURCE_DIR / selected_file)
    else:
        selected_file = DATASET_FILE_PATH
        source_df = pd.read_csv(selected_file)
    
    
    print("\nPreview top 20 stemming data")
    print(source_df.head(20))

    print("\nData cleaning is start to process")
    source_df['text'] = source_df['text'].apply(lambda words: stemmer.stem(words))

    print("\nPreview result from stemming:")
    print(source_df.head(20))
    
    print("\nConverting result from pandas data frame to CSV file")
    try:
        output_file_name = STEMMING_OUTPUT_DIR / f"stemming_{TIMESTAMP}.csv"
        source_df.to_csv(output_file_name, index=False)
        print(f"Stemming CSV file successfully exported as {output_file_name}")
    except Exception as e:
        print("An error occurred while saving the CSV file:", e)
    
    print("Stemming process is done!")

if __name__ == "__main__":
    main(prev_process="Stopword removal")
