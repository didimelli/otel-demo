import os

import anyio
from aiokafka import AIOKafkaConsumer


async def main() -> None:
    consumer = AIOKafkaConsumer(
        os.environ["TOPIC_2"],
        bootstrap_servers=[
            f"{os.environ['KAFKA_HOST']:{os.environ['KAFKA_PORT']}}",
        ],
    )
    async with consumer as consumer:
        async for msg in consumer:
            print(msg.value)


if __name__ == "__main__":
    anyio.run(main)
