from datetime import datetime
from pathlib import Path

BASE_PATH                   = Path(__file__).parent.parent

DATA_DIR                    = BASE_PATH / "data"

DATASET_FILE_PATH           = DATA_DIR / "dataset" / "tiktok_comments_text.csv"

DICTIONARY_PATH             = DATA_DIR / "dictionary"

PREPROCESSED_DATA_DIR       = DATA_DIR / "preprocessed-data"

CASE_FOLDING_OUTPUT_DIR     = PREPROCESSED_DATA_DIR / "case-folding"
DATA_CLEANING_OUTPUT_DIR    = PREPROCESSED_DATA_DIR / "data-cleaning"
TOKENIZATION_OUTPUT_DIR     = PREPROCESSED_DATA_DIR / "tokenization"
STEMMING_OUTPUT_DIR         = PREPROCESSED_DATA_DIR / "stemming"
TOKENIZATION_OUTPUT_DIR     = PREPROCESSED_DATA_DIR / "tokenization" 
WORD_REPAIR_OUTPUT_DIR      = PREPROCESSED_DATA_DIR / "word-repair"
STOPWORD_OUTPUT_DIR         = PREPROCESSED_DATA_DIR / "stopword-removal"

VECTORIZATION_DIR          = BASE_PATH / "data" / "vectorization"

IMG_DIR                     = BASE_PATH / "img"


############################

TIMESTAMP                   = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
