from labkit import run


async def exercise(p):
    _, schema = await p.request("GET", "/openapi.json")
    paths = schema["paths"]
    p.show(
        "Custom operation paths",
        [x for x in paths if "summary" in x or "preview" in x],
    )
    p.check(
        "/task/summary" in paths,
        "collection action has no member selector",
    )
    p.check(
        "/task/{item_id}/preview" in paths,
        "member action contains item_id",
    )
    status, _ = await p.request("POST", "/task/preview", {})
    p.check(
        status >= 400, "missing member selector is rejected"
    )
    status, _ = await p.request(
        "POST", "/task/member-1/preview", {}
    )
    p.check(
        status == 200, "member action accepts the selected path"
    )


if __name__ == "__main__":
    run(10, exercise)
