# Lektochat network topology.

For each 'net' there is a central server which clients connect to. The server stores only information which helps clients discover and connect to other clients, not identify them. Most of the communications happen with p2p connections between clients.

All of the protocol documentation assumes big endian encoding, unless otherwise specified.

## Server \<-\> Client protocol.

Please refer to [server-client](server_client.md).

## Client \<-\> Client protocol.

Please refer to [client-client](client_client.md).
