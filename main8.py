import requests
import asyncio
import aiohttp
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


async def downloadcat(session, n, url):
    name = r"C:\Users\olymp\timurnab\cats\cat"
    name += str(n) + url[len(url)-4:len(url)]
    response = await session.get(url)
    img_bytes = await response.read()
    file = open(name, 'wb')
    file.write(img_bytes)
    file.close()
    print(f'cat {n} done!')


async def main():
    masdown = []
    async with aiohttp.ClientSession() as session:
        response = await session.get('https://api.thecatapi.com/v1/images/search?limit=10')
        response_bytes = await response.json()
        for i in range(10):
            masdown.append(downloadcat(session, i + 1, response_bytes[i]['url']))
        await asyncio.gather(*masdown)
        response.release()


asyncio.run(main())