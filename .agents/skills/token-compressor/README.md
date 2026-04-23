# Token Compressor Skill

The **Token Compressor** skill is designed to reduce token consumption and operational costs in AI agent workflows. It achieves this by intelligently compressing prompts, conversation history, and context windows while strictly preserving high-fidelity components like code, examples, and security constraints.

## Features

- **Multi-Target Compression**: Specialized techniques for prompts, chat history, source code context, and tool definitions.
- **Fidelity Preservation**: A strict "Protected Content" policy ensuring code blocks, few-shot examples, and regex patterns remain 100% intact.
- **Task Routing**: Intelligence to identify simple sub-tasks (like classification or boilerplate generation) that can be offloaded to local, small LLMs (e.g., Llama 3.2, Qwen 2.5) to eliminate per-call costs.
- **Cost Estimation**: Provides metrics on token savings and approximate dollar amounts saved.

## How to Use

### 1. Compression Requests
Use this skill when you need to shrink the context or reduce costs. Common triggers:
- "Compress my system prompt."
- "This conversation is getting expensive, compress the history."
- "Reduce tokens in this context window."

### 2. Optimization Audit
Ask the skill to audit your entire workflow:
- "My agent costs too much per run, help me optimize."
- "What tasks in my workflow could run locally?"

## Protected Content Policy
The skill will **never** compress or alter the following:
- **Code Blocks**: Logic and syntax must remain bit-perfect.
- **Few-shot Examples**: Formatting is critical for pattern matching.
- **Function/Tool Signatures**: Breaking contracts leads to execution errors.
- **Security Constraints**: Must be stated literally and completely.
- **Regex, JSON Schemas, & IDs**: Precision-sensitive data.

## Local Model Routing
For high-volume, low-complexity tasks, the skill recommends using **Ollama** with models like:
- `llama3.2:3b` for classification and intent detection.
- `qwen2.5-coder:7b` for boilerplate code generation.
- `mistral:7b` for summarization.

---

## Token Economy

### API pricing reference

| Model | Input | Output | Avg blended\* |
|---|---|---|---|
| Local (Ollama) | $0 | $0 | **$0** |
| Claude Haiku 4.5 | $0.80 / 1M | $4.00 / 1M | ~$1.60 / 1M |
| Claude Sonnet 4.6 | $3.00 / 1M | $15.00 / 1M | ~$7.50 / 1M |
| Claude Opus 4.7 | $15.00 / 1M | $75.00 / 1M | ~$37.50 / 1M |

\* Blended estimate assumes ~80% input / 20% output token ratio for typical agent workloads.

> **Rule of thumb:** 1 token ≈ 4 characters of English text.

---

### What compression achieves

The skill targets **40–60% reduction in prose tokens** while applying **0% reduction to protected content** (code, examples, regex, error messages, IDs).

For a typical agent system prompt that is 60% prose and 40% protected content:

| Metric | Value |
|---|---|
| Prose reduction | 40–60% |
| Code / example reduction | 0% |
| Effective total reduction | ~25–35% of the full prompt |

**Example savings report** (generated after each compression run):

```
Original:   ~1,840 tokens
Compressed: ~620 tokens
Savings:    ~1,220 tokens (66%)

Protected (unchanged): 3 code blocks, 2 few-shot examples
Prose reduction: 71% | Code reduction: 0%

Approx cost saved @ Sonnet 4.6 input pricing: ~$0.0037 per call
At 1,000 calls/day → ~$3.70/day  |  ~$111/month
```

---

### Task routing economics

Not every sub-task needs a frontier model. Routing simple tasks to a local LLM cuts per-call cost to $0:

| Task type | Recommended model | Cost |
|---|---|---|
| Classification, intent detection | `llama3.2:3b`, `phi4-mini` | $0 |
| Boilerplate generation (CRUD, getters) | `qwen2.5-coder:7b` | $0 |
| Summarisation of long documents | `mistral:7b`, `llama3.2:3b` | $0 |
| Format conversion (JSON↔YAML, CSV→table) | any small local model | $0 |
| Regex / string operations | plain code — no LLM | $0 |
| Complex reasoning, architecture decisions | Sonnet 4.6 / Opus 4.7 | $7.50–$37.50 / 1M |
| Code review, security analysis | Sonnet 4.6 | $7.50 / 1M |
| Novel code generation | Sonnet 4.6 | $7.50 / 1M |

**Combined savings potential** — compression + routing applied to a 10-step agent pipeline where 6 steps are simple tasks:

| Scenario | Cost per run |
|---|---|
| All steps on Sonnet 4.6, no compression | ~$0.075 |
| Simple steps on Ollama, complex on Sonnet 4.6 | ~$0.030 |
| + Prompt compression (40% reduction) | ~$0.018 |
| **Total saving vs baseline** | **~76%** |

---

*This skill focuses on extractive and prose-terse compression, ensuring AI agent performance remains consistent while overhead decreases.*
