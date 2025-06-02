import pandas as pd
import numpy as np
from collections import defaultdict
from wordcloud import WordCloud

from constants import TIMESTAMP, VECTORIZATION_DIR, IMG_DIR

def visualize_word_cloud(tfidf_df: pd.DataFrame) -> None:
    """Generate word cloud visualization from the latest TF-IDF results."""
    
    # Aggregate TF-IDF scores across all documents
    tfidf_total = tfidf_df.sum(axis=0).to_dict()

    # Filter out very low-scoring terms for cleaner visualization
    scores = list(tfidf_total.values())
    min_score = np.percentile(scores, 25)  # Keep top 75%
    filtered_scores = {
        term: score for term, score in tfidf_total.items()
        if score >= min_score
    }

    if not filtered_scores:
        print("No significant terms found for word cloud generation.")
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
    
    print("\nConverting result from wordcloud data frame to png file")
    try:
        output_file_name = IMG_DIR / f"word_cloud_{TIMESTAMP}.png"
        wordcloud.to_file(output_file_name)
        print(f"Tokenization CSV file successfully exported as {output_file_name}")
    except Exception as e:
        print("An error occurred while saving the CSV file:", e)
    
    print("Word cloud process is done!")
    print(f"Word cloud contains {len(filtered_scores):,} terms")

if __name__ == '__main__':
    visualize_word_cloud()