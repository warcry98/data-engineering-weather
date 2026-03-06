import asyncio
import aiohttp
import time
import dlt
import logging
from datetime import datetime, timezone

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

BASE_URL = "https://api.bmkg.go.id/publik/prakiraan-cuaca"

ADM4_LIST = [
    "34.01.07.2005"
]

RATE = 60
PERIOD = 60

TEST_MODE = True

class TokenBucket:

    def __init__(self, rate, period):
        self.capacity = rate
        self.tokens = rate
        self.period = period
        self.updated = time.monotonic()

    async def consume(self):

        while True:
            now = time.monotonic()
            elapsed = now - self.updated

            refill = elapsed * (self.capacity / self.period)

            if refill > 0:
                self.tokens = min(self.capacity, self.tokens + refill)
                self.updated = now

            if self.tokens >= 1:
                self.tokens -= 1
                logging.info(f"Token consumed | remaining={self.tokens:.2f}")
                return

            await asyncio.sleep(0.05)


bucket = TokenBucket(RATE, PERIOD)


async def fetch(session, adm4):

    start = time.time()

    await bucket.consume()

    url = f"{BASE_URL}?adm4={adm4}"

    logging.info(f"Request start | adm4={adm4}")

    async with session.get(url) as resp:

        data = await resp.json()

        duration = time.time() - start

        logging.info(
            f"Request done | adm4={adm4} | status={resp.status} | time={duration:.2f}s"
        )

        return {
            "adm4": adm4,
            "ingested_at": datetime.now(timezone.utc),
            "payload": data
        }


@dlt.resource(
    name="bmkg_weather_raw",
    write_disposition="append"
)
def bmkg_weather():

    async def runner():

        async with aiohttp.ClientSession() as session:

            tasks = []

            for adm4 in ADM4_LIST:
                tasks.append(fetch(session, adm4))

            logging.info(f"Launching {len(tasks)} tasks")

            results = await asyncio.gather(*tasks)

            return results

    results = asyncio.run(runner())

    for r in results:
        logging.info(f"Yielding record for adm4={r['adm4']}")
        yield r


def run():

    if TEST_MODE:
        logging.info("TEST MODE")

        for row in bmkg_weather():
            logging.info(row)

    else:
        pipeline = dlt.pipeline(
            pipeline_name="bmkg_weather",
            destination="postgres",
            dataset_name="raw"
        )

        pipeline.run(bmkg_weather())

if __name__ == "__main__":
    run()