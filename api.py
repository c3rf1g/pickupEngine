from fastapi import FastAPI, Query
from pydantic import BaseModel
from concurrent.futures import ThreadPoolExecutor
import asyncio
from bot import download_image, process_photo

app = FastAPI()
executor = ThreadPoolExecutor()


class Result(BaseModel):
    text: str


@app.post("/process_photo", response_model=Result)
async def process_photo_endpoint(file_id: str = Query(...)):
    loop = asyncio.get_event_loop()
    photo_data = await download_image(file_id)
    result = await loop.run_in_executor(executor, process_photo, photo_data)
    return {"text": result}
