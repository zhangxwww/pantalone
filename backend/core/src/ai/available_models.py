import enum


class AvailableChatModel(enum.Enum):
    QWEN25_3B = "qwen2.5:3b-instruct"
    QWEN25_7B = "qwen2.5:7b"
    QWEN25_32B = "qwen2.5:32b-instruct-q2_K"
    QWEN25_72B = "qwen2.5:72b-instruct-q3_K_S"


class AvailableEmbeddingModel(enum.Enum):
    BGE_M3 = "bge-m3"
    NOMIC_EMBED_TEXT = "nomic-embed-text"


AVAILABLE_CHAT_MODELS = [e.value for e in AvailableChatModel]
AVAILABLE_EMBEDDING_MODELS = [e.value for e in AvailableEmbeddingModel]