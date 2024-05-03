import os

import anyio
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer


async def main() -> None:
    consumer = AIOKafkaConsumer(
        os.environ["TOPIC_1"],
        bootstrap_servers=[
            f"{os.environ['KAFKA_HOST']:{os.environ['KAFKA_PORT']}}",
        ],
    )
    producer = AIOKafkaProducer(
        bootstrap_servers=[
            f"{os.environ['KAFKA_HOST']:{os.environ['KAFKA_PORT']}}",
        ],
    )
    async with producer as producer:
        async with consumer as consumer:
            async for msg in consumer:
                print(msg.value)
                await producer.send(os.environ["TOPIC_2"], msg.value * 2)


if __name__ == "__main__":
    anyio.run(main)
