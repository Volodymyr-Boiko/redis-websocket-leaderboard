# redis-websocket-leaderboard
A WebSocket-based leaderboard client and server that uses Redis behind the scenes (demo for my talk @ Lviv SQL User Group).

## How To Run

### Install Prerequisites

The project uses Python 3 and a few 3rd party packages, so make sure to install all of these first:

    $ sudo apt-get install python3 python3-pip
    $ sudo pip3 install asyncio websockets redis

### Run Server (localhost)

    $ python3 server.py

### Run Client (localhost)

There are three clients available:

1. Interactive client: allows you to run each command manually.

    `$ python3 interactive_client.py`

2. Load generator client: continuously hits the server with random requests for adding scores.

    `$ python3 load_generator_client.py`
    
3. Web UI (currently tested in Chrome and Firefox): navigate to `top.html` in your Web browser.

### Running in a Distributed Environment

If you want to run the server and the clients on different machines, make sure to override the host/port using an optional command line parameter:

    $ python3 server.py <WebSocketHost>:<WebSocketPort> <RedisHost>:<RedisPort>
    $ python3 interactive_client.py <WebSocketHost>:<WebSocketPort>

Example:

    $ python3 server.py 0.0.0.0:8765 192.168.10.205:6379
    $ python3 interactive_client.py 192.168.9.175:8765

_Note_: To connect to a remote server from the `top.html` Web UI, please edit `top.html` manually, specifying the proper hostname and port for the websocket.
