import json
import math
from pathlib import Path
from collections import defaultdict
import questionary

from constants import TIMESTAMP, STEMMING_OUTPUT_DIR, VECTORIZATION_OUTPUT_DIR
from helpers.io import export_data_to_json

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


if __name__ == '__main__':
    main()