import asyncio, json, websockets
from labkit import run


async def exercise(p):
    exchanges = []
    async with websockets.connect(
        "ws://127.0.0.1:8782/ws/lessons",
        subprotocols=["jsonrpc"],
    ) as ws:
        for ident, title in (
            (41, "First message"),
            (42, "Second message"),
        ):
            sent = {
                "jsonrpc": "2.0",
                "method": "SocketTask.summary",
                "params": {"title": title},
                "id": ident,
            }
            await ws.send(json.dumps(sent))
            received = json.loads(
                await asyncio.wait_for(ws.recv(), 5)
            )
            exchanges.append(
                {"request": sent, "response": received}
            )
            p.check(
                received["id"] == ident,
                (
                    f"message {ident} receives its own "
                    "correlated response"
                ),
            )
    p.show(
        "Two real exchanges on one socket",
        exchanges,
        "websocket",
    )
    p.show("Connection after context exit", str(ws.state))
    p.check(
        int(ws.state) == 3,
        "socket is closed after the context exits",
    )


if __name__ == "__main__":
    run(20, exercise)
