from labkit import run
from task_app import TRACE


async def exercise(p):
    task = await p.create("good")
    status, error = await p.request(
        "POST",
        "/task",
        {
            "id": task["id"] + "-bad",
            "title": "Rejected task",
            "status": "unknown",
        },
    )
    p.check(
        status >= 400,
        "pre-handler rule rejects an invalid status",
    )
    read_status, _ = await p.request(
        "GET", f"/task/{task['id']}-bad"
    )
    p.check(
        read_status == 404,
        "rejected create did not persist the row",
    )
    p.show("Observed hook events", await p.trace())


if __name__ == "__main__":
    run(15, exercise)
