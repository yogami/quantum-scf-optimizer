import httpx
import asyncio

urls = [
    "https://quantum-scf-optimizer.up.railway.app/api/health",
    "https://quantum-scf-optimizer-production.up.railway.app/api/health",
    "https://accurate-fulfillment-production.up.railway.app/api/health",
    "https://quantum-scf-optimizer-accurate-fulfillment-production.up.railway.app/api/health",
    "https://quantum-scf-optimizer-accurate-fulfillment.up.railway.app/api/health"
]

async def check_url(url):
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, timeout=5.0)
            print(f"{url} -> {resp.status_code}")
            if resp.status_code == 200:
                print(f"SUCCESS: {url} is UP!")
                print(resp.json())
    except Exception as e:
        print(f"{url} -> Error: {e}")

async def main():
    tasks = [check_url(url) for url in urls]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
