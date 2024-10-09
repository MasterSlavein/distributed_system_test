from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import logging

app = FastAPI()
log = []
secondaries = ['http://0.0.0.0:8001', 'http://0.0.0.0:8002']
logging.basicConfig(level=logging.INFO)


class Message(BaseModel):
    message: str


@app.post("/append")
def append_message(message: Message):
    log.append(message.message)
    logging.info(f"Appended message to master log: {message.message}")

    # Replicate to secondaries
    for secondary in secondaries:
        try:
            logging.info(f"Replicating message to {secondary}")
            res = requests.post(f'{secondary}/replicate', json={'message': message.message})
            if res.status_code != 200:
                logging.error(f"Failed to replicate to {secondary}")
                raise HTTPException(status_code=500, detail="Replication failed")
        except Exception as e:
            logging.error(f"Error communicating with {secondary}: {str(e)}")
            raise HTTPException(status_code=500, detail="Replication failed")

    return {"status": "OK"}


@app.get("/messages")
def get_messages():
    return {"messages": log}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
