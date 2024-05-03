import os

import asyncclick as click
from aiokafka import AIOKafkaProducer


@click.command()
@click.option("--message", help="Message to publish.", required=True)
async def publish_topic_1(message: str) -> None:
    producer = AIOKafkaProducer(
        bootstrap_servers=[
            f"{os.environ['KAFKA_HOST']:{os.environ['KAFKA_PORT']}}",
        ]
    )
    async with producer as producer:
        await producer.send(os.environ["TOPIC_1"], message.encode())


if __name__ == "__main__":
    publish_topic_1()
