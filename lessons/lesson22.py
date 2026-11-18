from tigrbl_core._spec.hook_spec import (
    HookSpec,
    validate_hook_legality,
)
from labkit import run


async def exercise(p):
    rejected = False
    try:
        validate_hook_legality(
            HookSpec(phase="POST_EMIT", fn=lambda ctx: None)
        )
    except ValueError as error:
        p.show("Actual legality rejection", str(error))
        rejected = True
    p.check(
        rejected, "POST_EMIT is rejected as a user-hook phase"
    )
    validate_hook_legality(
        HookSpec(phase="PRE_HANDLER", fn=lambda ctx: None)
    )
    p.show(
        "Public phase validation",
        {"phase": "PRE_HANDLER", "accepted": True},
    )
    p.check(
        True, "PRE_HANDLER passes the public hook validator"
    )


if __name__ == "__main__":
    run(22, exercise)
