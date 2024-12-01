import time

import psutil
from fastapi import Depends


class MetricsService:

    def get_system_metrics(self):
        # CPU usage
        cpu = psutil.cpu_percent(interval=1)
        # Memory usage
        memory = psutil.virtual_memory().percent
        # Disk usage
        disk = psutil.disk_usage("/").percent
        # Network activity
        net = psutil.net_io_counters()
        network_sent = round(net.bytes_sent / 1024 / 1024, 2)  # Convert to MB
        network_received = round(net.bytes_recv / 1024 / 1024, 2)  # Convert to MB

        # System uptime
        boot_time = psutil.boot_time()  # Boot time as a timestamp
        current_time = time.time()  # Current time as a timestamp
        uptime_seconds = int(current_time - boot_time)
        uptime_formatted = time.strftime(
            "%H:%M:%S", time.gmtime(uptime_seconds)
        )  # Format as HH:MM:SS

        # Load average (Linux/Unix only)
        load_avg = psutil.getloadavg() if hasattr(psutil, "getloadavg") else (0, 0, 0)

        # Number of running processes
        running_processes = len(psutil.pids())

        # Swap memory usage
        swap = psutil.swap_memory().percent

        return {
            "cpu_usage_percent": cpu,
            "memory_usage_percent": memory,
            "disk_usage_percent": disk,
            "swap_memory_usage_percent": swap,
            "network_sent_mbytes": network_sent,
            "network_received_mbytes": network_received,
            "system_uptime": uptime_formatted,
            "load_average": {
                "1_min": load_avg[0],
                "5_min": load_avg[1],
                "15_min": load_avg[2],
            },
            "running_processes": running_processes,
        }


def get_metrics_service():
    return MetricsService()


metrics_service_dependency = Depends(get_metrics_service)
