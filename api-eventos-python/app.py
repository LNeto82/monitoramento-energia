from fastapi import FastAPI, Request
import redis
import json
from rabbitmq_consumer import consume_rabbitmq

app = FastAPI()
redis_client = redis.Redis(host='localhost', port=6379, db=0)
EVENT_KEY = 'eventos'

@app.post("/event")
async def receive_event(request: Request):
    body = await request.json()
    eventos = redis_client.get(EVENT_KEY)
    eventos_list = json.loads(eventos) if eventos else []
    eventos_list.append(body)
    redis_client.set(EVENT_KEY, json.dumps(eventos_list))
    return {"status": "evento armazenado"}

@app.get("/events")
def get_events():
    eventos = redis_client.get(EVENT_KEY)
    return json.loads(eventos) if eventos else []

consume_rabbitmq()
