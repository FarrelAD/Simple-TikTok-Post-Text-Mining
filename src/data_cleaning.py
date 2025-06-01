import json
from pathlib import Path
import questionary
import re

from constants import TIMESTAMP, CASE_FOLDING_OUTPUT_DIR, DATA_CLEANING_OUTPUT_DIR


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

def main() -> None:
    case_folding_files = [str(f) for f in Path(CASE_FOLDING_OUTPUT_DIR).iterdir() if f.is_file()]
    
    selected_file: str = questionary.select("Select case folding file", choices=case_folding_files).ask()
    
    print(f"Selected file: {selected_file}")
    
    with open(selected_file, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    print("\nPreview top 5 case folding data")
    for i in range(5):
        print(f"- {data[i]}")
    
    print(f"\nData cleaning is start to process")
    for i in range(len(data)):
        data[i] = clean_text_data(data[i])
        
    print(f"\nPreview result from data cleaning")
    for i in range(5):
        print(f"- {data[i]}")
        
    print("\nConvert list of string to JSON file")
    output_file = DATA_CLEANING_OUTPUT_DIR / f"data-cleaning-{TIMESTAMP}.json"
    
    try:
        with open(output_file, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False)
        print("\nList of string successfully convert to JSON file!")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    


if __name__ == '__main__':
    main()