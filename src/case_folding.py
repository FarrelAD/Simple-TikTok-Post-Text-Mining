import pandas as pd
from constants import TIMESTAMP, DATASET_FILE_PATH, CASE_FOLDING_OUTPUT_DIR

def main():
    print(f"dataset: {DATASET_FILE_PATH}")
    if not DATASET_FILE_PATH.exists():
        print("Dataset is not found!")
        return
    
    dataset_df = pd.read_csv(DATASET_FILE_PATH)
    
    print("Preview top 20 raw data")
    print(dataset_df.head(10))
    
    dataset_df['text'] = dataset_df['text'].str.lower()
    
    print("\nPreview result from case-folding (lowercasing)")
    print(dataset_df.head(20))
    
    output_file_name = CASE_FOLDING_OUTPUT_DIR / f"case_folding_{TIMESTAMP}.csv"
    dataset_df.to_csv(output_file_name, index=False)
    
if __name__ == "__main__":
    main()