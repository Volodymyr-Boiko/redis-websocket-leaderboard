# redis-websocket-leaderboard
A WebSocket-based leaderboard client and server that uses Redis behind the scenes (demo for my talk @ Lviv SQL User Group).

## How To Run

### Install Prerequisites

The project uses Python 3 and a few 3rd party packages, so make sure to install all of these first:

    $ sudo apt-get install python3 python3-pip
    $ sudo pip3 install asyncio websockets redis

### Run Server

    $ python3 server.py

### Run Client

There are three clients available:

1. Interactive client: allows you to run each command manually.

    `$ python3 interactive_client.py`

2. Load generator client: continuously hits the server with random requests for adding scores.

    `$ python3 load_generator_client.py`
    
3. Web UI (currently tested in Chrome and Firefox): navigate to `top.html` in your Web browser.
