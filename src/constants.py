from datetime import datetime
from pathlib import Path

BASE_PATH                   = Path(__file__).parent.parent

DATASET_PATH                = BASE_PATH / "data" / "dataset_tiktok-comments-scraper_2025-05-25_06-21-26-775.json"

DICTIONARY_PATH             = BASE_PATH / "data" / "dictionary" / "custom-kamus.json"

CASE_FOLDING_OUTPUT_DIR     = BASE_PATH / "data" / "preprocessed-data" / "case-folding"
DATA_CLEANING_OUTPUT_DIR    = BASE_PATH / "data" / "preprocessed-data" / "data-cleaning"
TOKENIZATION_OUTPUT_DIR     = BASE_PATH / "data" / "preprocessed-data" / "tokenization"
STEMMING_OUTPUT_DIR         = BASE_PATH / "data" / "preprocessed-data" / "stemming"
TOKENIZATION_FILE           = BASE_PATH / "data" / "preprocessed-data" / "tokenization" 
WORD_REPAIR_OUTPUT_DIR      = BASE_PATH / "data" / "preprocessed-data" / "word-repair"
STOPWORD_OUTPUT_DIR         = BASE_PATH / "data" / "preprocessed-data" / "stopword-removal"

VECTORIZATION_OUTPUT_DIR    = BASE_PATH / "data" / "vectorization"

TIMESTAMP                   = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
