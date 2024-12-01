import psutil


class MetricsRepository:

    def get_system_metrics():
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

        return {
            "cpu_usage_percent": cpu,
            "memory_usage_percent": memory,
            "disk_usage_percent": disk,
            "network_sent_mbytes": network_sent,
            "network_received_mbytes": network_received,
        }
