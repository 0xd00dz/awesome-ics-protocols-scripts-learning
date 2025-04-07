from opcua import Client
from opcua.ua.uaerrors import UaStatusCodeError
import time

client = Client("opc.tcp://localhost:4840/freeopcua/server/")
client.set_user("admin")
client.set_password("1234")
client.connect()

try:
    print("Client authenticated")

    temp_node = client.get_node("ns=2;s=Device1.Temperature")
    control_node = client.get_node("ns=2;s=Device1.Control")
    rogue_node = client.get_node("ns=2;s=Device1.RogueTemp")

    while True:
        # Read values on server
        temp = temp_node.get_value()
        rogue = rogue_node.get_value()
        print(f"Real temp: {temp:.2f} °C | RogueTemp: {rogue:.2f} °C")

        try:
            if temp > 24.0:
                control_node.set_value(True)
                print("Control ON")
            else:
                control_node.set_value(False)
                print("Control OFF")
        except UaStatusCodeError as e:
            print(f"You don't have writing permissions on 'Control': {e}")
            
        time.sleep(5)

except KeyboardInterrupt:
    print("Client stopped.")
finally:
    client.disconnect()
