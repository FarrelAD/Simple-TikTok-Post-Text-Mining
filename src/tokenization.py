from pathlib import Path
import pandas as pd
import questionary

from constants import TIMESTAMP, DATASET_FILE_PATH, DATA_CLEANING_OUTPUT_DIR, TOKENIZATION_OUTPUT_DIR, CASE_FOLDING_OUTPUT_DIR, STEMMING_OUTPUT_DIR, STOPWORD_OUTPUT_DIR, WORD_REPAIR_OUTPUT_DIR

def main(prev_process: str) -> None:
    print("\nTokenization is starting")
    
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
        
        selected_file: str = questionary.select(f"Select {prev_process.casefold()} file", choices=source_files).ask()
        
        print(f"Selected file: {selected_file}")
        
        source_df = pd.read_csv(SOURCE_DIR / selected_file)
    else:
        selected_file = DATASET_FILE_PATH
        source_df = pd.read_csv(selected_file)
    
    
    print("\nPreview top 20 tokenization data")
    print(source_df.head(20))
    
    print("\nTokenization is start to process")
    source_df['text'] = source_df['text'].apply(lambda x: x.split())
        
    print("\nPreview result from tokenization")
    print(source_df.head(20))
    
    print("\nConverting result from pandas data frame to CSV file")
    try:
        output_file_name = TOKENIZATION_OUTPUT_DIR / f"tokenization_{TIMESTAMP}.csv"
        source_df.to_csv(output_file_name, index=False)
        print(f"Tokenization CSV file successfully exported as {output_file_name}")
    except Exception as e:
        print("An error occurred while saving the CSV file:", e)
    
    print("Tokenization process is done!")


if __name__ == '__main__':
    main(prev_process="Data cleaning")