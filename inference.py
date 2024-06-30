import torch
import pandas as pd
import argparse
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from datasets import load_dataset
import numpy as np
from datasets import disable_caching
import os
from main import allow_patterns_prefix, default_patterns_list
import json

disable_caching()

access_token = "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"
cache_dir = "/root/.cache/huggingface"

#disable_caching()
RETRY_LIMIT = 5 # 设置重试次数

def delete_files(file_path):
    for root, dirs, files in os.walk(file_path, topdown=False):
        for name in files:
            file_path = os.path.join(root, name)
            os.remove(file_path)
        for name in dirs:
            dir_path = os.path.join(root, name)
            os.rmdir(dir_path)



tokenizer = AutoTokenizer.from_pretrained('Chrisneverdie/sports-text-classifier')
model = AutoModelForSequenceClassification.from_pretrained('Chrisneverdie/sports-text-classifier', torch_dtype=torch.bfloat16)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)


# def compute_scores(batch):
#     inputs = tokenizer(batch['text'], return_tensors="pt", padding="longest", truncation=True).to(device)
#     with torch.no_grad():
#         outputs = model(**inputs)
#         logits = outputs.logits.squeeze(-1).float().cpu().numpy()

#     batch["score"] =  logits.tolist()
#     return batch

# def add_prefix(example):
#     example['pred'] = np.argmax(example['score'])
#     return example



def compute_scores(batch):
    inputs = tokenizer(batch['text'], return_tensors="pt", padding="longest", truncation=True).to(device)
    with torch.no_grad():
        outputs = model(**inputs).logits.argmax().item()

    batch["score"] =  outputs
    return batch


def process_data(name):

    retry_count = 0
    while retry_count < RETRY_LIMIT:
        try:
            dataset = load_dataset("Chrisneverdie/OnlySports", name,
                        split="train", num_proc=8)
            print('Dataset loaded')
            break
        except Exception as e:
            retry_count += 1
  

            if retry_count >= RETRY_LIMIT:
                error_message = f"Failed to upload dataset after {RETRY_LIMIT} retries. Error: {str(e)}"
                with open("upload_error.txt", "a") as file:
                    file.write(error_message + "\n")
                print(error_message)


    retry_count = 0
    while retry_count < RETRY_LIMIT:
        try:
            dataset = dataset.map(compute_scores, batched=True, batch_size=512)
            #dataset = dataset.map(add_prefix)
            dataset = dataset.filter(lambda example: example["pred"]==1)
            dataset = dataset.select_columns(['text','url','token_count'])
            print('Dataset filtered')
            break
        except Exception as e:
            retry_count += 1
  

            if retry_count >= RETRY_LIMIT:
                error_message = f"Failed to upload dataset after {RETRY_LIMIT} retries. Error: {str(e)}"
                with open("upload_error.txt", "a") as file:
                    file.write(error_message + "\n")
                print(error_message)


    retry_count = 0
    while retry_count < RETRY_LIMIT:
        try:
            dataset.push_to_hub('Chrisneverdie/OnlySports_clean', config_name=name, data_dir=f'data/{name}', private=False, max_shard_size="4096MB",token=access_token)
            print('Dataset uploaded')
            break
        except Exception as e:
            retry_count += 1
  

            if retry_count >= RETRY_LIMIT:
                error_message = f"Failed to upload dataset after {RETRY_LIMIT} retries. Error: {str(e)}"
                with open("upload_error.txt", "a") as file:
                    file.write(error_message + "\n")
                print(error_message)

    print('done')

def loop(patten):
    for i in patten:
        process_data(i)
        delete_files(cache_dir)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process parquet files to filter sports URLs.")
    parser.add_argument('-j', '--json', type=str, help='Path to JSON file with allow patterns list')
    parser.add_argument('-n', '--name', type=str, help='Path to JSON file with allow patterns list')



    args = parser.parse_args()
    if args.json:
        with open(args.json, 'r') as f:
            data = json.load(f)
            allow_patterns_list = data.get("patterns", default_patterns_list)
    else:
        allow_patterns_list = [args.name]

    loop(allow_patterns_list)