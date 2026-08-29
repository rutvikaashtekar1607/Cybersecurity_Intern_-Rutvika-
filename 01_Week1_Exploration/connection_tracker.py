# connection_tracker.py - Stateful Connection Tracking

import time

class ConnectionTracker:
    def __init__(self, idle_timeout=300):
        self.connections = {}
        self.idle_timeout = idle_timeout

    def _key(self, packet_info):
        a = (packet_info["source_ip"], packet_info.get("source_port", 0))
        b = (packet_info["dest_ip"], packet_info.get("dest_port", 0))
        endpoints = tuple(sorted([a, b]))
        return (endpoints[0], endpoints[1], packet_info.get("protocol", ""))

    def track(self, packet_info):
        key = self._key(packet_info)
        now = time.time()
        conn = self.connections.get(key)

        if conn is None:
            conn = {
                "state": "NEW",
                "first_seen": now,
                "last_seen": now,
                "packet_count": 0,
            }
            self.connections[key] = conn

        conn["last_seen"] = now
        conn["packet_count"] += 1
        if conn["packet_count"] > 1:
            conn["state"] = "ESTABLISHED"

        return conn

    def is_established(self, packet_info):
        conn = self.connections.get(self._key(packet_info))
        return conn is not None and conn["state"] == "ESTABLISHED"

    def sweep_expired(self):
        now = time.time()
        expired = [k for k, c in self.connections.items()
                   if now - c["last_seen"] > self.idle_timeout]
        for k in expired:
            del self.connections[k]
        return len(expired)

    def count(self):
        return len(self.connections)

tracker = ConnectionTracker()
