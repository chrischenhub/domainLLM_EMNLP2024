

# OnlySportsLM

OnlySportsLM is a comprehensive project aimed at creating and evaluating a domain-specific language model for sports-related content. This repository contains the code and resources for the entire OnlySports collection, including dataset creation, model training, and evaluation. 

The OnlySports dataset and model checkpoint can be found in our [Huggingface](https://huggingface.co/collections/Chrisneverdie/onlysports-66b3e5cf595eb81220cc27a6).

## Table of Contents
- [Overview](#overview)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
  - [Data Preprocessing](#data-preprocessing)
  - [Model Training](#model-training)
  - [Evaluation](#evaluation)
- [Contributing](#contributing)
- [License](#license)

## Overview

The OnlySports collection consists of:
1. OnlySports Dataset: A large-scale sports-specific text corpus
2. OnlySports Classifier: A text-embedding model for identifying sports-related content
3. OnlySportsLM: A 196M parameter language model specialized for sports domain
4. OnlySports Benchmark: A novel evaluation method for sports knowledge generation

This repository provides tools and scripts to recreate our work or use our code for your own projects.

## Requirements

- Python 3.8+
- CUDA 12.5+ (for GPU acceleration)
- Key libraries:
  - `huggingface_hub`
  - `transformers`
  - `datasets`
  - `torch` (version 2.3.1+cu121 recommended)
  - `pandas`
  - `numpy`
  - `pytorch-lightning==1.9.5`
  - `deepspeed`
  - `wandb`

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/chrischenhub/OnlySportsLM.git
   cd OnlySportsLM
   ```

2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

3. For model training, install additional dependencies:
   ```bash
   pip install torch --upgrade --extra-index-url https://download.pytorch.org/whl/cu121
   pip install pytorch-lightning==1.9.5 deepspeed wandb ninja --upgrade
   ```

## Usage

### Data Preprocessing

1. Download the target dataset to your local directory, preferably in parquet format.

3. Run the sports URL filter:
   ```bash
   python sports_URL_filter.py -t 4 -j patterns.json
   ```
   - `-t`, `--threads`: Number of threads to use (Default: 3)
   - `-j`, `--json`: Path to JSON file containing folder name with parquet files
   - `-n`, `--name`: Folder name with parquet files (if --json not provided)

4. Run the sports classifier:
   ```bash
   python sports_classifier.py -n CC-MAIN-2013-20
   ```

    #### JSON File Structure for Custom Patterns
    Each element in patterns is a folder name that contain parquet files
    ```json
    {
      "patterns": [
        "CC-MAIN-2013-20",
        "CC-MAIN-2013-40"
        ...
      ]
    }
    ```
5. Convert parquet to json
    ```bash
    cargo install parquet2json
    parquet2json ./myfile.parquet cat > output.jsonl
    ```
6. Convert json to bin
    ```bash
    cargo install json2bin@0.2.0
    json2bin -i src/sample.jsonl
    ```
### Model Training

1. Navigate to the training directory:
   ```bash
   cd model_training/
   ```

2. Prepare the training environment:
   ```bash
   ./demo-training-prepare.sh
   ```

3. Start the training process:
   ```bash
   ./demo-training-run.sh
   ```
   Note: You may want to log in to Weights & Biases (wandb) first for experiment tracking.

The current `--my_exit_tokens` number and `--magic_prime` prime is set for training using [OnlySports Dataset](https://huggingface.co/datasets/Chrisneverdie/OnlySports_Dataset). Adjust these parameters if using another dataset.

Refer to [RWKV](https://github.com/BlinkDL/RWKV-LM) repo for detail training setup.

### Evaluation

1. Use `eval_question.jsonl` containing 1000 generated sports prompts.
2. Complete each prompt with your models.
3. Combine and evaluate responses from different models using `api_eval.ipynb`.

Feel free to add more LLMs judges to the notebook for comparison.

## Performance

Here's a snapshot of OnlySportsLM's performance:

<img width="862" alt="OnlySportsLM Performance Chart" src="https://github.com/user-attachments/assets/4f2ca9eb-965f-465c-994d-c5b79e68a528">

## Citation

If you use OnlySports Collection in your research, please cite our [paper](https://arxiv.org/abs/2409.00286).

## License

This project is licensed under the [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.en).
