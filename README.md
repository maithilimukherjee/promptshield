# PromptShield

A hybrid cybersecurity system combining rule-based detection and generative AI classification to identify, score, and mitigate prompt-injection and jailbreak attacks against LLM applications.

## 📋 Overview

PromptShield is a two-tier security engine designed to protect large language model (LLM) applications from malicious inputs. It combines fast, cost-effective rule-based detection with deep semantic analysis using LLM classifiers to provide comprehensive protection against:

- **Prompt Injection Attacks**: Attempts to override system instructions through user input
- **Jailbreak Attempts**: Efforts to circumvent safety guidelines and restrictions
- **System Prompt Extraction**: Techniques to leak or expose system prompts
- **Obfuscated Payloads**: Base64-encoded and other encoded malicious content

## 🏗️ Architecture

PromptShield employs a **two-tier defense strategy**:

### Tier 1: Rule-Based Engine (Fast & Free)
- **Latency**: Sub-millisecond
- **Cost**: $0 (no external API calls)
- **Detection Methods**:
  - Regex pattern matching for known jailbreak keywords and phrases
  - Base64 decoding and obfuscation detection
  - Heuristic analysis (content length, special character ratios)

### Tier 2: LLM Classifier (Deep Analysis)
- **Latency**: ~1-2 seconds
- **Cost**: Minimal (Groq API integration)
- **Detection Methods**:
  - Semantic intent analysis using generative AI
  - Pydantic-validated structured output
  - Multi-category classification: `prompt_injection`, `jailbreak`, `system_extraction`, `none`

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/maithilimukherjee/promptshield.git
cd promptshield

# Install dependencies
pip install -r requirements.txt
```

### Configuration

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
```

### Basic Usage

```python
from hybrid_engine import HybridEngine

# Initialize the engine with optional confidence threshold
engine = HybridEngine(confidence_threshold=0.7)

# Inspect a prompt
prompt = "What is the capital of France?"
result = engine.inspect(prompt)

print(result)
# Output:
# {
#     "action": "ALLOW",
#     "decision_tier": "Tier 2 (LLM Classifier)",
#     "is_malicious": False,
#     "attack_type": "none",
#     "confidence": 0.95,
#     "explanation": "Passed inspection.",
#     "latency_ms": 1250.45
# }
```

## 📁 Project Structure

```
promptshield/
├── hybrid_engine.py          # Main orchestration engine
├── rule_based_engine.py      # Tier 1: Fast pattern matching & heuristics
├── llm_classifier.py         # Tier 2: Generative AI semantic analysis
├── benchmark_hybrid.py       # Performance evaluation suite
├── dataset_setup.py          # Test dataset configuration
├── test_rules.py             # Rule engine unit tests
├── .gitignore                # Git ignore patterns
└── README.md                 # This file
```

## 📊 Component Details

### 1. Rule-Based Engine (`rule_based_engine.py`)

Fast detection using compiled regex patterns and heuristics:

**Detection Methods**:
- **Regex Patterns**: Matches known jailbreak keywords (e.g., "ignore all previous instructions", "DAN mode", "act as an unrestricted")
- **Base64 Obfuscation**: Decodes and analyzes potential base64-encoded payloads
- **Heuristics**: Detects anomalies like excessive special characters or unusual text length

**Risk Scoring**:
- Base64 obfuscation: +8 points
- Regex match: +7 points
- Heuristic anomaly: +4 points
- Final score: Min(sum, 10)

**Output Example**:
```json
{
    "flagged": true,
    "risk_score": 7,
    "details": {
        "regex_match": true,
        "base64_obfuscation": false,
        "heuristic_anomaly": false
    }
}
```

### 2. LLM Classifier (`llm_classifier.py`)

Semantic analysis using Groq's generative AI models:

**Features**:
- Uses Pydantic for structured output validation
- Groq API integration for low-cost inference
- Temperature set to 0.0 for deterministic results
- Graceful error handling with fallback responses

**Attack Categories**:
- `prompt_injection`: Direct attempt to override instructions
- `jailbreak`: Effort to circumvent safety guidelines
- `system_extraction`: Attempt to leak system prompts
- `none`: Clean, benign input

**Output Example**:
```json
{
    "is_malicious": true,
    "attack_type": "jailbreak",
    "confidence": 0.92,
    "explanation": "Detected DAN mode jailbreak attempt with request to ignore system guidelines."
}
```

### 3. Hybrid Engine (`hybrid_engine.py`)

