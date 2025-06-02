import pandas as pd
import os
import questionary

from constants import DATASET_FILE_PATH

from case_folding import main as case_folding
from data_cleaning import main as data_cleaning
from stopword import main as stopword
from stemming import main as stemming
from word_repair import main as word_repair
from tokenization import main as tokenization

from tf_idf import main as tf_idf


last_process_of_preprocessing = None


def preprocessing_data() -> None:
    global last_process_of_preprocessing
    
    print("Preprocessing data is running!")
    
    preprocessing_steps = ["Data cleaning", "Stemming", "Stopword removal", "Case folding", "Word repair", "Tokenizing"]
    chosen_steps = []
    num_step = 0
    
    while preprocessing_steps:
        num_step += 1
        
        answer = questionary.select(f"What do you want to do for step {num_step} ?", choices=preprocessing_steps).ask()
        
        if answer:
            chosen_steps.append(answer)
            preprocessing_steps.remove(answer)
        else:
            break
    
    print("\nYou chose the following sequence:")
    for i, s in enumerate(chosen_steps, 1):
        print(f"{i}. {s}")
    
    is_confirm_execute_process = questionary.confirm("Start the preprocessing now?").ask()
    
    if not is_confirm_execute_process:
        print("Preprocessing is cancelled")
        return
    
    prev_step = None

    for step in chosen_steps:
        if step == "Data cleaning":
            data_cleaning(prev_process=prev_step)
        elif step == "Stopword removal":
            stopword(prev_process=prev_step)
        elif step == "Case folding":
            case_folding(prev_process=prev_step)
        elif step == "Word repair":
            word_repair(prev_process=prev_step)
        elif step == "Tokenizing":
            tokenization(prev_process=prev_step)
        elif step == "Stemming":
            stemming(prev_process=prev_step)
        
        prev_step = step
    
    last_process_of_preprocessing = prev_step
    
    print("=== PREPROCESSING IS DONE ===")


def vectorization() -> None:
    print("Vectorization is running!")
    
    tf_idf(last_process_of_preprocessing=last_process_of_preprocessing)

def sentiment_analysis() -> None:
    print("Sentiment analysis is running!")


def main() -> None:
    print("Preview dataset")
    
    raw_data_df = pd.read_csv(DATASET_FILE_PATH)
    
    print(raw_data_df.head(20))
    print("\n")
    
    selected_menu = "" 
    
    while selected_menu != "4. EXIT":
        selected_menu = questionary.select("Select menu", choices=[
            "1. Preprocessing data",
            "2. Vectorization",
            "3. Sentiment analysis",
            "4. EXIT"
        ]).ask()
        
        os.system("clear")
        
        if selected_menu == "1. Preprocessing data":
            preprocessing_data()
        elif selected_menu == "2. Vectorization":
            vectorization()
        elif selected_menu ==  "3. Sentiment analysis":
            sentiment_analysis()
        elif selected_menu == "4. EXIT":
            print("THE PROGRAM IS STOPPED!")
    


if __name__ == '__main__':
    main()