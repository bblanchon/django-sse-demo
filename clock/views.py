import asyncio
from django.utils import timezone
from django.http.response import StreamingHttpResponse

async def clock(request):

    async def event_stream():
        while True:
            yield f'data: The server time is: {timezone.now()}\n\n'.encode("utf-8")
            await asyncio.sleep(1)

    return StreamingHttpResponse(event_stream(), content_type='text/event-stream')