"""Explicit local HTTP + WebSocket serving configuration."""

from tigrcorn import run

if __name__ == "__main__":
    run(
        "lab_host:app",
        host="127.0.0.1",
        port=8782,
        websocket=True,
        lifespan="off",
    )
