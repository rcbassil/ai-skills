---
name: token-compressor
description: Reduces token usage and AI agent costs by compressing prompts, context, and conversation history — without degrading code quality or examples — and by routing simple tasks to local small LLMs. Use when the user asks to "compress this", "reduce tokens", "make this cheaper", "shrink the context", or "optimize my prompt for cost".
---

# Token Compressor Skill

Reduces token consumption in AI agent workflows by compressing prompts, context windows, system instructions, and conversation history — without losing semantic meaning, code correctness, or example fidelity. Also recommends routing simple sub-tasks to local small LLMs to cut per-call costs.

## Core Rule: What Must Never Be Compressed

Before applying any technique, identify and mark these as **PROTECTED** — never shorten, paraphrase, or drop them:

| Protected content | Why |
|---|---|
| Code blocks (any language) | Changing even one token can break logic, syntax, or semantics |
| Few-shot examples | Models rely on exact formatting and content to pattern-match |
| Function/tool signatures | Renaming or truncating breaks calling contracts |
| Error messages / stack traces | Every word carries diagnostic signal |
| Regex, SQL, JSON schemas | Precision-sensitive — paraphrasing breaks them |
| Numeric values, thresholds, IDs | Off-by-one or truncation causes silent bugs |
| Security constraints | Must be stated completely and literally |

Only **prose surrounding** protected content is eligible for compression.

---

## Instructions

### 1. Identify What to Compress

Ask (or infer from context) which of these the user wants to compress:

| Target | When to use |
|---|---|
| **Prompt / instruction** | A system prompt or user message that is verbose |
| **Conversation history** | A long chat thread being fed as context |
| **Code context** | Source files included in agent context |
| **Document / text** | Docs, READMEs, or data passed as context |
| **Agent tool definitions** | Tool schemas being sent to the model |
| **Agent task routing** | Workflow with sub-tasks that could run on cheaper models |

### 2. Apply the Right Technique

#### A. Prompt / Instruction Compression
Compress only the **prose and natural language** — never the examples, constraints, or code snippets.

- Remove filler phrases: "Please make sure to...", "It is important that...", "Always remember to..."
- Convert prose rules into bullet lists or numbered steps
- Replace verbose role descriptions with terse role + goal statements
- Collapse redundant instructions (two rules saying the same thing → keep one)
- Use symbols where unambiguous (`→` for "leads to", `&` for "and", `e.g.` for "for example")
- Target: reduce word count by **40–60%** in prose; **0% reduction** in code/examples

**Before:**
```
You are a helpful assistant. Your job is to help the user with their questions. 
Please make sure to always be polite and professional. It is very important that 
you never provide information that could be harmful. Always cite your sources 
when possible and make sure your answers are accurate.
```
**After:**
```
Helpful assistant. Be polite & professional. Never provide harmful info. Cite sources. Be accurate.
```

**Before (with examples — protect them):**
```
When the user asks you to format code, make sure you always use proper indentation
and follow the style of the existing codebase. Here is an example of what good 
output looks like:

def greet(name: str) -> str:
    return f"Hello, {name}!"

Please ensure you follow this pattern in all your responses.
```
**After:**
```
Format code with proper indentation, matching existing style.

Example:
def greet(name: str) -> str:
    return f"Hello, {name}!"
```
The example is preserved verbatim; only the surrounding prose was compressed.

#### B. Conversation History Compression
- Replace completed sub-tasks with a one-line summary
- Drop assistant "thinking out loud" turns that were not acted upon
- Merge consecutive user messages with the same intent
- Replace large tool outputs with a short result summary — **but keep any code the tool produced**
- Keep: decisions made, errors encountered, user constraints, output artifacts, code changes
- Drop: pleasantries, redundant confirmations, intermediate reasoning that led nowhere

**Pattern:**
```
[COMPRESSED HISTORY]
- User asked to refactor auth module. Completed. Files changed: auth.py, tests/test_auth.py.
- User requested DB connection pooling. Blocked: missing env var DB_POOL_SIZE.
[CURRENT TASK]
...
```

**Tool output compression — right way:**
```
# Before (500 tokens of raw JSON)
{"users": [{"id": 1, "name": "Alice", ...}, {"id": 2, ...}, ... 47 more records]}

# After (10 tokens — code result is preserved separately if used)
[Tool result: returned 49 user records, IDs 1–49]
```
If the code written during a tool call is referenced later, keep it verbatim in the history.

#### C. Code Context Compression
Code itself is never rewritten. Only surrounding scaffolding is reduced:

- Strip comments that restate what the code does (keep WHY comments and non-obvious invariants)
- Remove blank lines beyond one between logical blocks
- For **unused** sections: replace with a placeholder — `[... 80 lines omitted: class PaymentProcessor — not relevant to this task ...]`
- For **read-only reference** code: keep function signatures + docstrings; omit implementations **only if** the caller doesn't need to understand the internals
- Remove import blocks when every import is obviously inferable from usage
- **Never** change variable names, types, logic, or formatting in active code

