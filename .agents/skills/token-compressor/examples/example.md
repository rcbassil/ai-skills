# Token Compressor Examples

This document demonstrates how the **Token Compressor** skill handles various scenarios, from prompt optimization to intelligent task routing.

## 1. Prompt Compression (Prose Optimization)

### Original (Verbose)
```text
You are a helpful assistant. Your job is to help the user with their questions. 
Please make sure to always be polite and professional. It is very important that 
you never provide information that could be harmful. Always cite your sources 
when possible and make sure your answers are accurate.

Here is an example of a good response:
```json
{"status": "success", "message": "Source cited: Wikipedia."}
```
Please follow this style.
```

### Compressed
```text
Helpful assistant. Be polite & professional. Never provide harmful info. Cite sources. Be accurate.

Example:
```json
{"status": "success", "message": "Source cited: Wikipedia."}
```
Follow this style.
```
**Savings:** ~55% reduction in prose. Code example preserved 100%.

---

## 2. Conversation History Compression

### Original (Messy Thread)
- **User**: Can you refactor the auth module?
- **Assistant**: Sure! I'll look into it. I see you are using JWT. I will add a new middle-ware for refresh tokens.
- **Assistant**: [Writes 200 lines of code]
- **Assistant**: Is that okay?
- **User**: Yes, but I also need DB connection pooling.
- **Assistant**: I can do that. What is the pool size?
- **User**: Make it 10.
- **Assistant**: [Writes 50 lines of code]
- **Assistant**: Done! Anything else?

### Compressed History
```text
[COMPRESSED HISTORY]
- Task: Refactored auth module. Added JWT refresh token middleware. (Verified)
- Task: Added DB connection pooling (size: 10). (Verified)
[CURRENT CONTEXT]
...
```
**Savings:** Replaced 250+ tokens of turn-taking and pleasantries with a ~20 token summary.

---

## 3. Tool Definition Compression

### Original (Redundant Fields)
```json
{
  "name": "get_weather",
  "description": "This tool allows you to retrieve the current weather for a specific location. It is very useful for checking temperatures.",
  "parameters": {
    "type": "object",
    "properties": {
      "location": {
        "type": "string",
        "title": "The City Name",
        "description": "The name of the city, for example 'London' or 'Paris'."
      },
      "unit": {
        "type": "string",
        "enum": ["celsius", "fahrenheit"],
        "default": "celsius",
        "description": "The unit of measurement to return the temperature in."
      }
    }
  }
}
```

### Compressed Tool
```json
{
  "name": "get_weather",
  "description": "Retrieve current weather for a location.",
  "parameters": {
    "type": "object",
    "properties": {
      "location": { "type": "string", "description": "City name." },
      "unit": { "type": "string", "enum": ["c", "f"], "description": "Unit (c/f)." }
    }
  }
}
```
**Savings:** ~40% token reduction by stripping cosmetics (`title`, `default`) and shortening descriptions.

---

## 4. Sub-Task Routing (Cost Optimization)

When asked: *"Help me optimize my automation pipeline cost."*

**Analysis:**
- **Step 1: Text Sanitization** → Route to `llama3.2:3b` ($0)
- **Step 2: Pydantic Model Generation** → Route to `qwen2.5-coder:7b` ($0)
- **Step 3: Security Policy Analysis** → Route to `claude-3-5-sonnet` ($3.00/1M)

**Recommendation:**
> "By offloading the first two steps to local models via Ollama, you reduce per-run costs by 60% with zero loss in quality for the final security audit."
