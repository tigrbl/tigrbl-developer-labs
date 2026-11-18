from tigrbl_kernel.lifecycle_matrix import (
    build_lifecycle_matrix,
)
from labkit import run


async def exercise(p):
    matrix = build_lifecycle_matrix()
    selected = matrix["cells"][
        ("socket", "message.received", "HANDLER")
    ]
    p.show("Actual phase columns", matrix["phases"])
    p.show("Actual event rows", matrix["rows"])
    p.show("socket / message.received / HANDLER", selected)
    p.check(
        selected["tx_unit"] == "message"
        and selected["loop_region"] == "socket.receive",
        (
            "selected cell identifies message "
            "transaction unit and receive loop"
        ),
    )
    p.check(
        len(matrix["cells"]) == 66,
        "snapshot has 6 phase columns and 11 event rows",
    )


if __name__ == "__main__":
    run(21, exercise)
