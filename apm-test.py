#from splunk_otel.tracing import start_tracing
import os
token = 'XnI5SWNNVv_uoCURsap5TA'
#ENV VARS
os.environ["OTEL_EXPORTER_JAEGER_ENDPOINT"] = "https://ingest.{REALM}.signalfx.com/v2/trace".format(REALM=REALM)
os.environ["OTEL_RESOURCE_ATTRIBUTES"] = "nike-farshore-testing"
os.environ["SPLUNK_ACCESS_TOKEN"] = token


import uwsgidecorators
from splunk_otel.tracing import start_tracing
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from flask import Flask

app = Flask(__name__)

@uwsgidecorators.postfork
def setup_tracing():
    start_tracing()
    FlaskInstrumentor().instrument_app(app)

@app.route('/hello/')
def hello_world():
    return 'Hello, World!'



