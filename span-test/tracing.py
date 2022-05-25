import os
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace.export import (
    ConsoleSpanExporter,
    SimpleSpanProcessor,
    BatchSpanProcessor
)
#VARS
token = 'XnI5SWNNVv_uoCURsap5TA'
REALM = "us1"

os.environ["OTEL_EXPORTER_JAEGER_ENDPOINT"] = "https://ingest.{REALM}.signalfx.com/v2/trace".format(REALM=REALM)
os.environ["OTEL_RESOURCE_ATTRIBUTES"] = "nike-farshore-testing"
os.environ["SPLUNK_ACCESS_TOKEN"] = token
os.environ["OTEL_RESOURCE_ATTRIBUTES"] = "'service.version': '3.1', 'deployment.environment': 'testing'"
os.environ["OTEL_TRACES_EXPORTER"] = "jaeger-thrift-splunk"




trace.set_tracer_provider(
    TracerProvider(

    )
)





jaeger_exporter = JaegerExporter()

trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(jaeger_exporter)
)





tracer = trace.get_tracer(__name__)





with tracer.start_as_current_span("foo"):
    with tracer.start_as_current_span("bar"):
        with tracer.start_as_current_span("baz"):
            print("Hello world from OpenTelemetry Python!")