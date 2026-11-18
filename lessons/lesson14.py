from tigrbl import TableBase, op_ctx, hook_ctx, build_handlers
from tigrbl_core._spec.op_spec import resolve
from labkit import run


async def exercise(p):
    events = []

    class ProbeTask(TableBase):
        @op_ctx(alias="ping", target="custom", persist="skip")
        def ping(cls, ctx):
            events.append("core")
            return {"ok": True}

        @hook_ctx(ops="ping", phase="PRE_TX_BEGIN")
        def before(cls, ctx):
            events.append("PRE_TX_BEGIN")

        @hook_ctx(ops="ping", phase="POST_COMMIT")
        def after_commit(cls, ctx):
            events.append("POST_COMMIT")

        @hook_ctx(ops="ping", phase="POST_RESPONSE")
        def after_response(cls, ctx):
            events.append("POST_RESPONSE")

    build_handlers(ProbeTask, resolve(ProbeTask))
    for entry in ("core", "dispatch", "invoke"):
        events.clear()
        result = await getattr(ProbeTask.handlers.ping, entry)(
            {"payload": {}}
        )
        p.show(
            entry, {"result": result, "events": list(events)}
        )
        if entry == "core":
            p.check(
                events == ["core"],
                "core executes only the core",
            )
        if entry == "dispatch":
            p.check(
                events == ["PRE_TX_BEGIN", "core"],
                "dispatch runs its selected lifecycle subset",
            )
        if entry == "invoke":
            p.check(
                events
                == [
                    "PRE_TX_BEGIN",
                    "core",
                    "POST_COMMIT",
                    "POST_RESPONSE",
                ],
                "invoke runs the complete fixture lifecycle",
            )


if __name__ == "__main__":
    run(14, exercise)
