from tigrbl_core._spec import WsBindingSpec, JsonRpcFramingSpec
from tigrbl_atoms.atoms.framing.codec import (
    encode_frame,
    decode_frame,
)
from task_app import Task
from labkit import run


async def exercise(p):
    try:
        WsBindingSpec(
            proto="ws",
            path="/ws",
            framing=JsonRpcFramingSpec(),
            subprotocols=("wrong",),
        )
    except ValueError as error:
        p.show(
            "Actual conflicting-subprotocol rejection",
            str(error),
        )
        rejected = True
    else:
        rejected = False
    p.check(rejected, "conflicting subprotocol fails closed")
    results = []
    for framing in ("jsonrpc", "ndjson"):
        frame = {
            "jsonrpc": "2.0",
            "method": "Task.summary",
            "params": {"title": "Framed input"},
            "id": 42,
        }
        wire = encode_frame(
            framing, [frame] if framing == "ndjson" else frame
        )
        decoded = decode_frame(framing, wire)
        if framing == "ndjson":
            decoded = decoded[0]
        result = await Task.handlers.summary.core(
            {"payload": decoded["params"]}
        )
        results.append(result)
        p.show(
            f"{framing} codec boundary",
            {
                "encoded": wire.decode(),
                "decoded": decoded,
                "core_result": result,
            },
        )
    p.check(
        results[0] == results[1],
        "decoded parameters produce equivalent pure-core results",
    )
    p.show(
        "Scope",
        "This is a codec/core lab. Only lesson 17 claims an actual network WS JSON-RPC exchange; NDJSON is not presented as a second network demo.",
    )


if __name__ == "__main__":
    run(18, exercise)
