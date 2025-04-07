from opcua import Server, ua
import time
import random
import threading

# Create OPC UA Server
server = Server()
server.set_endpoint("opc.tcp://0.0.0.0:4840/freeopcua/server/")

# Security policy without encryption and with authentication
server.set_security_policy([ua.SecurityPolicyType.NoSecurity])


# User, pass
def user_auth(isession, username, password):
    return username == "admin" and password == "1234"

server.user_manager.set_user_manager(user_auth)

# Namespace
uri = "urn:demo:d00dz"
idx = server.register_namespace(uri)

# Devices
objects = server.get_objects_node()
device = objects.add_object(idx, "Device1")

# Nodes
temperature_node = device.add_variable(ua.NodeId("Device1.Temperature", idx), "Temperature", 22.5)
control_node = device.add_variable(ua.NodeId("Device1.Control", idx), "Control", False)
rogue_node = device.add_variable(ua.NodeId("Device1.RogueTemp", idx), "RogueTemp", 88.8)  # Nodo vulnerable

# Enable writing permissions
#control_node.set_writable()
rogue_node.set_writable()

# Change temperature procedure
def simulate_temperature():
    while True:
        temperature_node.set_value(22.0 + random.random() * 4.0)
        time.sleep(5)

threading.Thread(target=simulate_temperature, daemon=True).start()

# Launch server
server.start()
print("OPC UA Server launched... Listening on opc.tcp://0.0.0.0:4840")
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    server.stop()
