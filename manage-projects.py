import os
from anthropic import Anthropic
from auth import key

# Initialize the client API
client = Anthropic(api_key=key)

# 1. Personalized instructions (similar to the Project's System Prompt / Custom Instructions)
system_instructions = """
You are an assistant specializing in software architecture and GIS systems.
Always provide responses that focus on clean, modular code that adheres to the repository's guidelines.
"""

# 2. Load local files context (as same as the Knowledge Base of the Project)
def load_project_folder(folder_path):
    context_parts = []
    if os.path.exists(folder_path):
        for root, _, files in os.walk(folder_path):
            for file in files:
                # Filtra apenas extensões relevantes
                if file.endswith((".md", ".txt", ".py", ".json")):
                    full_path = os.path.join(root, file)
                    try:
                        with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                            content = f.read()
                            context_parts.append(f"=== ARQUIVO: {file} ===\n{content}")
                    except Exception as e:
                        print(f"Erro ao ler {file}: {e}")
    return "\n\n".join(context_parts)

# Example: Loading an architecture document or internal documentation
context_docs = load_project_folder("docs")

# 3. Create the request combining instructions and the files' context
user_prompt = "What are the best practices for building a simple and consistent data architecture based on mcp agents for 32 simultaneous users?"

response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=2048,
    system=f"{system_instructions}\n\n--- REFERENCE CONTEXT OF THE PROJECT ---\n{context_docs}",
    messages=[
        {"role": "user", "content": user_prompt}
    ]
)

print(response.content[0].text)