from fastapi import FastAPI, WebSocket, Request, Response
from starlette.responses import StreamingResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session
# from database import SessionLocal, User
from typing import Optional
from pathlib import Path
import os

app = FastAPI()

class UserRequest(BaseModel):
    username: str
    email: str

@app.get("/stream/{video_id}")
async def stream_video(request: Request, video_id: str):
    video_path = Path("test.mp4")
    if not video_path.exists():
        return Response(status_code=404, media_type="application/json", content='{"error": "Video not found"}')

    video_size = os.path.getsize(video_path)
    range_header = request.headers.get("range")

    if not range_header:
        headers = {
            "Content-Range": f"bytes */{video_size}",
            "Content-Type": "video/mp4",
            "Accept-Ranges": "bytes"
        }
        return Response(status_code=416, headers=headers, media_type="video/mp4")

    byte_range = range_header.replace("bytes=", "").split("-")
    start = int(byte_range[0])
    end = video_size - 1 if byte_range[1] == '' else int(byte_range[1])

    chunk_size = end - start + 1
    headers = {
        "Content-Range": f"bytes {start}-{end}/{video_size}",
        "Content-Type": "video/mp4",
        "Accept-Ranges": "bytes",
        "Content-Length": str(chunk_size)
    }

    async def file_iterator_range():
        with open(video_path, "rb") as f:
            f.seek(start)
            remaining = chunk_size
            while remaining > 0:
                chunk = f.read(min(remaining, 1024 * 1024))
                if not chunk:
                    break
                yield chunk
                remaining -= len(chunk)

    async def file_iterator_full():
        with open(video_path, "rb") as f:
            while True:
                chunk = f.read(1024 * 1024)
                if not chunk:
                    break
                yield chunk

    if range_header:
        return StreamingResponse(file_iterator_range(), status_code=206, headers=headers, media_type="video/mp4")
    else:
        return StreamingResponse(file_iterator_full(), headers={"Content-Length": str(video_size), "Content-Type": "video/mp4"}, media_type="video/mp4")

@app.websocket("/chat")
async def chat(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")
