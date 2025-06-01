import pandas as pd
import questionary
from pathlib import Path

from constants import TIMESTAMP, DATASET_FILE_PATH, CASE_FOLDING_OUTPUT_DIR, DATA_CLEANING_OUTPUT_DIR, STOPWORD_OUTPUT_DIR, WORD_REPAIR_OUTPUT_DIR, TOKENIZATION_OUTPUT_DIR, STEMMING_OUTPUT_DIR

def main(prev_process: str):
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
        SOURCE_DIR = None
        
    
    sources_files = [str(f) for f in Path(SOURCE_DIR).iterdir() if f.is_file()]
    
    selected_file: str = questionary.select(f"Select {prev_process} file", choices=sources_files).ask()
    
    print(f"Selected file: {selected_file}")
    
    source_df = pd.read_csv(SOURCE_DIR / selected_file)
    
    print("Preview top 20 data")
    print(source_df.head(10))
    
    source_df['text'] = source_df['text'].str.lower()
    
    print("\nPreview result from case-folding (lowercasing)")
    print(source_df.head(20))
    
    print("\nConverting result from pandas data frame to CSV file")
    try:
        output_file_name = CASE_FOLDING_OUTPUT_DIR / f"case_folding_{TIMESTAMP}.csv"
        source_df.to_csv(output_file_name, index=False)
        print(f"Case folding CSV file successfully exported as {output_file_name}")
    except Exception as e:
        print("An error occurred while saving the CSV file:", e)
    
    print("Case folding process is done!")
    
if __name__ == "__main__":
    main()