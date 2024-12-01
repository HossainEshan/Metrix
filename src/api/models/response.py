from typing import Dict

from pydantic import BaseModel


class SystemMetrics(BaseModel):
    cpu_usage_percent: float
    memory_usage_percent: float
    disk_usage_percent: float
    swap_memory_usage_percent: float
    network_sent_mbytes: float
    network_received_mbytes: float
    system_uptime: str  # Uptime formatted as HH:MM:SS
    load_average: Dict[str, float]  # Dictionary for 1, 5, 15-minute averages
    running_processes: int
