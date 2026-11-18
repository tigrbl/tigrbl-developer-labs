from task_app import Task, TRACE
from labkit import run


async def exercise(p):
    TRACE.clear()
    result = await Task.handlers.summary.core(
        {"payload": {"title": "Core handler"}}
    )
    p.show("Direct core result", result)
    p.show("Direct core trace", list(TRACE))
    p.check(
        result["words"] == 2,
        "custom core executes the authored function",
    )
    p.check(
        not any(e.get("hook") for e in TRACE),
        "core does not execute lifecycle hooks",
    )
    await p.create("canonical")
    p.show(
        "Interpretation",
        (
            "Canonical create performs persistence. "
            "The custom summary core computes a "
            "result."
        ),
    )


if __name__ == "__main__":
    run(12, exercise)
