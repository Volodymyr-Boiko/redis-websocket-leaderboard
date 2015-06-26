#!/usr/bin/env python3

import asyncio
import json
import random
import sys
import websockets


def main():
    host = "localhost"
    port = 8765

    if len(sys.argv) > 1:
        host, port = sys.argv[1].split(":")

    client = LeaderboardLoadGeneratorClient(host, port)
    client.run()


class LeaderboardLoadGeneratorClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_path = "ws://{host}:{port}".format(**locals())
        self.names = []

    def run(self):
        self.names = self.read_names_from_file("names.txt")
        asyncio.get_event_loop().run_until_complete(self.main_loop())

    def read_names_from_file(self, filename):
        with open(filename, "r") as names_file:
            return [name.strip() for name in names_file.readlines()]

    @asyncio.coroutine
    def main_loop(self):
        while True:
            yield from self.submit_random_score()

    @asyncio.coroutine
    def submit_random_score(self):
        websocket = yield from websockets.connect(self.server_path + "/score/add")

        # Choosing a random name using Gaussian distribution where the mean value is the middle of the list.
        choice_index = int(random.gauss(len(self.names) / 2, len(self.names) / 4))

        # Making sure that the choice does not exceed the 0..N-1 bounds.
        choice_index = max(0, choice_index)
        choice_index = min(len(self.names) - 1, choice_index)

        name = self.names[choice_index]
        score = random.randint(0, 100)
        request = json.dumps({"name": name, "score": score})
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
