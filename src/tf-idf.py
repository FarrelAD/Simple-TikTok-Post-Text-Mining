import json
import math
from pathlib import Path
from collections import defaultdict
import questionary
from wordcloud import WordCloud

from constants import TIMESTAMP, STEMMING_OUTPUT_DIR, VECTORIZATION_OUTPUT_DIR, IMG_DIR_PATH
from helpers.io import export_data_to_json, read_json_file

def compute_tf(doc: list[str]):
    tf = defaultdict(int)
    for word in doc:
        tf[word] += 1
    total_terms = len(doc)
    for word in tf:
        tf[word] /= total_terms
    return dict(tf)

def compute_idf(docs: list[list[str]]):
    N = len(docs)
    idf = defaultdict(int)
    for doc in docs:
        unique_terms = set(doc)
        for word in unique_terms:
            idf[word] += 1
    for word in idf:
        idf[word] = math.log(N / (1 + idf[word]))
    return dict(idf)

def compute_tfidf(docs: list[list[str]]):
    idf = compute_idf(docs)
    tfidf_all = []
    for doc in docs:
        tf = compute_tf(doc)
        tfidf = {word: tf[word] * idf.get(word, 0) for word in tf}
        tfidf_all.append(tfidf)
    return tfidf_all

def visualize_word_cloud() -> None:
    files = list(VECTORIZATION_OUTPUT_DIR.glob('*'))
    
    if not files:
        print(f"ERROR: Can not found any files in {VECTORIZATION_OUTPUT_DIR}")
        return

    files.sort(key=lambda f: f.stat().st_mtime, reverse=True)
    newest_file = files[0]
    
    tfidf_docs = read_json_file(file_path=newest_file)
    
    tfidf_total = defaultdict(float)
    for doc in tfidf_docs:
        for term, score in doc.items():
            tfidf_total[term] += score
    
    wordcloud = WordCloud(width=800, height=400, background_color='white')
    wordcloud.generate_from_frequencies(tfidf_total)
    
    output_file = IMG_DIR_PATH / f"word-cloud-{TIMESTAMP}.png"
    wordcloud.to_file(output_file)
    
    print("Successfully to generate word cloud visualization")

def main() -> None:
    stemming_files = [str(f) for f in Path(STEMMING_OUTPUT_DIR).iterdir() if f.is_file()]

    if not stemming_files:
        print("No file found in :", STEMMING_OUTPUT_DIR)
        return

    selected_file = questionary.select(
        "Select the file output from stemming to process in TF-IDF vectorization",
        choices=stemming_files
    ).ask()
    
    print(f"Selected file: {selected_file}")

    with open(selected_file, "r", encoding="utf-8") as file:
        documents = json.load(file)
        
    tfidf_results = compute_tfidf(documents)
    
    print(f"\nPreview result from TF-IDF")
    for idx, tfidf_doc in enumerate(tfidf_results[:5]):
        print(f"\nDocument {idx + 1}")
        for word, score in sorted(tfidf_doc.items(), key=lambda x: -x[1]):
            print(f"{word:12}: {score:.4f}")
    
    output_files = VECTORIZATION_OUTPUT_DIR / f"tf-idf-{TIMESTAMP}.json"
    export_data_to_json(data=tfidf_results, output_file=output_files)
    
    is_visualize_word_cloud = questionary.confirm("Do you want to visualize the importance of words in the document using a word cloud?").ask()
    
    if is_visualize_word_cloud:
        visualize_word_cloud()


if __name__ == '__main__':
    main()