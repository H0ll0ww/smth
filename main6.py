import asyncio
from random import random


async def cat(n):
    print('cat', n,  'is downloading')
    await asyncio.sleep(random()+1)
    print('cat', n, 'has been dowloaded')

async def main():
    a = (cat(i) for i in range(1,11))
    await asyncio.gather(*a)


asyncio.run(main())