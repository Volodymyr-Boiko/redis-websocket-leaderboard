#!/usr/bin/env python3

import asyncio
import json
import sys
import websockets


def main():
    host = "localhost"
    port = 8765

    if len(sys.argv) > 1:
        host, port = sys.argv[1].split(":")

    client = LeaderboardInteractiveClient(host, port)
    client.run()


class LeaderboardInteractiveClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_path = "ws://{host}:{port}".format(**locals())

    def run(self):
        asyncio.get_event_loop().run_until_complete(self.command_selector())

    @asyncio.coroutine
    def command_selector(self):
        while True:
            command = int(input("Enter command [1 - Add Score, 2 - Get Top Scores, 3 - Clear, 4 - Exit]: "))

            if command == 1:
                yield from self.handle_add_score_command()
            if command == 2:
                yield from self.handle_get_top_command()
            if command == 3:
                yield from self.handle_clear_command()
            if command == 4:
                break

    @asyncio.coroutine
    def handle_add_score_command(self):
        websocket = yield from websockets.connect(self.server_path + "/score/add")
        name = input("Name? ")
        score = int(input("Score? "))
        request = json.dumps({"name": name, "score": score})
        yield from self.send_request(websocket, request)

    @asyncio.coroutine
    def handle_get_top_command(self):
        websocket = yield from websockets.connect(self.server_path + "/top")
        count = int(input("Count? "))
        request = json.dumps({"count": count})
        yield from self.send_request(websocket, request)

    @asyncio.coroutine
    def handle_clear_command(self):
        websocket = yield from websockets.connect(self.server_path + "/clear")
        request = "{}"
        yield from self.send_request(websocket, request)

    @asyncio.coroutine
    def send_request(self, websocket, request):
        yield from websocket.send(request)
        print("> {}".format(request))

        response = yield from websocket.recv()
        print("< {}".format(response))
        print()


if __name__ == "__main__":
    main()
