import json
import numpy as np
from pathlib import Path
from collections import defaultdict
import questionary
from wordcloud import WordCloud
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import normalize

from constants import TIMESTAMP, STEMMING_OUTPUT_DIR, VECTORIZATION_OUTPUT_DIR, IMG_DIR_PATH
from helpers.io import export_data_to_json, read_json_file

def compute_tfidf_sklearn(docs: list[list[str]]):
    """
    Compute TF-IDF using scikit-learn for better accuracy and performance.
    
    Args:
        docs: List of documents, where each document is a list of tokens
        
    Returns:
        List of dictionaries containing TF-IDF scores for each document
    """
    # Convert list of tokens back to strings for sklearn
    doc_strings = [' '.join(doc) for doc in docs]
    
    # Initialize TfidfVectorizer with optimized parameters
    vectorizer = TfidfVectorizer(
        lowercase=False,  # Assume preprocessing is already done
        token_pattern=r'\S+',  # Split on whitespace, preserve all tokens
        smooth_idf=True,  # Add 1 to document frequencies (standard practice)
        sublinear_tf=True,  # Apply sublinear scaling to TF (1 + log(tf))
        norm='l2',  # L2 normalization for better similarity comparisons
        use_idf=True
    )
    
    # Fit and transform documents
    tfidf_matrix = vectorizer.fit_transform(doc_strings)
    
    # Get feature names (vocabulary)
    feature_names = vectorizer.get_feature_names_out()
    
    # Convert sparse matrix to list of dictionaries
    tfidf_results = []
    for i in range(tfidf_matrix.shape[0]):
        doc_tfidf = {}
        # Get non-zero values for this document
        row = tfidf_matrix.getrow(i)
        for j in row.nonzero()[1]:
            word = feature_names[j]
            score = row[0, j]
            doc_tfidf[word] = float(score)
        tfidf_results.append(doc_tfidf)
    
    return tfidf_results, vectorizer


def compute_tfidf(docs: list[list[str]], method='sklearn'):
    """
    Compute TF-IDF using the specified method.
    
    Args:
        docs: List of documents, where each document is a list of tokens
        method: 'sklearn' for scikit-learn implementation, 'manual' for improved manual
        
    Returns:
        TF-IDF results and optional vectorizer object
    """
    if method == 'sklearn':
        return compute_tfidf_sklearn(docs)
    else:
        return compute_tfidf_manual_improved(docs), None

def analyze_vocabulary_stats(docs: list[list[str]]):
    """
    Analyze vocabulary statistics for better understanding of the corpus.
    
    Args:
        docs: List of documents, where each document is a list of tokens
    """
    vocab = set()
    doc_lengths = []
    total_terms = 0
    
    for doc in docs:
        vocab.update(doc)
        doc_lengths.append(len(doc))
        total_terms += len(doc)
    
    print(f"\n📊 Corpus Statistics:")
    print(f"Total documents: {len(docs):,}")
    print(f"Vocabulary size: {len(vocab):,}")
    print(f"Total terms: {total_terms:,}")
    print(f"Average document length: {np.mean(doc_lengths):.1f} terms")
    print(f"Document length range: {min(doc_lengths)} - {max(doc_lengths)} terms")

def visualize_word_cloud() -> None:
    """Generate word cloud visualization from the latest TF-IDF results."""
    files = list(VECTORIZATION_OUTPUT_DIR.glob('*'))
    
    if not files:
        print(f"ERROR: Cannot find any files in {VECTORIZATION_OUTPUT_DIR}")
        return

    files.sort(key=lambda f: f.stat().st_mtime, reverse=True)
    newest_file = files[0]
    
    tfidf_docs = read_json_file(file_path=newest_file)
    
    # Aggregate TF-IDF scores across all documents
    tfidf_total = defaultdict(float)
    for doc in tfidf_docs:
        for term, score in doc.items():
            tfidf_total[term] += score
    
    # Filter out very low-scoring terms for cleaner visualization
    min_score = np.percentile(list(tfidf_total.values()), 25)  # Keep top 75%
    filtered_scores = {term: score for term, score in tfidf_total.items() 
                      if score >= min_score}
    
    if not filtered_scores:
        print("No terms found for word cloud generation")
        return
    
    # Generate word cloud with improved parameters
    wordcloud = WordCloud(
        width=1200, 
        height=600, 
        background_color='white',
        max_words=200,
        colormap='viridis',
        relative_scaling=0.5,
        min_font_size=10
    )
    wordcloud.generate_from_frequencies(filtered_scores)
    
    output_file = IMG_DIR_PATH / f"word-cloud-{TIMESTAMP}.png"
    wordcloud.to_file(output_file)
    
    print(f"✅ Successfully generated word cloud: {output_file}")
    print(f"📈 Word cloud contains {len(filtered_scores):,} terms")

def main() -> None:
    """Main function to run TF-IDF vectorization with improved accuracy."""
    stemming_files = [str(f) for f in Path(STEMMING_OUTPUT_DIR).iterdir() if f.is_file()]

    if not stemming_files:
        print(f"No files found in: {STEMMING_OUTPUT_DIR}")
        return

    selected_file = questionary.select(
        "Select the stemmed file to process with TF-IDF vectorization:",
        choices=stemming_files
    ).ask()
    
    if not selected_file:
        print("No file selected. Exiting.")
        return
    
    print(f"📂 Selected file: {selected_file}")

    # Load documents
    with open(selected_file, "r", encoding="utf-8") as file:
        documents = json.load(file)
    
    # Validate input data
    if not documents or not all(isinstance(doc, list) for doc in documents):
        print("ERROR: Invalid document format. Expected list of lists.")
        return

    method_key = 'sklearn'
    
    print(f"🔄 Computing TF-IDF using {method_key} method...")
    
    # Analyze corpus statistics
    analyze_vocabulary_stats(documents)
    
    # Compute TF-IDF
    result = compute_tfidf(documents, method=method_key)
    if method_key == 'sklearn':
        tfidf_results, vectorizer = result
        print(f"📏 TF-IDF matrix shape: {len(tfidf_results)} documents × {len(vectorizer.vocabulary_)} terms")
    else:
        tfidf_results = result
    
    # Preview results
    print(f"\n🔍 Preview of TF-IDF Results (top 5 documents):")
    for idx, tfidf_doc in enumerate(tfidf_results[:5]):
        print(f"\n📄 Document {idx + 1} (top 10 terms):")
        sorted_terms = sorted(tfidf_doc.items(), key=lambda x: -x[1])[:10]
        for word, score in sorted_terms:
            print(f"  {word:15}: {score:.4f}")
    
    # Export results
    output_file = VECTORIZATION_OUTPUT_DIR / f"tf-idf-{TIMESTAMP}.json"
    export_data_to_json(data=tfidf_results, output_file=output_file)
    print(f"💾 Results saved to: {output_file}")
    
    # Optional word cloud visualization
    if questionary.confirm("Generate word cloud visualization?").ask():
        visualize_word_cloud()

if __name__ == '__main__':
    main()