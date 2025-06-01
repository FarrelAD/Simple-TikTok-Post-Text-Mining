import pandas as pd
from pathlib import Path
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory, ArrayDictionary, StopWordRemover
import questionary

from constants import TIMESTAMP, WORD_REPAIR_OUTPUT_DIR, STOPWORD_OUTPUT_DIR, STEMMING_OUTPUT_DIR, DATA_CLEANING_OUTPUT_DIR, CASE_FOLDING_OUTPUT_DIR, TOKENIZATION_OUTPUT_DIR

def main(prev_process: str) -> None:
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
        
    source_files = [str(f) for f in Path(SOURCE_DIR).iterdir() if f.is_file()]
    
    selected_file: str = questionary.select(f"Select {prev_process} file", choices=source_files).ask()
    
    print(f"Selected file: {selected_file}")
    
    source_df = pd.read_csv(SOURCE_DIR / selected_file)
    
    print("Preview top 20 data")
    print(source_df.head(20))
    
    print(f"\nStopword removal is starting to process")
    
    more_stop_words = []
    
    stop_words = StopWordRemoverFactory().get_stop_words()
    stop_words.extend(more_stop_words)
    
    new_array = ArrayDictionary(stop_words)
    stop_words_remover_new = StopWordRemover(new_array)
    
    def stopword(text: str) -> str:
        return stop_words_remover_new.remove(text)
    
    source_df['text'] = source_df["text"].apply(lambda x: stopword(x))
    
    
    print(f"\nPreview result from stopword removal")
    print(source_df.head(20))

    
    print("\nConverting result from pandas data frame to CSV file")
    try:
        output_file_name = STOPWORD_OUTPUT_DIR / f"stopword_removal_{TIMESTAMP}.csv"
        source_df.to_csv(output_file_name, index=False)
        print(f"Stopword removal CSV file successfully exported as {output_file_name}")
    except Exception as e:
        print("An error occurred while saving the CSV file:", e)
    
    print("Stopword removal process is done!")

if __name__ == '__main__':
    main(prev_process="Data cleaning")