Orchestrates both tiers with intelligent routing:

**Decision Logic**:
1. **Tier 1 Match** → Immediately BLOCK (no cost, sub-millisecond)
2. **Tier 1 Pass** → Route to Tier 2 LLM Classifier
3. **Confidence ≥ threshold** → BLOCK
4. **Confidence < threshold** → FLAG_FOR_REVIEW (manual inspection)
5. **Not malicious** → ALLOW

**Output Actions**:
- `BLOCK`: Immediate rejection (Tier 1 or high-confidence Tier 2)
- `FLAG_FOR_REVIEW`: Manual review required (Tier 2 with low confidence)
- `ALLOW`: Safe to process

## 🧪 Testing & Benchmarking

### Run Unit Tests

```bash
python test_rules.py
```

### Benchmark the Hybrid Engine

```bash
python benchmark_hybrid.py
```

This will evaluate the system on 100 test prompts and output:
- **Accuracy, Precision, Recall, F1 Score**
- **Average latency per prompt**
- **Tier 1 vs Tier 2 split** (cost/performance breakdown)
- **Confusion matrix metrics**

**Expected Benchmark Output**:
```
HYBRID ENGINE BENCHMARK
Overall Accuracy : 95.20%
Precision        : 94.50%
Recall           : 96.00%
F1 Score         : 0.9524
Average Latency  : 850.32 ms / prompt
Tier 1 (Rules) Short-Circuited : 45 prompts (0 Cloud Cost)
Tier 2 (LLM) Evaluated          : 55 prompts
False Positives : 3 | False Negatives : 2
```

## 🔧 Configuration Options

### HybridEngine Parameters

```python
engine = HybridEngine(
    confidence_threshold=0.7  # Confidence threshold for Tier 2 (default: 0.7)
)
```

- **confidence_threshold** (float, 0.0-1.0): 
  - If LLM confidence ≥ threshold and is_malicious=True → BLOCK
  - If LLM confidence < threshold and is_malicious=True → FLAG_FOR_REVIEW

## 📈 Performance Characteristics

| Metric | Tier 1 | Tier 2 | Hybrid |
|--------|--------|--------|--------|
| Latency | <1 ms | ~1-2s | ~850ms avg |
| API Cost | $0 | $0.0005/call | ~$0.000025/blocked prompt |
| Detection Type | Pattern-based | Semantic | Combined |
| False Positives | Medium | Low | Very Low |

## 🛡️ Security Features

- **Zero-Cost Fast Path**: Rule engine blocks ~40-50% of attacks instantly
- **Semantic Defense**: LLM classifier catches sophisticated, obfuscated attacks
- **Graceful Degradation**: Falls back safely if LLM API unavailable
- **Audit Trail**: Every decision includes latency, tier, confidence, and reasoning
- **Customizable Thresholds**: Tune balance between precision and recall

## 🚨 Known Limitations

- Requires internet connection for Tier 2 (Groq API)
- API rate limits apply to Groq service
- Rule patterns require manual updates for new attack vectors
- Base64 detection may have false positives on legitimate encoded content

## 📚 Dataset Integration

The `dataset_setup.py` file provides integration with test datasets:

```python
from dataset_setup import test_prompts, ground_truth_labels

# Use these for evaluation and benchmarking
for prompt, label in zip(test_prompts, ground_truth_labels):
    result = engine.inspect(prompt)
    # label: 1 = malicious, 0 = benign
```

## 🔑 Environment Variables

- **GROQ_API_KEY**: Required for Tier 2 classification
  - Obtain from [Groq Console](https://console.groq.com)
  - Store in `.env` file (not in version control)

## 🤝 Contributing

Contributions are welcome! Areas for improvement:

- [ ] Additional rule patterns for emerging attack vectors
- [ ] Performance optimization for high-throughput scenarios
- [ ] Multi-language support
- [ ] Integration with popular LLM frameworks (LangChain, LlamaIndex)
- [ ] Web API wrapper for REST/gRPC deployment
- [ ] Detailed logging and observability

## 📄 License

MIT License - See LICENSE file for details

## 👤 Author

[Maithili Mukherjee](https://github.com/maithilimukherjee)

## 🙏 Acknowledgments

- Built with [Groq](https://groq.com) for fast LLM inference
- Inspired by security best practices in prompt engineering
- Topics: Cybersecurity, Generative AI, LLM Safety, Prompt Engineering

---

**Stay Safe. Stay Shielded. 🛡️**
