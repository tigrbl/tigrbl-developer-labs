from labkit import run


async def exercise(p):
    _, methods = await p.request("GET", "/system/methodz")
    _, hooks = await p.request("GET", "/system/hookz")
    _, plan = await p.request("GET", "/system/kernelz")
    p.check(
        "Task" in str(methods), "method inventory includes Task"
    )
    p.check(
        "check_status" in str(hooks),
        "hook inventory exposes the bound rule",
    )
    p.show(
        "Interpretation",
        "Inventories and plans describe structure; a request trace proves execution.",
    )


if __name__ == "__main__":
    run(4, exercise)
