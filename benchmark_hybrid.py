import time
import pandas as pd
from dataset_setup import test_prompts, ground_truth_labels
from hybrid_engine import HybridEngine

def run_benchmark():
    engine = HybridEngine()
    
    # Test on a subset of 100 prompts to avoid rate limits (adjust as needed)
    subset_size = 100 
    prompts = test_prompts[:subset_size]
    labels = ground_truth_labels[:subset_size]

    print(f"Evaluating Hybrid Security Engine on {subset_size} prompts...\n")

    tp, fp, tn, fn = 0, 0, 0, 0
    tier1_blocks = 0
    tier2_evals = 0
    total_latency_ms = 0

    for i, (prompt, actual_malicious) in enumerate(zip(prompts, labels)):
        res = engine.inspect(prompt)
        
        predicted_malicious = res["action"] in ["BLOCK", "FLAG_FOR_REVIEW"]
        total_latency_ms += res["latency_ms"]

        if res["decision_tier"].startswith("Tier 1"):
            tier1_blocks += 1
        else:
            tier2_evals += 1

        # Confusion Matrix Updates
        if predicted_malicious and actual_malicious == 1:
            tp += 1
        elif predicted_malicious and actual_malicious == 0:
            fp += 1
        elif not predicted_malicious and actual_malicious == 0:
            tn += 1
        elif not predicted_malicious and actual_malicious == 1:
            fn += 1

        if (i + 1) % 10 == 0:
            print(f"Processed {i + 1}/{subset_size} prompts...")

    total = tp + fp + tn + fn
    accuracy = (tp + tn) / total if total > 0 else 0
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    avg_latency = total_latency_ms / total if total > 0 else 0

    print("HYBRID ENGINE BENCHMARK")
    print(f"Overall Accuracy : {accuracy * 100:.2f}%")
    print(f"Precision        : {precision * 100:.2f}%")
    print(f"Recall           : {recall * 100:.2f}%")
    print(f"F1 Score         : {f1:.4f}")
    print(f"Average Latency  : {avg_latency:.2f} ms / prompt")
    print(f"Tier 1 (Rules) Short-Circuited : {tier1_blocks} prompts (0 Cloud Cost)")
    print(f"Tier 2 (LLM) Evaluated          : {tier2_evals} prompts")
    print(f"False Positives : {fp} | False Negatives : {fn}")

if __name__ == "__main__":
    run_benchmark()