from pydantic import BaseModel


class SystemMetrics(BaseModel):
    cpu_usage_percent: float
    memory_usage_percent: float
    disk_usage_percent: float
    network_sent_mbytes: float
    network_received_mbytes: float
