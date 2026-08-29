# firewall.py - Main Firewall Program

import sys
from packet_sniffer import packet_sniffer
from rule_engine import rule_engine
from logger import logger
from api import app

def print_banner():
    print("""
    ╔═══════════════════════════════════════╗
    ║     CyberOS Firewall Engine v1.0      ║
    ║     EduRankAI Cybersecurity Program   ║
    ╚═══════════════════════════════════════╝
    """)

def show_menu():
    print("\n[FIREWALL MENU]")
    print("1. Start packet sniffer")
    print("2. Start REST API server")
    print("3. View firewall rules")
    print("4. Add new rule")
    print("5. View statistics")
    print("6. View recent logs")
    print("7. Exit")
    return input("\nSelect option (1-7): ")

def main():
    print_banner()
    
    while True:
        choice = show_menu()
        
        if choice == "1":
            print("\n[*] Starting packet sniffer (Ctrl+C to stop)...")
            print("[*] Requires admin/root privileges")
            try:
                packet_sniffer.start_sniffing(packet_count=100)
                print(f"\n[*] Captured {packet_sniffer.packet_count} packets")
            except PermissionError:
                print("[!] Error: Need admin privileges. Run as administrator.")
            except KeyboardInterrupt:
                print("\n[*] Sniffer stopped")
        
        elif choice == "2":
            print("\n[*] Starting REST API on http://localhost:5000")
            print("[*] Press Ctrl+C to stop")
            try:
                app.run(debug=False, port=5000)
            except KeyboardInterrupt:
                print("\n[*] API stopped")
        
        elif choice == "3":
            print("\n[FIREWALL RULES]")
            rules = rule_engine.list_rules()
            for rule in rules:
                print(f"  Rule #{rule['id']}: {rule['action']} {rule['protocol']} "
                      f"port {rule['port']} ({rule['description']})")
        
        elif choice == "4":
            action = input("Action (ALLOW/DROP): ").upper()
            protocol = input("Protocol (TCP/UDP): ").upper()
            port = int(input("Port number: "))
            description = input("Description: ")
            rule_engine.add_rule(action, protocol, port, description)
            print("[+] Rule added successfully")
        
        elif choice == "5":
            stats = logger.get_stats()
            print("\n[TRAFFIC STATISTICS]")
            print(f"  Total packets: {stats['total_packets']}")
            print(f"  Allowed: {stats['allowed_packets']}")
            print(f"  Dropped: {stats['dropped_packets']}")
            print(f"  Bytes processed: {stats['bytes_processed']}")
        
        elif choice == "6":
            logs = logger.get_recent_logs(5)
            print("\n[RECENT LOGS]")
            for log in logs:
                print(f"  [{log['action']}] {log['source_ip']} → {log['dest_ip']} "
                      f"| {log['protocol']}:{log['dest_port']}")
        
        elif choice == "7":
            print("\n[*] Exiting firewall...")
            break
        
        else:
            print("[!] Invalid option")

if __name__ == "__main__":
    main()
