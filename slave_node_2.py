from fastapi import FastAPI
from pydantic import BaseModel
import logging

app = FastAPI()
replicated_log = []
logging.basicConfig(level=logging.INFO)


class Message(BaseModel):
    message: str


@app.post("/replicate")
def replicate_message(message: Message):

    replicated_log.append(message.message)
    logging.info(f"Replicated message: {message.message}")
    return {"status": "OK"}


@app.get("/messages")
def get_messages():
    return {"messages": replicated_log}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8002)

