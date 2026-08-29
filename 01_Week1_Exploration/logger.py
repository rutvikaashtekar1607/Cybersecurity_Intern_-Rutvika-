# logger.py - Firewall Logging

import json
import hashlib
from datetime import datetime
from config import LOG_FILE

class FirewallLogger:
    def __init__(self):
        self.log_file = LOG_FILE
        self.traffic_stats = {
            "total_packets": 0,
            "allowed_packets": 0,
            "dropped_packets": 0,
            "bytes_processed": 0
        }
    
    def log_packet(self, packet_info, action):
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "source_ip": packet_info.get("source_ip", "N/A"),
            "dest_ip": packet_info.get("dest_ip", "N/A"),
            "protocol": packet_info.get("protocol", "N/A"),
            "source_port": packet_info.get("source_port", "N/A"),
            "dest_port": packet_info.get("dest_port", "N/A"),
            "packet_size": packet_info.get("packet_size", 0)
        }
        
        log_json = json.dumps(log_entry, sort_keys=True)
        log_entry["hash"] = hashlib.sha256(log_json.encode()).hexdigest()
        
        with open(self.log_file, 'a') as f:
            f.write(json.dumps(log_entry) + "\n")
        
        self._update_stats(action, packet_info)
    
    def _update_stats(self, action, packet_info):
        self.traffic_stats["total_packets"] += 1
        if action == "ALLOW":
            self.traffic_stats["allowed_packets"] += 1
        else:
            self.traffic_stats["dropped_packets"] += 1
        self.traffic_stats["bytes_processed"] += packet_info.get("packet_size", 0)
    
    def get_stats(self):
        return self.traffic_stats
    
    def get_recent_logs(self, count=10):
        try:
            with open(self.log_file, 'r') as f:
                lines = f.readlines()
            recent = []
            for line in lines[-count:]:
                recent.append(json.loads(line))
            return recent
        except FileNotFoundError:
            return []
    
    def export_logs(self, output_file):
        try:
            with open(self.log_file, 'r') as f:
                logs = [json.loads(line) for line in f.readlines()]
            with open(output_file, 'w') as f:
                json.dump(logs, f, indent=2)
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False

logger = FirewallLogger()
