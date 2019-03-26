# Intro

The client which wants to connect starts a new connection of one of the supported connection types of the other client.

## Handshake

First the client which started the connection sends a handshake packet with its nickname.

## Acknowledge

Then the other client can either aknowledge or deny the request. If it accepts the request, then it sends its nickname and also waits until the client which started the connection accepts or rejects the connection.

## Communication

Then the two clients go into connected state, where they can freely exchange data. The data is only packeted, so that the exchanged data can be of arbitrary length.
