import pandas as pd
from dataset_setup import test_prompts, ground_truth_labels
from rule_based_engine import RuleBasedDetector

# Initialize the detector
detector = RuleBasedDetector()

print("Running Rule-Based Engine across 1,000 evaluation prompts...")

# Run detection on all test prompts
predictions = [int(detector.analyze(p)["flagged"]) for p in test_prompts]

# Calculate accuracy
correct = sum(1 for p, y in zip(predictions, ground_truth_labels) if p == y)
accuracy = (correct / len(ground_truth_labels)) * 100

print(f"\nRule-Based Layer Accuracy: {accuracy:.2f}%")

# Quick breakdown of results
fp = sum(1 for p, y in zip(predictions, ground_truth_labels) if p == 1 and y == 0)
fn = sum(1 for p, y in zip(predictions, ground_truth_labels) if p == 0 and y == 1)

print(f"False Positives (Safe prompts flagged as bad): {fp}")
print(f"False Negatives (Attacks missed by rules): {fn}")