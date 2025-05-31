import asyncio
import aio_pika
import redis
import json

def consume_rabbitmq():
    asyncio.create_task(_consume())

async def _consume():
    redis_client = redis.Redis(host='localhost', port=6379, db=0)
    EVENT_KEY = 'eventos'
    connection = await aio_pika.connect_robust("amqp://guest:guest@localhost/")
    channel = await connection.channel()
    queue = await channel.declare_queue("logistica", durable=True)

    async with queue.iterator() as qiterator:
        async for message in qiterator:
            async with message.process():
                body = json.loads(message.body)
                eventos = redis_client.get(EVENT_KEY)
                eventos_list = json.loads(eventos) if eventos else []
                eventos_list.append({"origem": "rabbitmq", **body})
                redis_client.set(EVENT_KEY, json.dumps(eventos_list))
