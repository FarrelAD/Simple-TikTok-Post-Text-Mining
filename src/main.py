import pandas as pd
import questionary

from constants import DATA_DIR_PATH


def preprocessing_data() -> None:
    print("Preprocessing data is running!")


def vectorization() -> None:
    print("Vectorization is running!")

def sentiment_analysis() -> None:
    print("Sentiment analysis is running!")


def main() -> None:
    print("Preview dataset")
    
    raw_data_df = pd.read_csv(DATA_DIR_PATH / "CSV" / "tiktok_comments_text.csv")
    
    print(raw_data_df.head())
    
    selected_menu = questionary.select("Select menu", choices=[
        "1. Preprocessing data",
        "2. Vectorization",
        "3. Sentiment analysis"
    ]).ask()
    
    if selected_menu == "1. Preprocessing data":
        preprocessing_data()
    elif selected_menu == "2. Vectorization":
        vectorization()
    elif selected_menu ==  "3. Sentiment analysis":
        sentiment_analysis()


if __name__ == '__main__':
    main()