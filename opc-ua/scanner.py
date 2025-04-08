import socket
from opcua import Client
from opcua.ua.uaerrors import UaStatusCodeError
from opcua.ua import NodeClass
import json
import csv
import time

# Global list to store extracted node data
extracted_nodes = []

# ---------------------------------------------------------------------
# Simple network scan to find OPC UA servers
def discover_opc_ua_servers(base_ip="192.168.0.", ports=[4840], ip_range=25):
    print(f"🔍 Scanning for real OPC UA servers...\n")
    found = []

    for i in range(1, ip_range + 1):
        ip = f"{base_ip}{i}"
        for port in ports:
            endpoint = f"opc.tcp://{ip}:{port}/"
            try:
                print(f"Trying: {endpoint}")
                client = Client(endpoint)
                endpoints = client.connect_and_get_server_endpoints()
                print(f"✅ Valid OPC UA server: {endpoint}")
                found.append(endpoint)
            except UaStatusCodeError as e:
                print(f"⚠️  {endpoint} responded, but not a valid OPC UA server: {e}")
            except socket.timeout:
                pass
            except Exception:
                pass
            finally:
                try:
                    client.disconnect()
                except:
                    pass
    if not found:
        print("❌ No valid OPC UA servers found.")
    return found

# ---------------------------------------------------------------------
# Enhanced recursive node browsing with values, data types and export support
def enhanced_browse(node, level=0, only_with_values=False):
    children = node.get_children()
    for child in children:
        try:
            browse_name = child.get_browse_name()
            node_class = child.get_node_class()

            if node_class == NodeClass.Variable:
                try:
                    value = child.get_value()
                    if only_with_values and (value is None or value == "" or value == 0):
                        continue  # skip uninteresting values when filtering
                    data_type = child.get_data_type_as_variant_type().name
                    print("  " * level + f"- {browse_name} | {node_class.name} | {value} ({data_type})")
                    extracted_nodes.append({
                        "browse_name": str(browse_name),
                        "node_class": node_class.name,
                        "value": str(value),
                        "data_type": data_type
                    })
                except:
                    if not only_with_values:
                        print("  " * level + f"- {browse_name} | {node_class.name} | [UNREADABLE]")
            else:
                if not only_with_values:
                    print("  " * level + f"- {browse_name} | {node_class.name}")
        except Exception as e:
            print("  " * level + f"- [ERROR] {e}")

        try:
            enhanced_browse(child, level + 1, only_with_values)
        except:
            continue

# ---------------------------------------------------------------------
# Export node data to JSON

def export_to_json(filename="opc_nodes.json"):
    with open(filename, "w") as f:
        json.dump(extracted_nodes, f, indent=2)
    print(f"\n📦 Nodes exported to {filename}")

# ---------------------------------------------------------------------
# Export node data to CSV

def export_to_csv(filename="opc_nodes.csv"):
    if not extracted_nodes:
        return
    keys = extracted_nodes[0].keys()
    with open(filename, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(extracted_nodes)
    print(f"\n📦 Nodes exported to {filename}")

# ---------------------------------------------------------------------
# Connect to an OPC UA server and scan its nodes
def scan_opc_server(endpoint="opc.tcp://localhost:4840/freeopcua/server/", only_values=True):
    global extracted_nodes
    extracted_nodes = []  # Clear previous results

    client = Client(endpoint)
    client.set_user("admin")
    client.set_password("1234")

    try:
        client.connect()
        print(f"\n🔗 Connected to {endpoint}")
        print("🔍 Browsing OPC UA node tree...\n")
        root = client.get_root_node()
        enhanced_browse(root, only_with_values=only_values)
    except Exception as e:
        print("❌ Error during scan:", e)
    finally:
        client.disconnect()
        print("🔌 Disconnected")

    export_to_json()
    export_to_csv()

# ---------------------------------------------------------------------
# Main menu
def main():
    while True:
        print("\n====== ICS TOOLKIT: OPC UA ======")
        print("1. Search for OPC UA servers on the network")
        print("2. Connect to a server and scan/export nodes with values")
        print("0. Exit")
        choice = input("Select an option: ")

        if choice == "1":
            base_ip = input("Base IP (e.g., 192.168.0.): ") or "192.168.0."
            ip_range = input("IP range to scan (e.g., 25): ") or "25"
            port_range = input("Port range (e.g., 4840-4845): ") or "4840"

            if "-" in port_range:
                start_port, end_port = map(int, port_range.split("-"))
                ports = list(range(start_port, end_port + 1))
            else:
                ports = [int(port_range)]

            discover_opc_ua_servers(base_ip, ports, int(ip_range))

        elif choice == "2":
            endpoint = input("Enter OPC UA endpoint (e.g., opc.tcp://192.168.0.10:4840/): ")
            filter_values = input("Only show variables with real values? (y/n): ").lower() == "y"
            scan_opc_server(endpoint, only_values=filter_values)

        elif choice == "0":
            break
        else:
            print("❌ Invalid option")

if __name__ == "__main__":
    main()
