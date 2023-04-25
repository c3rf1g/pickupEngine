import asyncio
import datetime

import httpx

async def send_request(file_id: str):
    timeout = httpx.Timeout(10.0, connect=10.0, read=30.0)
    async with httpx.AsyncClient(timeout=timeout) as client:
        response = await client.post("https://tgpickuphelper.herokuapp.com/process_photo", params={"file_id": file_id})
        print(f"Response for file_id {file_id}: {response.text}")
        print(datetime.datetime.now())

async def main():
    file_ids = [f"AgACAgIAAxkBAAP_ZEU9JGetRWUE7m0UnhS-PcEyWf4AAtvEMRsd-ihK0_dy7pG-FJABAAMCAAN5AAMvBA" for i in range(5)]
    print("start", datetime.datetime.now())
    # Отправляем все запросы одновременно
    tasks = [asyncio.create_task(send_request(file_id)) for file_id in file_ids]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())