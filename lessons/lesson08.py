from task_app import Task
from labkit import run
from tigrbl.schema import _build_schema
from pydantic import ValidationError


async def exercise(p):
    schema = _build_schema(Task, verb="create")
    bad = {
        "id": "validation-1",
        "title": "x" * 81,
        "status": "open",
    }
    try:
        schema.model_validate(bad)
    except ValidationError as error:
        p.show("Actual input-model rejection", error.errors())
        rejected = True
    else:
        rejected = False
    p.check(
        rejected,
        (
            "81-character title is rejected by the "
            "generated input model"
        ),
    )
    good = {**bad, "title": "Ship a lesson"}
    p.show(
        "Corrected input",
        schema.model_validate(good).model_dump(),
    )
    await p.create("valid")


if __name__ == "__main__":
    run(8, exercise)
