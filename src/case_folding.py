import json
from constant import BASE_PATH, TIMESTAMP

DATASET_PATH = BASE_PATH / "data" / "dataset_tiktok-comments-scraper_2025-05-25_06-21-26-775.json"
CASE_FOLDING_OUTPUT_DIR = BASE_PATH / "data" / "preprocessed-data"

def main():
    print(f"dataset: {DATASET_PATH}")
    if not DATASET_PATH.exists():
        print("Dataset is not found!")
        return
    
    with DATASET_PATH.open('r', encoding='utf-8') as file:
        data = json.load(file)
    
    comments = [item['text'] for item in data]
    
    print("Preview top 5 raw data")
    for i in range(5):
        print(f"- {comments[i]}")
        
    for i in range(len(comments)):
        comments[i] = comments[i].lower()
    
    print("\nPreview result of case-folding (lowercasing)")
    for i in range(5):
        print(f"- {comments[i]}")
    
    print("\nConvert list of string to JSON file")
    output_file = CASE_FOLDING_OUTPUT_DIR / f"1-case-folding-{TIMESTAMP}.json"
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(comments, file, ensure_ascii=False)

if __name__ == "__main__":
    main()