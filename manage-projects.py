import os
from anthropic import Anthropic
from auth import key
from models import MODELS, CHEAPEST_MODEL  # Importa o dicionário e os atalhos

# Initialize the client API
client = Anthropic(api_key=key)

# 1. Personalized instructions (similar to the Project's System Prompt / Custom Instructions)
system_instructions = """
                    Talk about the first principles on the optics of a software architect. Be as much as didatic possible.
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
                            context_parts.append(f"=== FILE: {file} ===\n{content}")
                    except Exception as e:
                        print(f"Erro ao ler {file}: {e}")
    return "\n\n".join(context_parts)

# Example: Loading an architecture document or internal documentation
context_docs = load_project_folder("docs")

# 3. Create the request combining instructions and the files' context
user_prompt = "How does first principles theory works for a software architect?"

response = client.messages.create(
    model= MODELS["haiku-5.5"],  # Using the cheapest model for cost efficiency
    max_tokens=4096,
    system=f"{system_instructions}\n\n--- REFERENCE CONTEXT OF THE PROJECT ---\n{context_docs}",
    messages=[{"role": "user", "content": user_prompt}]
)

for block in response.content:
    if hasattr(block, "text"):
        print(block.text)
