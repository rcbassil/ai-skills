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

*Note: This skill focuses on "Extractive" and "Prose-Terse" compression, ensuring that the AI agent's performance remains consistent while the overhead decreases.*
