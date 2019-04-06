# Lektochat network topology

A group of clients is defined by the server they connect to.

The server only tracks the connected clients and distributes that information to the rest of the clients.

Client to client communication happens exclusively with direct(p2p) connections.

That way the server is only required during client discovery. Client messages never traverse the server.

## Protocol

Version: 0.0.1

|   Constants   |  Value  |
|:-------------:|:-------:|
| VERSION_MAJOR |   0x0   |
| VERSION_MINOR |   0x0   |
| VERSION_EXTRA |   0x0   |

Big endian encoding and 4 byte alignment is used encoding data.

### Server \<-\> Client

Please refer to [server-client](server_client.md).

### Client \<-\> Client

Please refer to [client-client](client_client.md).
