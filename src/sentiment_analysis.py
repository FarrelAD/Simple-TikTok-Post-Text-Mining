from itertools import islice
from pathlib import Path
from pprint import pprint

import questionary

from constants import VECTORIZATION_OUTPUT_DIR, DICTIONARY_PATH, TIMESTAMP
from helpers.io import read_json_file, export_data_to_json



def get_unique_tokens() -> set:
    vectorization_files = [str(f) for f in Path(VECTORIZATION_OUTPUT_DIR).iterdir() if f.is_file()]

    if not vectorization_files:
        print("No file found in :", VECTORIZATION_OUTPUT_DIR)
        return

    selected_file = questionary.select(
        "Select the file output from vectorization directory",
        choices=vectorization_files
    ).ask()

    print(f"Selected file: {selected_file}")
    
    documents: list[dict] = read_json_file(Path(selected_file))
    
    unique_tokens = set()
    for sentence in documents:
        unique_tokens.update(sentence.keys())
        
    print("\nPreview all unique token")
    preview_10_tokens = list(islice(unique_tokens, 50))
    pprint(preview_10_tokens)
    
    print(f"Total token: {len(unique_tokens)}")
    
    return unique_tokens

def auto_labelling_with_indobert(tokens: list) -> list[dict]:
    print("\nAuto labelling with IndoBERT is running")
    
    import torch
    from transformers import pipeline
    from transformers import AutoTokenizer, AutoModelForSequenceClassification
    
    DEVICE = 0 if torch.cuda.is_available() else -1
    
    pretrained= "mdhugol/indonesia-bert-sentiment-classification"

    model = AutoModelForSequenceClassification.from_pretrained(pretrained)
    tokenizer = AutoTokenizer.from_pretrained(pretrained)

    sentiment_analysis = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer, device=DEVICE)
    label_index = {'LABEL_0': 'positive', 'LABEL_1': 'neutral', 'LABEL_2': 'negative'}
    
    result = {}
    for token in tokens:
        sentiment = sentiment_analysis(token)
        label = label_index[sentiment[0]['label']]
        result[token] = label
    
    print("\nPreview labelling with indobert")
    for token, label in list(result.items())[:20]:
        print(f"- {token} : {label}")
    
    output_file = DICTIONARY_PATH / f"labelled-tokens-{TIMESTAMP}.json"
    export_data_to_json(data=result, output_file=output_file)
    
    return result

def predict_sentiment(input_data: list[dict], lexicon: list[dict]) -> None:
    print("\nPredicting sentiment is running")
    
    total_positive = 0
    total_negative = 0
    for comment in input_data:
        temp_positive = 0
        temp_negative = 0
        for token in comment.keys():
            if lexicon[token] == "positive":
                temp_positive += 1
            else:
                temp_negative += 1
        if temp_positive > temp_negative:
            total_positive += 1
        else:
            total_negative += 1
    
    if total_positive > total_negative:
        conclusion = "positive"
    elif total_negative > total_positive:
        conclusion = "negative"
    else:
        conclusion = "neutral"
    
    positive_percentage = (total_positive / len(input_data)) * 100
    negative_percentage = (total_negative / len(input_data)) * 100
    
    print(f"\nThe result of sentiment analysis prediction is : {conclusion} with percentage:")
    print(f"Positive: {total_positive} - {positive_percentage:.3f}%")
    print(f"Negative: {total_negative} - {negative_percentage:.3f}%")

def main() -> None:
    is_generate_new_tokens = questionary.confirm("Do you want to generate new labelled tokens ?").ask()
    
    unique_tokens = get_unique_tokens()
    if is_generate_new_tokens:
        lexicon = auto_labelling_with_indobert(unique_tokens)
    else:
        lexicon_file = [str(f) for f in Path(DICTIONARY_PATH).iterdir() if f.is_file() and f.name.startswith("labelled-tokens-")]
        
        selected_file = questionary.select(
            "Select the lexicon file",
            choices=lexicon_file
        ).ask()

        print(f"Selected file: {selected_file}")
        
        lexicon: list[dict] = read_json_file(Path(selected_file))
    
    input_files = [str(f) for f in Path(VECTORIZATION_OUTPUT_DIR).iterdir() if f.is_file()]
        
    selected_file = questionary.select(
        "Select the vectorization file",
        choices=input_files
    ).ask()

    print(f"Selected file: {selected_file}")
    
    input_data: list[dict] = read_json_file(Path(selected_file))
    
    predict_sentiment(input_data=input_data, lexicon=lexicon)


if __name__ == '__main__':
    main()