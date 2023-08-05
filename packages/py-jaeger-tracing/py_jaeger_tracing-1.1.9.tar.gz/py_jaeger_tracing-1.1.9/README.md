# PyJaegerTracing

PyJaegerTracing: Ultimate tool for distribution tracing in Python


## Installation

```bash
pip install py-jaeger-tracing
```


## Features

* Multiprocessing support
* Context / Decorator based tracing
* Injecting / Extracting tracer span
* Logger integration
* Requests integration using patching
* Boto3 integration using patching
* Tornado integration


# All in One

```
docker run -d --name jaeger \
  -e COLLECTOR_ZIPKIN_HTTP_PORT=9411 \
  -p 5775:5775/udp \
  -p 6831:6831/udp \
  -p 6832:6832/udp \
  -p 5778:5778 \
  -p 16686:16686 \
  -p 14268:14268 \
  -p 9411:9411 \
  jaegertracing/all-in-one:1.13
```