import os

import anyio
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from aiokafka_instrumentation import KafkaInstrumentor

resource = Resource(attributes={SERVICE_NAME: "service-1"})
provider = TracerProvider(resource=resource)
processor = BatchSpanProcessor(
    OTLPSpanExporter(endpoint="http://127.0.0.1:4318/v1/traces")
)
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)
tracer = trace.get_tracer("my.tracer.name")
KafkaInstrumentor().instrument()


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
                with tracer.start_as_current_span(
                    "consume-service-1", context=trace.set_span_in_context(msg.span)
                ):
                    await producer.send(os.environ["TOPIC_2"], msg.value * 2)


if __name__ == "__main__":
    anyio.run(main)
