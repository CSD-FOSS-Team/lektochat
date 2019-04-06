# Client \<-\> Client

## Connection Establishment

1. Client A wants to connect to client B.
2. Client A checks and picks one of the supported connection methods of client B which it got from the server.
3. Client A starts a new connection to client B with the picked connection type.

### Handshake

Client A sends a [handshake packet](#handshake-packet) with its nickname.

#### Handshake packet

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
    <td style="text-align:center" colspan="4">NULL terminated string of nickname</td>
  </tr>
</table>

### Acknowledge

Client B now can either aknowledge or deny the request.

If it accepts the request, then it sends its nickname and also waits until client A also accepts or rejects the connection.

### Client B Accept Packet

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
  <tr>
    <td style="text-align:center" colspan="4">NULL terminated string of nickname</td>
  </tr>
</table>

### Client A Accept Packet

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

### Client Reject Packet

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
    <td style="text-align:center" colspan="4">NULL terminated string of rejection reason</td>
  </tr>
</table>

### Message Exchange

Finally the two clients go into connected state, where they can freely exchange data.
The data gets packeted and split, so that the message can be of arbitrary length.

<table>
  <tr>
    <th style="text-align:left">0</th>
    <th style="text-align:left">1</th>
    <th style="text-align:left">2</th>
    <th style="text-align:left">3</th>
  </tr>
  <tr>
    <td style="text-align:center" colspan="4">Message id</th>
  </tr>
  <tr>
    <td style="text-align:center" colspan="4">Message part</th>
  </tr>
  <tr>
    <td style="text-align:center" colspan="4">Message length in bytes</th>
  </tr>
  <tr>
    <td style="text-align:center" colspan="4">Message</th>
  </tr>
  <tr>
    <td style="text-align:center" colspan="4">...</th>
  </tr>
</table>