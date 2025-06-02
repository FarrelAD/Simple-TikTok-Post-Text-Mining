import ast
import pandas as pd
import numpy as np
from pathlib import Path
import questionary
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import normalize

from constants import TIMESTAMP, STEMMING_OUTPUT_DIR, VECTORIZATION_DIR, IMG_DIR, DATA_CLEANING_OUTPUT_DIR, STOPWORD_OUTPUT_DIR, CASE_FOLDING_OUTPUT_DIR, TOKENIZATION_OUTPUT_DIR, WORD_REPAIR_OUTPUT_DIR
from word_cloud import visualize_word_cloud

def compute_tfidf(df: pd.DataFrame, token_column: str) -> pd.DataFrame:
    """
    Compute TF-IDF using scikit-learn from a DataFrame column containing tokenized documents.
    
    Args:
        df: Pandas DataFrame containing tokenized documents.
        token_column: Name of the column containing lists of tokens per document.
        
    Returns:
        tfidf_results: List of dictionaries with TF-IDF scores per document.
        vectorizer: Trained TfidfVectorizer instance.
    """
    # Convert list of tokens back to strings
    df[token_column] = df[token_column].apply(ast.literal_eval)
    df[token_column] = df[token_column].apply(lambda tokens: ' '.join(tokens))
    
    # Initialize TfidfVectorizer
    vectorizer = TfidfVectorizer(
        lowercase=False,
        token_pattern=r'\S+',
        smooth_idf=True,
        sublinear_tf=True,
        norm='l2',
        use_idf=True
    )

    # Fit and transform the data
    tfidf_matrix = vectorizer.fit_transform(df[token_column])
    tfidf_df = pd.DataFrame(tfidf_matrix.toarray(), columns=vectorizer.get_feature_names_out())

    # Print results
    print("\nTF-IDF Matrix:")
    print(tfidf_df.head(10))
    
    print("\nConverting result from pandas data frame to CSV file")
    try:
        output_file_name = VECTORIZATION_DIR / f"vectorization_{TIMESTAMP}.csv"
        tfidf_df.to_csv(output_file_name, index=False)
        print(f"Vectorization CSV file successfully exported as {output_file_name}")
        
        return tfidf_df
    except Exception as e:
        print("An error occurred while saving the CSV file:", e)
    
def analyze_vocabulary_stats_df(df: pd.DataFrame, token_column: str):
    """
    Analyze vocabulary statistics from a DataFrame column of tokenized documents.
    
    Args:
        df: Pandas DataFrame containing tokenized documents.
        token_column: Name of the column containing lists of tokens per document.
    """
    vocab = set()
    doc_lengths = []
    total_terms = 0
    
    for tokens in df[token_column]:
        vocab.update(tokens)
        doc_lengths.append(len(tokens))
        total_terms += len(tokens)
    
    print(f"\nCorpus Statistics:")
    print(f"Total documents: {len(df):,}")
    print(f"Vocabulary size: {len(vocab):,}")
    print(f"Total terms: {total_terms:,}")
    print(f"Average document length: {np.mean(doc_lengths):.1f} terms")
    print(f"Document length range: {min(doc_lengths)} - {max(doc_lengths)} terms")
    
def main(last_process_of_preprocessing: str) -> None:
    """Main function to run TF-IDF vectorization with improved accuracy."""
    
    SOURCE_DIR = None
    
    if last_process_of_preprocessing == "Data cleaning":
        SOURCE_DIR = DATA_CLEANING_OUTPUT_DIR
    elif last_process_of_preprocessing == "Stopword removal":
        SOURCE_DIR = STOPWORD_OUTPUT_DIR
    elif last_process_of_preprocessing == "Case folding":
        SOURCE_DIR = CASE_FOLDING_OUTPUT_DIR
    elif last_process_of_preprocessing == "Word repair":
        SOURCE_DIR = WORD_REPAIR_OUTPUT_DIR
    elif last_process_of_preprocessing == "Tokenizing":
        SOURCE_DIR = TOKENIZATION_OUTPUT_DIR
    elif last_process_of_preprocessing == "Stemming":
        SOURCE_DIR = STEMMING_OUTPUT_DIR
    else:
        SOURCE_DIR = None
    
    source_files = [str(f) for f in Path(SOURCE_DIR).iterdir() if f.is_file()]

    if not source_files:
        print(f"No files found in: {SOURCE_DIR}")
        return

    selected_file = questionary.select(
        f"Select the {last_process_of_preprocessing} to process with TF-IDF vectorization:",
        choices=source_files
    ).ask()
    
    print(f"Selected file: {selected_file}")
    
    source_df = pd.read_csv(SOURCE_DIR / selected_file)

    print(f"Computing TF-IDF using scikit-learn method...")
    
    # Analyze corpus statistics
    analyze_vocabulary_stats_df(source_df, 'text')
    
    # Compute TF-IDF
    tfidf_df = compute_tfidf(source_df, token_column="text")
    
    if questionary.confirm("Generate word cloud visualization?").ask():
        visualize_word_cloud(tfidf_df)

if __name__ == '__main__':
    main(last_process_of_preprocessing="Tokenizing")