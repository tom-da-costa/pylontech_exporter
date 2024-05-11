from prometheus_client import start_http_server, Gauge, Summary, Info, Counter, Enum
import time
import serial
import json

# Create a metric to track time spent and requests made.
REQUEST_TIME = Summary('metrics_retrieving_seconds', 'Time spent retrieving metrics')
g = Gauge('perso_test',"Metrics peronnel de test")
c = Counter('my_requests_total', 'HTTP Failures', ['method', 'endpoint'], 'test', 'toto', 'seconds')
c.labels('get', '/').inc(exemplar={'trace_id': 'abc123'})
c.labels('post', '/submit').inc(1.0, {'trace_id': 'def456'})
e = Enum('my_task_state', 'Description of enum',
        states=['starting', 'running', 'stopped'])
e.state('running')

# Decorate function with metric.
@REQUEST_TIME.time()
def update_metrics():
  time.sleep(2)

if __name__ == '__main__':
  # Start up the server to expose the metrics.
  start_http_server(8000)
  # Generate some requests.
  while True:
    update_metrics()
    time.sleep(5)