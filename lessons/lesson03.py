from tigrbl import TigrblApp, TableBase
from labkit import run


async def exercise(p):
    from task_app import Task

    empty = TigrblApp(mount_system=False)
    before = [getattr(r, "path", "") for r in empty.routes]
    empty.include_table(Task)
    after = [getattr(r, "path", "") for r in empty.routes]
    p.show("Before include_table", before)
    p.show("After include_table", after)
    p.check(
        "/task" not in before and "/task" in after,
        "registration adds the collection route",
    )


if __name__ == "__main__":
    run(3, exercise)
