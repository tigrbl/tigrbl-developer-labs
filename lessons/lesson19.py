from tigrbl_runtime.executors.kernel_executor import (
    resolve_phase_chains,
)
from task_app import Task
from labkit import run


async def exercise(p):
    chains = resolve_phase_chains(Task, "summary")
    inventory = {
        str(phase): [
            getattr(
                fn,
                "__tigrbl_label",
                getattr(fn, "__name__", str(fn)),
            )
            for fn in steps
        ]
        for phase, steps in chains.items()
        if steps
    }
    p.show("Compiled operation phase chains", inventory)
    p.check(
        any("HANDLER" in k for k in inventory),
        "plan contains handler-phase work",
    )
    await p.request(
        "POST", "/task/summary", {"title": "Trace the plan"}
    )
    p.show(
        "Interpretation",
        (
            "Plan labels describe possible work; the "
            "separate teaching trace records executed "
            "hooks and handler calls."
        ),
    )


if __name__ == "__main__":
    run(19, exercise)
