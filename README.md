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
The client will connect to the OPC server using credentials. It reads nodes and tries to write to them. Note that it will show a write error — this is because the user does not have write permissions on the node.
Do not close this execution, as we will run the attacker script and observe the changes.

####
```bash
$ python attacker.py
```
The attacker script will write on the RogueTemp node. See Client script how RogueTemp has changed.



![OPC Execution](/img/opc_execution.png)
