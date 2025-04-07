## Awesome Scripts for learning OT/ICS protocols
This is a personal project I worked on to get a deeper understanding of how OT protocols work. As a cybersecurity analyst, I'm interested in knowing how they operate in order to detect threats and configure detection rules. If you're in the same situation, I hope this project helps you as much as it helped me. In this repository, I present the scripts and how to use them, along with a brief explanation.

### Protocols Supported
- OPC UA

### How to use it
#### Dependencies
```bash
$ pip install opcua
```
#### Server
```bash
$ python server.py
```

#### Client
```bash
$ python client.py
```
The client will connect to the OPC server using credentials. It reads nodes and tries to write to them. Note that it will show a write error — this is because the user does not have write permissions on the node. This is intentional, to show that you can harden your nodes by removing write permissions (if necessary).
Do not close this execution, as we will run the attacker script and observe the changes.


####
```bash
$ python attacker.py
```
The attacker script will write to the RogueTemp node. Check the client script to see how RogueTemp has changed.



![OPC Execution](/img/opc_execution.png)

### Blue Team
You can observe a bunch of interesting traffic you can monitor as an analyst:

![OPC Wireshark](/img/opc_wireshark.png)

#### Hello message
Use this traffic to detect possible OPC Scanners

#### Acknowledge message
You could use it if you want to monitor if there is a response by the server. Maybe useful if you correlate Hello messages with Acknowledge messages.

#### WriteRequest
You want to know if there are uncontrolled and malicious devices on your OT network. Create alerts if you see writerequests from those uncontrolled devices on the net.
![OPC Write Attacker](/img/opc_write_attacker.png)

### Harden Nodes
Do you want to prevent the attacker from writing to the RogueTemp node? I challenge you to try it! Edit server.py and look for the line of code you need to modify.

