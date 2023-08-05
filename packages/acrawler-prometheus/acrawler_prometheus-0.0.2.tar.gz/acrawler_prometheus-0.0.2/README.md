# acrawler-prometheus

The handler working with [aCrawler](https://github.com/wooddance/aCrawler) and [Prometheus](http://prometheus.io/).

Export statistics for:

- Concurrent requests
- Task (Requests, Items) counts
- Queue status

## Installation

```bash
$ pip install acrawler_prometheus
```

## Usage

Add Handler:

```python
class MyCrawler(Crawler):
    middleware_config = {
        "acrawler_prometheus.PromExporter": 100,
    }

    config = {
        PROMETHEUS_INTERVAL = 5
    }
```

Avaliable Config:

```python
PROMETHEUS_ADDR = "localhost"
PROMETHEUS_PORT = 8000
PROMETHEUS_INTERVAL = 1  # exporting interval, in second
```
