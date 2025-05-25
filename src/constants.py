from datetime import datetime
from pathlib import Path

BASE_PATH                   = Path(__file__).parent.parent
DATASET_PATH                = BASE_PATH / "data" / "dataset_tiktok-comments-scraper_2025-05-25_06-21-26-775.json"
CASE_FOLDING_OUTPUT_DIR     = BASE_PATH / "data" / "preprocessed-data" / "case-folding"
DATA_CLEANING_OUTPUT_DIR    = BASE_PATH / "data" / "preprocessed-data" / "data-cleaning"
TOKENIZATION_OUTPUT_DIR     = BASE_PATH / "data" / "preprocessed-data" / "tokenization"
<<<<<<< HEAD
STEMMING_OUTPUT_DIR         = BASE_PATH / "data" / "preprocessed-data" / "stemming"
TOKENIZATION_FILE           = BASE_PATH / "data" / "preprocessed-data" / "tokenization" 

=======
WORD_REPAIR_OUTPUT_DIR      = BASE_PATH / "data" / "preprocessed-data" / "word-repair"
DICTIONARY_PATH             = BASE_PATH / "data" / "dictionary" / "custom-kamus.json"
>>>>>>> 968daac3a661418728c5caabef5b59b71710f6d3
TIMESTAMP                   = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
