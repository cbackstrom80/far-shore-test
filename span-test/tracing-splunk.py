from splunk_otel.tracing import start_tracing

start_tracing()

# Also accepts optional config options:
# start_tracing(
#   service_name='my-python-service',
#   span_exporter_factories=[OTLPSpanExporter]
#   access_token='',
#   max_attr_length=12000,
#   trace_response_header_enabled=True,
#   resource_attributes={
#    'service.version': '3.1',
#    'deployment.environment': 'production',
#  })