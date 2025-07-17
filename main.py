from fastapi import FastAPI
from pydantic import BaseModel
from starlette.requests import Request
from starlette.responses import Response, JSONResponse
from typing import List

app = FastAPI()

class EventModel(BaseModel):
    name: str
description: str
start_date: str
end_date: str

events_store: List[EventModel] = []

def serialized_stored_events():
    events_converted = []
    for event in events_store:
        events_converted.append(event.model_dump())
    return events_converted
@app.get("/")
def root(request: Request):
    api_key = request.headers.get("x-api-key")
    if api_key != "12345678":
        return JSONResponse(content={"detail": "Clé API non reconnue"},status_code=403)
    with open("welcome.html", "r", encoding="utf-8") as file:
        html_content = file.read()
    return Response(content=html_content, status_code=200, media_type="text/html")

@app.get("/hello")
def hello(request: Request):
    accept_headers = request.headers.get("Accept")
    if accept_headers not in ("text/html", "text/plain"):
        return JSONResponse(content={"message": "Unsupported Media Type"}, status_code=400)
    return JSONResponse(content={"message": "Hello, world!"}, status_code=200)

@app.get("/events")
def list_events():
    return {"events": serialized_stored_events()}

@app.post("/events")
def add_events(new_events: List[EventModel]):
    events_store.extend(new_events)
    return {"events": serialized_stored_events()}

@app.put("/events")
def update_events(incoming_events: List[EventModel]):
    for incoming in incoming_events:
        for stored in events_store:
            if stored.name == incoming.name:
                stored.name = incoming.name
                stored.description = incoming.description
                stored.start_date = incoming.start_date
                stored.end_date = incoming.end_date
    return {"events": serialized_stored_events()}

@app.get("/{full_path:path}")
def catch_all(full_path: str):
    with open("404.html", "r", encoding="utf-8") as file:
        html_content = file.read()
    return Response(content=html_content, status_code=404, media_type="text/html")
