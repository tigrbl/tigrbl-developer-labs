from tigrbl_core._spec.hook_spec import (
    HookSpec,
    matches_hook_selector,
)
from labkit import run


async def exercise(p):
    hook = HookSpec(
        phase="PRE_HANDLER",
        fn=lambda ctx: None,
        ops="summary",
        family=("message",),
        framing=("jsonrpc",),
        subevents=("message.received",),
    )
    matched = {
        "op": "summary",
        "family": "message",
        "subevent": "message.received",
        "framing": "jsonrpc",
    }
    excluded = {**matched, "framing": "ndjson"}
    a = matches_hook_selector(hook, matched)
    b = matches_hook_selector(hook, excluded)
    p.show(
        "Matching metadata",
        {"metadata": matched, "selected": a},
    )
    p.show(
        "Excluded metadata",
        {"metadata": excluded, "selected": b},
    )
    p.check(
        a and not b,
        "the selector matcher distinguishes framing",
    )
    p.show(
        "Scope",
        "Matcher proof is not universal mounted-path enforcement. Owner-level binding filters differ; validate the selected transport path separately.",
    )


if __name__ == "__main__":
    run(23, exercise)
