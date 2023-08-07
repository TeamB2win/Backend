import os

import httpx

async def request_dl_server(data):
    url = os.path.join(os.environ["DL_URL"], "api", "inference")
    print(url)
    async with httpx.AsyncClient() as client:
        response = await client.post(url, data=data.json())
        print(response)

    return response