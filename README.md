## Django Server Sent Event Demo

This repository is a proof of concept for an async [`StreamingHttpResponse`](https://docs.djangoproject.com/en/4.2/ref/request-response/#django.http.StreamingHttpResponse) that could be used as a building block for [server-sent events](https://en.wikipedia.org/wiki/Server-sent_events) without using [Django Channels](https://channels.readthedocs.io/).

This project contains only a single view that sends the current date every seconds:

```python
async def clock(request):

    async def event_stream():
        while True:
            yield f'data: The server time is: {timezone.now()}\n\n'.encode("utf-8")
            await asyncio.sleep(1)

    return StreamingHttpResponse(event_stream(), content_type='text/event-stream')
```

See the related Stack Overflow thread: https://stackoverflow.com/q/63316840/1164966