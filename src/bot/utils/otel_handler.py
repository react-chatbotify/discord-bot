"""
OpenTelemetry Logging Handler Module.

Sets up the OpenTelemetry LoggerProvider, exporter, and processor.
Defines OTELHandler for Python's logging module that forwards logs
to the OTEL Collector in structured format.

The code snippet below is taken from the otel python example here:
https://github.com/open-telemetry/opentelemetry-python/tree/main/docs/examples/logs
"""

import logging

from opentelemetry import trace
from opentelemetry._logs import set_logger_provider
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import (
    OTLPLogExporter,
)
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter,
)

from bot.config.logging import logging_config

trace.set_tracer_provider(TracerProvider())
trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))

logger_provider = LoggerProvider(
    resource=Resource.create(
        {
            "service.name": "rcb-discord-bot",
        }
    ),
)
set_logger_provider(logger_provider)

exporter = OTLPLogExporter(endpoint=logging_config.otel_endpoint, insecure=True)
logger_provider.add_log_record_processor(BatchLogRecordProcessor(exporter))
otel_handler = LoggingHandler(level=logging.NOTSET, logger_provider=logger_provider)
