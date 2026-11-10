# models.py
# Dicionário mapeando apelidos amigáveis aos IDs exatos dos modelos da Anthropic

MODELS = {
    # Geração 5.5 (Mais recentes)
    "haiku-5.5": "claude-haiku-5-5",
    "sonnet-5.5": "claude-sonnet-5-5",
    "opus-5.5": "claude-opus-5-5",

    # Geração 5.0 a 5.2 (Fable, Opus, Sonnet)
    "fable-5.2": "claude-fable-5-2",
    "fable-5.1": "claude-fable-5-1",
    "fable-5.0": "claude-fable-5",
    "sonnet-5.0": "claude-sonnet-5",
    "opus-5.0": "claude-opus-5",

    # Geração 4 (Modelos com versão específica)
    "opus-4.8": "claude-opus-4-8",
    "opus-4.7": "claude-opus-4-7",
    "sonnet-4.6": "claude-sonnet-4-6",
    "opus-4.6": "claude-opus-4-6",
    "opus-4.5": "claude-opus-4-5-20251101",
    "haiku-4.5": "claude-haiku-4-5-20251001",
}

# Aliases de conveniência para desenvolvimento rápido
DEFAULT_MODEL = MODELS["sonnet-5.5"]
CHEAPEST_MODEL = MODELS["haiku-5.5"]
MOST_CAPABLE_MODEL = MODELS["opus-5.5"]