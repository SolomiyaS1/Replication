# Replication

The project consists of three nodes -- one master and two secondaries. 
Currently the amount of secondaries, ports, etc are hardcoded. In future it will be moved to configs.

The project is written on python.
There's an HTTP server setup with Flask on every node.  Master also has jsonrpcclient, secondaries -- jsonrpcserver. 

A client (e. g. Postman) sends a message via POST request to the master node. Master sends the message and the name of the remote procedure ('method': 'save_message'), via jsonrpcclient.http_client. On secondaries jsonrpcserver handles the request, calling save_message procedure, passed in the request.

Every node is wrapped in docker
