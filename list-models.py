import os
from anthropic import Anthropic
from auth import key

# Inicializa o cliente da API
client = Anthropic(api_key=key)

try:
    # A listagem retorna um objeto paginado; usamos .data para acessar os modelos
    response = client.models.list()
    print("Modelos disponíveis na sua conta:")
    for model in response.data:
        print(f"- ID: {model.id}")
except Exception as e:
    print(f"Erro ao listar modelos: {e}")