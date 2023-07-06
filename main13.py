import asyncio
import time


class Countdown:
    def __init__(self, count: int, name: str):
        self.count = count
        self.name = name

    async def start(self):
        mass = []
        for i in range(1, self.count + 1):
            mass.append(self.timer(i))
        await asyncio.gather(*mass)
        print(self.name + ' done')

    async def timer(self, n):
        await asyncio.sleep(n)
        print(self.name + ' ' + str(self.count + 1 - n))


async def main():
    cd = Countdown(5, 'First')
    await cd.start()

asyncio.run(main())
