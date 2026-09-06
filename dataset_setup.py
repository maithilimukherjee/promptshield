import os
import pandas as pd
import kagglehub

print("Loading dataset from Kaggle cache...")

# Download / locate dataset
path = kagglehub.dataset_download("mohammedaminejebbar/malicious-prompt-detection-dataset-mpdd")

# Load the CSV
csv_file = os.path.join(path, "MPDD.csv")
df = pd.read_csv(csv_file)

print(f"Total samples: {len(df)}")

# Auto-detect column names
text_col = [c for c in df.columns if c.lower() in ['text', 'prompt', 'input', 'query']][0]
label_col = [c for c in df.columns if c.lower() in ['ismalicious', 'label', 'malicious']][0]

print(f"Using '{text_col}' for text and '{label_col}' for labels.\n")

# 1. Sample 500 of each class to keep the dataset balanced
malicious_df = df[df[label_col] == 1].sample(500, random_state=42)
benign_df = df[df[label_col] == 0].sample(500, random_state=42)

# 2. Combine and shuffle the evaluation dataset
df_eval = pd.concat([malicious_df, benign_df]).sample(frac=1, random_state=42).reset_index(drop=True)

# 3. Extract into Python lists for our engines
test_prompts = df_eval[text_col].tolist()
ground_truth_labels = df_eval[label_col].tolist()

print("--- Sample Malicious Prompt ---")
print(df_eval[df_eval[label_col] == 1].iloc[0][text_col])
print("\nDataset successfully prepared!")