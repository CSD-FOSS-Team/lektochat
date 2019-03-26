# Intro

First the client establishes a TCP connection with the server.

## Handshake

When the connection is created, the client first sends a packet with information about the supported protocols and any extra required information. The server can then accept or reject the handshake.

## Test Connect

After the handshake is accepted, the server proceeds to test each of the supported protocols the client advertised.

## Heartbeat/Update

After test connect finishes, the client and server go into heartbeat state. In this state, the client sends heartbeat request and the server responds with a number of update packets, which contain differential information about all the connected clients.
