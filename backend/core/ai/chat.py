from langchain_ollama.chat_models import ChatOllama

from ai.available_models import AvailableChatModel
from ai.prompts import CHAT_MODEL_SYSTEM_PROMPT


async def chat(
    messages,
    model=AvailableChatModel.QWEN25_7B,
    system_prompt=CHAT_MODEL_SYSTEM_PROMPT):

    messages = [('system', system_prompt)] + messages
    llm = ChatOllama(model=model)

    async for chunk in llm.astream(messages):
        yield chunk.content
