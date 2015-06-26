#!/usr/bin/env python3

import asyncio
import json
import redis
import websockets


def main():
    server = LeaderboardServer(socket_host="localhost", socket_port=8765, redis_host="localhost", redis_port=6379)
    server.start()


class LeaderboardServer:
    def __init__(self, socket_host, socket_port, redis_host, redis_port):
        self.socket_host = socket_host
        self.socket_port = socket_port
        self.redis_host = redis_host
        self.redis_port = redis_port
        self.redis_client = None
        self.socket_server = None

    def start(self):
        self.redis_client = redis.StrictRedis(host=self.redis_host, port=self.redis_port, db=0)
        self.socket_server = websockets.serve(self.main_handler, host=self.socket_host, port=self.socket_port)
        asyncio.get_event_loop().run_until_complete(self.socket_server)
        asyncio.get_event_loop().run_forever()

    @asyncio.coroutine
    def main_handler(self, websocket, path):
        if path == "/score/add":
            yield from self.add_score_handler(websocket)
        if path == "/top":
            yield from self.top_n_handler(websocket)
        if path == "/clear":
            yield from self.clear_handler(websocket)

    @asyncio.coroutine
    def add_score_handler(self, websocket):
        # Parse request
        request = yield from websocket.recv()
        print("< [Add Score]   {}".format(request))
        request_params = json.loads(request)
        name = request_params["name"]
        score = request_params["score"]

        # Execute Redis command
        redis_result = self.redis_client.zincrby(name="leaderboard", value=name, amount=score)
        new_score = int(redis_result)

        # Return response
        response = json.dumps({"new_score": new_score})
        print("> {}".format(response))
        yield from websocket.send(response)

    @asyncio.coroutine
    def top_n_handler(self, websocket):
        # Parse request
        request = yield from websocket.recv()
        print("< [Get Top N]   {}".format(request))
        request_params = json.loads(request)
        count = request_params["count"]

        # Execute Redis command
        redis_result = self.redis_client.zrevrange(name="leaderboard", start=0, end=count - 1, withscores=True)
        normalized_result = [(name.decode("utf-8"), int(score)) for name, score in redis_result]

        # Return response
        response = json.dumps(normalized_result)
        print("> {}".format(response))
        yield from websocket.send(response)

    @asyncio.coroutine
    def clear_handler(self, websocket):
        # Parse request
        request = yield from websocket.recv()
        print("< [Clear]   {}".format(request))

        # Execute Redis command
        self.redis_client.delete("leaderboard")

        # Return response
        response = json.dumps({"cleared": True})
        print("> {}".format(response))
        yield from websocket.send(response)


if __name__ == "__main__":
    main()
