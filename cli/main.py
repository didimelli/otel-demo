import os

import asyncclick as click
from aiokafka import AIOKafkaProducer
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from aiokafka_instrumentation import KafkaInstrumentor

resource = Resource(attributes={SERVICE_NAME: "cli"})
provider = TracerProvider(resource=resource)
processor = BatchSpanProcessor(
    OTLPSpanExporter(endpoint="http://127.0.0.1:4318/v1/traces")
)
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)
tracer = trace.get_tracer("my.tracer.name")
KafkaInstrumentor().instrument()


@click.command()
@click.option("--message", help="Message to publish.", required=True)
@tracer.start_as_current_span("publish_topic_1")
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
