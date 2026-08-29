# packet_sniffer.py - Packet Capture Engine

from scapy.all import sniff, IP, TCP, UDP
from rule_engine import rule_engine
from logger import logger
from connection_tracker import tracker
from alerts import alert_engine

class PacketSniffer:
    def __init__(self):
        self.packet_count = 0
        self.is_running = False
    
    def start_sniffing(self, interface=None, packet_count=0):
        print("[*] Starting packet sniffer...")
        self.is_running = True
        
        try:
            sniff(
                prn=self.packet_callback,
                iface=interface,
                store=False,
                count=packet_count
            )
        except Exception as e:
            print(f"[!] Error: {e}")
    
    def packet_callback(self, packet):
        self.packet_count += 1
        packet_info = self._extract_packet_info(packet)
        
        if packet_info:
            action, rule_id, description = rule_engine.evaluate_packet(packet_info)
            logger.log_packet(packet_info, action)
            self._print_packet_info(packet_info, action, rule_id, description)
            conn = tracker.track(packet_info)
            new_alerts = alert_engine.check(packet_info)
            for a in new_alerts:
                print(f"[ALERT] {a['message']}")
    
    def _extract_packet_info(self, packet):
        if IP not in packet:
            return None
        
        ip_layer = packet[IP]
        packet_info = {
            "source_ip": ip_layer.src,
            "dest_ip": ip_layer.dst,
            "protocol": self._get_protocol_name(ip_layer.proto),
            "packet_size": len(packet),
            "source_port": 0,
            "dest_port": 0
        }
        
        if TCP in packet:
            tcp_layer = packet[TCP]
            packet_info["source_port"] = tcp_layer.sport
            packet_info["dest_port"] = tcp_layer.dport
        elif UDP in packet:
            udp_layer = packet[UDP]
            packet_info["source_port"] = udp_layer.sport
            packet_info["dest_port"] = udp_layer.dport
        
        return packet_info
    
    def _get_protocol_name(self, protocol_number):
        protocols = {6: "TCP", 17: "UDP", 1: "ICMP"}
        return protocols.get(protocol_number, f"OTHER({protocol_number})")
    
    def _print_packet_info(self, packet_info, action, rule_id, description):
        print(f"[{action}] {packet_info['source_ip']}:{packet_info['source_port']} "
              f"→ {packet_info['dest_ip']}:{packet_info['dest_port']} "
              f"| Rule #{rule_id} ({description})")

packet_sniffer = PacketSniffer()
