from flask import Flask
import pandas as pd
import logging
import os
import re
import ast
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from Utilities.llm import generate_response_openAI
app = Flask(__name__)

@app.route("/")
def home():
    return "Hello world"


# Setting up logging
logging.basicConfig(level=logging.INFO, filename='processing.log', filemode='a',
                    format='%(asctime)s - %(message)s')

    
def clean_output(llm_output):
    try:
        llm_output = llm_output.strip()
        match = re.search(r'```(?:python)?\n?(.*?)```', llm_output, re.DOTALL)
        if match:
            content = match.group(1).strip()
        else:
            content = llm_output.strip()
        cleaned_list = ast.literal_eval(content)
        if isinstance(cleaned_list, list) and all(isinstance(item, str) for item in cleaned_list):
            return cleaned_list
        else:
            raise ValueError("Output is not a list of strings")
    except (SyntaxError, ValueError) as e:
        logging.error(f"Error in clean_output: {e}")
        return None
    
def clean_output_openai(llm_output):
    try:

        output_list = ast.literal_eval(llm_output)
        
        if isinstance(output_list, list):
            return output_list
        else:
            raise ValueError("The evaluated output is not a list.")

    except (SyntaxError, ValueError) as e:
        print(f"Error: {e}")
        output_list = []

def process_batches(df, batch_size=20):
    return [df[i:i + batch_size] for i in range(0, len(df), batch_size)]

def create_prompt(batch):
    prompt = (
        "Instructions:\n"
        "Categorize the following text_list into one of the following categories:\n"
        "* Software Installation and Configuration\n"
        "* Networking Issues\n"
        "* Hardware Compatibility and Drivers\n"
        "* File Management and System Backup\n"
        "* System Errors and Bug Reports\n"
        "* Dual Boot and Partitioning\n"
        "* Miscellaneous and General Inquiries\n\n"
        "Ensure the output is in the sequential order of the provided text_list. Only output the list of categories corresponding to the text_list.\n\n"
        "text_list: "
    )
    lst = [f"'{row['raw_text']}'" for _, row in batch.iterrows()]
    list_string = "[" + ", ".join(lst) + "]"
    prompt += list_string + f" \nOutput format: A list of categories corresponding to the text_list, in the same order. output should contain list of categories in same order as text_list and should be as same length as original list which is text_list_length = {len(lst)}"
    return prompt

def assign_categories_to_dataframe(df, categories_list):
    df['category'] = categories_list
    return df

def save_checkpoint(offset):
    with open('checkpoint.txt', 'w') as f:
        f.write(str(offset))

def load_checkpoint():
    if os.path.exists('checkpoint.txt'):
        with open('checkpoint.txt', 'r') as f:
            try:
                return int(f.read().strip())
            except ValueError:
                logging.error("Checkpoint file contains invalid data. Starting from the beginning.")
                return 0
    return 0

def save_categorized_batches(categorized_batches, file_index, current_offset, save_interval):
    output_filename = f'ubuntu_queries_categorized_{file_index}.csv'
    pd.concat(categorized_batches).to_csv(output_filename, index=False)
    logging.info(f"Processed records {current_offset+1}-{current_offset+save_interval} into file {output_filename}")

def process_and_categorize(df, batch_size=20, save_interval=2000):
    categorized_batches = []
    batches = process_batches(df, batch_size=batch_size)
    total_records = len(df)

    start_offset = load_checkpoint()
    current_offset = start_offset

    for batch_index, batch in enumerate(batches):
        record_index = batch_index * batch_size
        if record_index < start_offset:
            continue

        prompt = create_prompt(batch)
        categories = None

        while categories is None or len(categories) != len(batch):
            categories = generate_response_openAI(prompt)

        categorized_batch = assign_categories_to_dataframe(batch, categories)
        categorized_batches.append(categorized_batch)

        if (batch_index + 1) % (save_interval // batch_size) == 0:
            file_index = (current_offset // save_interval) + 1
            save_categorized_batches(categorized_batches, file_index, current_offset, save_interval)
            categorized_batches = []
            current_offset += save_interval
            save_checkpoint(current_offset)

    if categorized_batches:
        file_index = (current_offset // save_interval) + 1
        save_categorized_batches(categorized_batches, file_index, current_offset, save_interval)

    save_checkpoint(total_records)


# Load the CSV file
df = pd.read_csv('ubuntu_customer_msg_small.csv')

# Select the first 10000 records
df_subset = df.head(10000)

# Process and categorize the records
# process_and_categorize(df_subset)

import glob
import os

def combine_csv_files(folder_path):
    files = glob.glob(folder_path + 'ubuntu_queries_categorized_*.csv')
    breakpoint()
    # Initialize an empty list to hold all dataframes
    dfs = []

    total_rows = 0

    for file in files:
        df = pd.read_csv(file)
        rows_in_file = len(df)
        total_rows += rows_in_file
        print(f'Number of rows in {file}: {rows_in_file}')
        dfs.append(df)
    breakpoint()
    # Concatenate all dataframes into one
    combined_df = pd.concat(dfs, ignore_index=True)
    combined_file_path = folder_path + 'ubuntu_queries_categorized.csv'
    combined_df.to_csv(combined_file_path, index=False)

    print(f'\nCombined CSV saved successfully as {combined_file_path}')
    print(f'Total number of rows in combined CSV: {total_rows}')

# combine_csv_files("")
