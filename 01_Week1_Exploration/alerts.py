import time
from collections import defaultdict, deque

class AlertEngine:
    def __init__(self, scan_window=10, scan_port_threshold=8,
                 burst_window=10, burst_packet_threshold=200):
        self.scan_window = scan_window
        self.scan_port_threshold = scan_port_threshold
        self.burst_window = burst_window
        self.burst_packet_threshold = burst_packet_threshold
        self._recent = defaultdict(deque)
        self.alerts = []

    def check(self, packet_info):
        src = packet_info.get("source_ip", "unknown")
        now = time.time()
        window = self._recent[src]
        window.append((now, packet_info.get("dest_port", 0)))

        cutoff = now - max(self.scan_window, self.burst_window)
        while window and window[0][0] < cutoff:
            window.popleft()

        new_alerts = []

        recent_scan = [p for t, p in window if t >= now - self.scan_window]
        distinct_ports = set(recent_scan)
        if len(distinct_ports) >= self.scan_port_threshold:
            alert = {
                "severity": "HIGH", "category": "port_scan",
                "source_ip": src, "timestamp": now,
                "message": f"Possible port scan from {src}: "
                           f"{len(distinct_ports)} ports in {self.scan_window}s"
            }
            new_alerts.append(alert)

        recent_burst = [t for t, p in window if t >= now - self.burst_window]
        if len(recent_burst) >= self.burst_packet_threshold:
            alert = {
                "severity": "MEDIUM", "category": "volumetric_burst",
                "source_ip": src, "timestamp": now,
                "message": f"Volumetric burst from {src}: "
                           f"{len(recent_burst)} packets in {self.burst_window}s"
            }
            new_alerts.append(alert)

        self.alerts.extend(new_alerts)
        return new_alerts

    def recent(self, count=20):
        return self.alerts[-count:]

    def all_alerts(self):
        return self.alerts

alert_engine = AlertEngine()