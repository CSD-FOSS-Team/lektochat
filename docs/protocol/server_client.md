# Server \<-\> Client

## Connection Establishment

The client must first establish a TCP connection with the server.

## Handshake

When the [connection](#connection-establishment) is created, the client **first** sends a [packet](#client-packet) with information about the supported and enabled protocols. The server can then [accept](#server-accept-packet) or [reject](#server-reject-packet) the handshake client.

### Client Packet

<table>
  <tr>
    <th style="text-align:left">0</th>
    <th style="text-align:left">1</th>
    <th style="text-align:left">2</th>
    <th style="text-align:left">3</th>
  </tr>
  <tr>
    <td style="text-align:center">'L'</td>
    <td style="text-align:center">'E'</td>
    <td style="text-align:center">'K'</td>
    <td style="text-align:center">'T'</td>
  </tr>
  <tr>
    <td style="text-align:center">'H'</td>
    <td style="text-align:center">VERSION_MAJOR</td>
    <td style="text-align:center">VERSION_MINOR</td>
    <td style="text-align:center">VERSION_EXTRA</td>
  </tr>
  <tr>
    <td style="text-align:center" colspan="4">Number of known connection methods(32bit unsigned integer)</td>
  </tr>
  <tr>
    <td style="text-align:center" colspan="4">Array of 32bit integers used as a bitfield of supported connection methods</td>
  </tr>
</table>

### Server Accept Packet

<table>
  <tr>
    <th style="text-align:left">0</th>
    <th style="text-align:left">1</th>
    <th style="text-align:left">2</th>
    <th style="text-align:left">3</th>
  </tr>
  <tr>
    <td style="text-align:center">'L'</td>
    <td style="text-align:center">'E'</td>
    <td style="text-align:center">'K'</td>
    <td style="text-align:center">'T'</td>
  </tr>
  <tr>
    <td style="text-align:center">'A'</td>
    <td style="text-align:center">VERSION_MAJOR</td>
    <td style="text-align:center">VERSION_MINOR</td>
    <td style="text-align:center">VERSION_EXTRA</td>
  </tr>
</table>

### Server Reject Packet

<table>
  <tr>
    <th style="text-align:left">0</th>
    <th style="text-align:left">1</th>
    <th style="text-align:left">2</th>
    <th style="text-align:left">3</th>
  </tr>
  <tr>
    <td style="text-align:center">'L'</td>
    <td style="text-align:center">'E'</td>
    <td style="text-align:center">'K'</td>
    <td style="text-align:center">'T'</td>
  </tr>
  <tr>
    <td style="text-align:center">'R'</td>
    <td style="text-align:center">VERSION_MAJOR</td>
    <td style="text-align:center">VERSION_MINOR</td>
    <td style="text-align:center">VERSION_EXTRA</td>
  </tr>
  <tr>
    <td style="text-align:center" colspan="4">Null terminated string containing rejection message.</td>
  </tr>
</table>

## Connection Setup

After the handshake is accepted, the server obtains extra connection information from the client.

1. First the server sends a request to the client for information on a specific connection method based on [request](#server-request-packet).
2. The client responds with the requested information according to [response](#client-response-packet).
3. When the server is ready to enter the [heartbeat](#heartbeat) phase, it sends another [request](#server-request-packet), but with a zero index.

### Server Request Packet

<table>
  <tr>
    <th style="text-align:left">0</th>
    <th style="text-align:left">1</th>
    <th style="text-align:left">2</th>
    <th style="text-align:left">3</th>
  </tr>
  <tr>
    <td style="text-align:center">'L'</td>
    <td style="text-align:center">'E'</td>
    <td style="text-align:center">'K'</td>
    <td style="text-align:center">'T'</td>
  </tr>
  <tr>
    <td style="text-align:center">'T'</td>
    <td style="text-align:center">VERSION_MAJOR</td>
    <td style="text-align:center">VERSION_MINOR</td>
    <td style="text-align:center">VERSION_EXTRA</td>
  </tr>
  <tr>
    <td style="text-align:center" colspan="4">Index of method (32bit unsigned integer)</td>
  </tr>
</table>

### Client Response Packet

<table>
  <tr>
    <th style="text-align:left">0</th>
    <th style="text-align:left">1</th>
    <th style="text-align:left">2</th>
    <th style="text-align:left">3</th>
  </tr>
  <tr>
    <td style="text-align:center">'L'</td>
    <td style="text-align:center">'E'</td>
    <td style="text-align:center">'K'</td>
    <td style="text-align:center">'T'</td>
  </tr>
  <tr>
    <td style="text-align:center">'T'</td>
    <td style="text-align:center">VERSION_MAJOR</td>
    <td style="text-align:center">VERSION_MINOR</td>
    <td style="text-align:center">VERSION_EXTRA</td>
  </tr>
  <tr>
    <td style="text-align:center" colspan="4">Index of method (32bit unsigned integer)</td>
  </tr>
  <tr>
    <td style="text-align:center" colspan="4">Information</td>
  </tr>
</table>

_Information_:

This field's length and meaning depends on the _index of method_. For more information refer to [the connection method list](connection_methods/list.md).

## Heartbeat

After [Connection Setup](#connection-setup) phase concludes, the client and server go into the [heartbeat](#heartbeat) phase.

In this state, the client sends [heartbeat request](#heartbeat-request-packet) and the server responds with a number of [update responses](#update-response-packet), which contain what changed from the last update.

### Heartbeat Request Packet

<table>
  <tr>
    <th style="text-align:left">0</th>
    <th style="text-align:left">1</th>
    <th style="text-align:left">2</th>
    <th style="text-align:left">3</th>
  </tr>
  <tr>
    <td style="text-align:center">'L'</td>
    <td style="text-align:center">'E'</td>
    <td style="text-align:center">'K'</td>
    <td style="text-align:center">'T'</td>
  </tr>
  <tr>
    <td style="text-align:center">'H'</td>
    <td style="text-align:center">VERSION_MAJOR</td>
    <td style="text-align:center">VERSION_MINOR</td>
    <td style="text-align:center">VERSION_EXTRA</td>
  </tr>
  <tr>
    <td style="text-align:center" colspan="4" rowspan="2">Unix time stamp (64bit signed integer)</td>
  </tr>
</table>

### Update Response Packet

#### Client got added

<table>
  <tr>
    <th style="text-align:left">0</th>
    <th style="text-align:left">1</th>
    <th style="text-align:left">2</th>
    <th style="text-align:left">3</th>
  </tr>
  <tr>
    <td style="text-align:center">'L'</td>
    <td style="text-align:center">'E'</td>
    <td style="text-align:center">'K'</td>
    <td style="text-align:center">'T'</td>
  </tr>
  <tr>
    <td style="text-align:center">'H'</td>
    <td style="text-align:center">VERSION_MAJOR</td>
    <td style="text-align:center">VERSION_MINOR</td>
    <td style="text-align:center">VERSION_EXTRA</td>
  </tr>
  <tr>
    <td style="text-align:center" colspan="4" rowspan="2">Unix time stamp (64bit signed integer)</td>
  </tr>
  <tr>
  </tr>
  <tr>
    <td style="text-align:center">'A'</td>
    <td style="text-align:center" colspan="3">How many clients this packet contains</td>
  </tr>
  <tr>
    <td style="text-align:center" colspan="4">Size of client object in bytes</td>
  </tr>
  <tr>
    <td style="text-align:center" colspan="4">IP of the client</td>
  </tr>
  <tr>
    <td style="text-align:center" colspan="4">Index of supported connection method</td>
  </tr>
  <tr>
    <td style="text-align:center" colspan="4">Connection method extra data</td>
  </tr>
  <tr>
    <td style="text-align:center" colspan="4"><i>More connection methods...</i></td>
  </tr>
  <tr>
    <td style="text-align:center" colspan="4">More clients...</td>
  </tr>
</table>

#### Client got removed

<table>
  <tr>
    <th style="text-align:left">0</th>
    <th style="text-align:left">1</th>
    <th style="text-align:left">2</th>
    <th style="text-align:left">3</th>
  </tr>
  <tr>
    <td style="text-align:center">'L'</td>
    <td style="text-align:center">'E'</td>
    <td style="text-align:center">'K'</td>
    <td style="text-align:center">'T'</td>
  </tr>
  <tr>
    <td style="text-align:center">'H'</td>
    <td style="text-align:center">VERSION_MAJOR</td>
    <td style="text-align:center">VERSION_MINOR</td>
    <td style="text-align:center">VERSION_EXTRA</td>
  </tr>
  <tr>
    <td style="text-align:center" colspan="4" rowspan="2">Unix time stamp (64bit signed integer)</td>
  </tr>
  <tr>
  </tr>
  <tr>
    <td style="text-align:center">'R'</td>
    <td style="text-align:center" colspan="3">How many clients this packet contains.</td>
  </tr>
  <tr>
    <td style="text-align:center" colspan="4" rowspan="1">List of IPs of clients which got removed.</td>
  </tr>
  <tr>
    <td style="text-align:center" colspan="4" rowspan="1">...</td>
  </tr>
</table>
