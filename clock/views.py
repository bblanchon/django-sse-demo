import asyncio

# By design asyncio does not allow its event loop to be nested.
# Trying to do so will give the error "RuntimeError: This event loop is already running".
# This library solves that problem.
import nest_asyncio

from django.http.response import StreamingHttpResponse


class AsyncStreamingHttpResponse(StreamingHttpResponse):

    def __init__(self, streaming_content=(), *args, **kwargs):
        sync_streaming_content = self.get_sync_iterator(streaming_content)
        super().__init__(streaming_content=sync_streaming_content, *args, **kwargs)

    @staticmethod
    async def convert_async_iterable(stream):
        """Accepts async_generator and async_iterator"""
        return iter([chunk async for chunk in stream])

    def get_sync_iterator(self, async_iterable):
        nest_asyncio.apply()

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(self.convert_async_iterable(async_iterable))
        return result


async def clock_view(request):

    async def event_stream():
        while True:
            yield 'data: The server time is: %s\n\n' % datetime.datetime.now()
            await asyncio.sleep(1)

    return AsyncStreamingHttpResponse(event_stream(), content_type='text/event-stream')