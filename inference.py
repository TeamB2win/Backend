import asyncio
import aiohttp
import asyncpg
from fastapi import FastAPI

app = FastAPI()
# data = [{'type':'긴급'},{'type':'종합'}]
dl_container_url = "http://dl_container:8000/api/inference"

async def create_pool():
    # PostgreSQL 데이터베이스와 연결하는 풀 생성
    return await asyncpg.create_pool(dsn="postgresql://user:password@postgres_container/db_name")

@app.on_event("startup")
async def startup_event():
    # PostgreSQL 데이터베이스와 연결하는 풀 생성
    app.db_pool = await create_pool()

@app.on_event("shutdown")
async def shutdown_event():
    # PostgreSQL 데이터베이스와 연결 종료
    await app.db_pool.close()
    

async def fetch_result(session, data):
    async with session.post(dl_container_url, json=data) as response:
        return await response.json()

@app.get("/send_data")
async def send_data_to_dl_container(redis_pool):
    q = asyncio.PriorityQueue()

    # 반복문을 두개로 나누어 긴급 data를 먼저 await q.put() 더이상 없다면 나머지를 작업
    await q.put((1, high_priority))
    await q.put((2, low_priority))

    async with aiohttp.ClientSession() as session:
        while not q.empty():
            # 데이터 처리 상태를 PostgreSQL로부터 확인
            async with app.db_pool.acquire() as conn:
                processing_status = await conn.fetchval("SELECT status FROM processing_status")

            if processing_status == "processing":
                return {"message": "Data is being processed. Please try again later."}
            elif processing_status == "completed":
                _, data = await q.get()
            
                result_data = await fetch_result(session, data)
                print("inference 결과:", result_data)

    return {"message": "Data sending to DL container has completed"}

@app.post("/api/inference_result")
async def receive_inference_result(result_data: dict): 
    print("Received inference result:", result_data) 
    
    return {"message": "Inference result received in Backend."}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)