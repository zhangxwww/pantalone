from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from ai.chat import chat
from libs.decorator.log import log_request
import api_model


router = APIRouter(tags=['ai'])

@router.post('/ai/chat/stream')
@log_request
async def chat_stream(request: api_model.ChatMessageRequestData):
    messages = request.messages

    messages = [(m['role'], m['content']) for m in messages]

    async def message_generator():
        async for data in chat(messages):
            yield f'{data}\n'

    return StreamingResponse(message_generator(), media_type='text/event-stream')
