import time

class Metrics:
    def __init__(self):
        self.calls = 0
        self.failures = 0
        self.total_latency = 0

    def record(self, latency, success=True):
        self.calls += 1
        self.total_latency += latency
        if not success:
            self.failures += 1

    def snapshot(self):
        return {
            "calls": self.calls,
            "failures": self.failures,
            "avg_latency": self.total_latency / self.calls if self.calls else 0
        }


metrics = Metrics()