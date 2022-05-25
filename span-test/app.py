from splunk_otel.tracing import start_tracing
#from opentelemetry import trace
import requests
from waitress import serve
import os
token = 'XnI5SWNNVv_uoCURsap5TA'
REALM = "us1"

os.environ["OTEL_EXPORTER_JAEGER_ENDPOINT"] = "https://ingest.{REALM}.signalfx.com/v2/trace".format(REALM=REALM)
#os.environ["OTEL_RESOURCE_ATTRIBUTES"] = "deployment.environment: production"
os.environ["SPLUNK_ACCESS_TOKEN"] = token


start_tracing(service_name='digitaldrivethru')




def hello_world():
    tracer = trace.get_tracer(__name__)
    with tracer.start_as_current_span("Get Reccomedations"):
        r = requests.get("http://www.splunk.com")
        with tracer.start_as_current_span("digital-drive-thru-flask"):
                    print("deepbrew")


    return r.url



hello_world()