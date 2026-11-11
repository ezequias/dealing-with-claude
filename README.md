# Dealing with Claude

This repository is a small Python experiment for working with Anthropic models and grounding prompts with local project documentation. It is not a full application with a web UI or package install flow; it is more of a lightweight prompt-and-context playground.

The project combines three ideas:

- a shared API key module
- a model alias registry
- a document loader that injects local Markdown/Python context into a model request

## Project purpose

The scripts in this repository let you:

- list the models available to your Anthropic account
- pick a model by a short alias such as `haiku-5.5` or `sonnet-5.5`
- build prompts that include project documentation as system context
- ask architecture and design questions grounded in local files such as the software design notes in the `docs/` folder

In other words, this project is designed to demonstrate how to use Anthropic's API in a simple, readable way while keeping the prompt context close to the codebase.

## File overview

### `auth.py`

This file holds the Anthropic API key used by the scripts.

```python
from anthropic import Anthropic
from auth import key

client = Anthropic(api_key=key)
```

In a real production setup, this kind of secret should usually come from an environment variable or a `.env` file rather than being committed directly. The current repository keeps it as a simple module for demonstration purposes.

### `models.py`

This file defines a dictionary of human-friendly model aliases and their exact Anthropic model IDs.

```python
MODELS = {
    "haiku-5.5": "claude-haiku-5-5",
    "sonnet-5.5": "claude-sonnet-5-5",
    "opus-5.5": "claude-opus-5-5",
    ...
}
```

It also exposes convenience values:

- `CHEAPEST_MODEL`
- `DEFAULT_MODEL`
- `MOST_CAPABLE_MODEL`

This makes scripts easier to read and avoids hard-coding raw model IDs in multiple places.

### `list-models.py`

This script calls Anthropic's `client.models.list()` endpoint and prints each available model ID.

It is the simplest example in the project and is useful to confirm that the API key is valid and that the account can access the expected models.

### `manage-projects.py`

This file appears to be a near-duplicate of `list-models.py` and serves the same purpose: it initializes the Anthropic client and prints available models. In a larger project, it could be expanded into a richer "project management" utility, but in the current form it is essentially a model-listing helper.

### `first-principles.md`

This file is a generated or curated document about first-principles reasoning for software architects. It explains how to reason from fundamentals rather than copying patterns used elsewhere.

It is a good example of the kind of knowledge the project can feed into a prompt to influence the LLM response.

### `docs/`

This folder contains architecture and design reference material, including:

- `software-design-principles.md`
- `software-design-principles-java.md`

These documents provide context about software design habits such as SOLID, DRY, KISS, YAGNI, separation of concerns, and composition over inheritance. The project uses these docs as reference material for architectural guidance.

## How the main prompt script works

The key prompt-driven example is the script that creates a Claude request with project context. The logic is conceptually:

1. Load the API key from `auth.py`
2. Initialize the Anthropic client
3. Build a system prompt that defines how the model should respond
4. Read local files from a folder such as `docs/`
5. Inject the file contents into the request as additional context
6. Send a user question and print the model result

### Example flow

```python
def load_project_folder(folder_path):
    context_parts = []
    if os.path.exists(folder_path):
        for root, _, files in os.walk(folder_path):
            for file in files:
                if file.endswith((".md", ".txt", ".py", ".json")):
                    full_path = os.path.join(root, file)
                    with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                        context_parts.append(f"=== ARQUIVO: {file} ===\n{content}")
    return "\n\n".join(context_parts)
```

This function recursively scans a folder and builds a large text blob containing the relevant project files. That blob is then added to the system prompt, so the model answers using the project's own documentation as background knowledge.

## Why this project is useful

This repository is useful as a learning and experimentation tool because it shows the building blocks of an LLM-based assistant without introducing a large framework or heavy architecture. It demonstrates:

- how to authenticate to an LLM API
- how to keep model versions centralized
- how to use local docs as prompt context
- how to ask a model to answer using a specific conceptual lens

It is especially relevant for use cases where you want a model to behave like a software architect or design reviewer, using your own notes and principles as grounding material.

## Typical usage

From the project root:

```bash
# activate the project virtual environment
source env/Scripts/activate

# list available Anthropic models
python list-models.py
```

If you want to build a prompt from local documentation, you would adapt the pattern used in the main request example and provide a custom user question.

## Recommended next steps

If this project were expanded, the most natural improvements would be:

- move the API key to an environment variable
- add a command-line interface for selecting a model and asking questions
- support reading additional folders or file types
- add logging or output files for requests and responses
- separate the prompt-building logic into a reusable module

## Summary

This repository is a compact Anthropic API starter project with a design-focused twist. It uses local documentation as prompt context and helps explore how large language models can act as architecture and design assistants. The code is intentionally small and readable, which makes it a good example of how to start integrating AI into a software engineering workflow.