#### D. Document / Text Compression
- Extract only the sections relevant to the current task; omit the rest with `[Section "X" omitted — not relevant]`
- Replace long lists of examples with `e.g., X, Y, Z (N more omitted)`
- Convert tables with many empty cells to filtered key→value lists
- Summarize intro/background paragraphs to one sentence

#### E. Tool Definition Compression
- Shorten `description` fields: one sentence, no inline examples if examples live elsewhere
- Remove optional parameters not used in this workflow
- Merge near-identical tools into one with a `mode` or `action` parameter
- Strip `title` fields from JSON Schema properties (they're cosmetic, not functional)

---

### 3. Route Simple Tasks to Local Small LLMs

Not all sub-tasks need a frontier model. For agent workflows, identify tasks by complexity and route accordingly:

| Task type | Recommended model | Why |
|---|---|---|
| Text classification, intent detection | Local: `llama3.2:3b`, `phi4-mini`, `gemma3:4b` | Simple pattern matching — $0 cost |
| Boilerplate generation (CRUD, getters) | Local: `qwen2.5-coder:7b`, `deepseek-coder:6.7b` | Code templates, not novel reasoning |
| Summarization of long documents | Local: `mistral:7b`, `llama3.2:3b` | Extractive compression, no deep reasoning needed |
| Format conversion (JSON↔YAML, CSV→table) | Local: any small model | Deterministic transformation |
| Regex / simple string operations | No LLM — use code | Pure computation |
| Complex reasoning, architecture decisions | Cloud: Sonnet 4.6 / Opus 4.7 | Requires broad knowledge |
| Code review, security analysis | Cloud: Sonnet 4.6 | Subtle reasoning required |
| Novel code generation (non-boilerplate) | Cloud: Sonnet 4.6 | Quality matters |

#### How to run local models (Ollama)

```bash
# Install Ollama (macOS)
brew install ollama

# Pull a small coding model
ollama pull qwen2.5-coder:7b

# Pull a small general model
ollama pull llama3.2:3b

# Run inference
ollama run llama3.2:3b "Classify this text as positive/negative: 'The build failed again'"
```

#### Routing pattern for agent code

```python
def route_task(task: str, complexity: str) -> str:
    """Route to local or cloud model based on task complexity."""
    local_tasks = {"classify", "summarize", "format", "boilerplate"}
    if complexity == "simple" or task in local_tasks:
        return "ollama/llama3.2:3b"       # $0 — runs locally
    elif complexity == "medium":
        return "claude-haiku-4-5"          # $0.80/1M tokens
    else:
        return "claude-sonnet-4-6"         # $3.00/1M tokens
```

#### Cost comparison (input + output, per 1M tokens)

| Model | Cost | Best for |
|---|---|---|
| Local (Ollama) | $0 | Simple, high-volume tasks |
| Haiku 4.5 | ~$1.60 avg | Fast, cheap, moderate quality |
| Sonnet 4.6 | ~$7.50 avg | Complex tasks, production quality |
| Opus 4.7 | ~$37.50 avg | Hardest problems only |

---

### 4. Estimate Savings

After compressing, report the token reduction:

```
Original: ~1,840 tokens
Compressed: ~620 tokens
Savings: ~1,220 tokens (66%) — approx $0.0037 saved per call at Sonnet 4.6 input pricing

Protected (unchanged): 3 code blocks, 2 examples
Prose reduction: 71% | Code reduction: 0%
```

Use this rough token estimator: **1 token ≈ 4 characters** (English text).

### 5. Output the Compressed Version

Deliver the compressed artifact clearly labeled, ready to copy-paste:

```
--- COMPRESSED OUTPUT ---
<compressed content here>
--- END ---
```

If compression involved judgment calls, list warnings:
```
⚠ Dropped: intro paragraph (lines 1–12) — re-add if agent needs background context
⚠ Summarized: tool output JSON — original preserved in memory if needed
✓ Protected: code block at lines 34–52 — unchanged
✓ Protected: 3 few-shot examples — unchanged
```

---

## Compression Heuristics (Quick Reference)

### Safe to compress (prose)
| Pattern | Action |
|---|---|
| "Please note that..." | Remove — state the constraint directly |
| "As an AI language model..." | Always remove |
| Repeated constraints | Keep one, drop duplicates |
| "The following is a list of..." | Delete — just give the list |
| Closing pleasantries in history | Remove |
| Verbose JSON with null/default fields | Strip nulls and defaults |
| Multi-sentence intro for a bullet list | Replace with the list title |

### Never compress
| Pattern | Reason |
|---|---|
| Any code block | Correctness is token-precise |
| Few-shot examples | Format and content both matter |
| Regex patterns | One wrong char breaks them |
| Numbers, IDs, thresholds | Silent bugs from truncation |
| Error messages | Every word is diagnostic signal |
| Security rules | Must be complete and literal |

---

## Examples

- "Compress my system prompt" → apply technique A (protect any embedded code/examples)
- "This conversation is getting expensive, compress the history" → apply technique B
- "Reduce tokens in this context window" → identify content types, apply A–E as needed
- "My agent costs too much per run, help me optimize" → audit prompt + tools + task routing; apply all relevant techniques
- "What tasks in my workflow could run locally?" → apply routing analysis in step 3
