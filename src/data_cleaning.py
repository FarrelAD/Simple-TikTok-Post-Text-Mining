import json
import pandas as pd
from pathlib import Path
import questionary
import re

from constants import TIMESTAMP, DATASET_FILE_PATH, CASE_FOLDING_OUTPUT_DIR, TOKENIZATION_OUTPUT_DIR, DATA_CLEANING_OUTPUT_DIR, STEMMING_OUTPUT_DIR, STOPWORD_OUTPUT_DIR, WORD_REPAIR_OUTPUT_DIR, VECTORIZATION_DIR


URL_PATTERN = re.compile(
    r'http[s]?://(?:[a-zA-Z0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F]{2}))+'
)
REPEATED_CHARS = re.compile(r'(.)\1+')
MENTION_PATTERN = re.compile(r'@\w+')
HASHTAG_PATTERN = re.compile(r'#\w+')
WHITESPACE_PATTERN = re.compile(r'\s+')
SPECIAL_CHAR_PATTERN = re.compile(r'[^\w\s]', flags=re.UNICODE)
SINGLE_CHAR_PATTERN = re.compile(r'\b\w\b')


def remove_urls(text: str) -> str:
    return URL_PATTERN.sub('', text)

def remove_repeated_chars(text: str):
    if text.isdigit():
        return text
    return REPEATED_CHARS.sub(r'\1', text)

def remove_mentions(text: str) -> str:
    return MENTION_PATTERN.sub('', text)

def remove_hashtags(text: str) -> str:
    return HASHTAG_PATTERN.sub('', text)

def remove_extra_whitespace(text: str) -> str:
    return WHITESPACE_PATTERN.sub(' ', text).strip()

def remove_special_characters(text: str) -> str:
    return SPECIAL_CHAR_PATTERN.sub('', text)

def remove_single_characters(text: str) -> str:
    return SINGLE_CHAR_PATTERN.sub('', text)

def clean_text_data(text: str) -> str:
    text = remove_urls(text)
    text = remove_repeated_chars(text)
    text = remove_mentions(text)
    text = remove_hashtags(text)
    text = remove_extra_whitespace(text)
    text = remove_special_characters(text)
    text = remove_single_characters(text)
    return text

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
            
    sources_files = [str(f) for f in Path(SOURCE_DIR).iterdir() if f.is_file()]
    
    selected_file: str = questionary.select(f"Select {prev_process} file", choices=sources_files).ask()
    
    print(f"Selected file: {selected_file}")
    
    source_df = pd.read_csv(SOURCE_DIR / selected_file)
    
    print("\nPreview top 20 case folding data")
    print(source_df.head(20))
    
    print("\nData cleaning is start to process")
    source_df['text'] = source_df['text'].apply(clean_text_data)
        
    print("\nPreview result from data cleaning")
    print(source_df.head(20))
    
    print("\nConverting result from pandas data frame to CSV file")
    try:
        output_file_name = DATA_CLEANING_OUTPUT_DIR / f"data_cleaning_{TIMESTAMP}.csv"
        source_df.to_csv(output_file_name, index=False)
        print(f"Data cleaning CSV file successfully exported as {output_file_name}")
    except Exception as e:
        print("An error occurred while saving the CSV file:", e)
    
    print("Data cleaning process is done!")


if __name__ == '__main__':
    main("Case folding")