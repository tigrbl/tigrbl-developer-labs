"""Companion lesson UI. Business HTTP/WS operations remain in Tigrbl apps."""

from pathlib import Path
import asyncio, importlib, json, traceback
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import PythonLexer, JsonLexer
from task_app import app as http_app, socket_app, TRACE

ROOT = Path(__file__).parent
LOCK = asyncio.Lock()


def syntax(value, python=False):
    source = (
        value
        if python
        else json.dumps(value, indent=4, default=str)
    )
    return highlight(
        source,
        PythonLexer() if python else JsonLexer(),
        HtmlFormatter(nowrap=True),
    )


async def respond(
    send, status, body, content_type="application/json"
):
    if isinstance(body, (dict, list)):
        body = json.dumps(body, default=str)
    if isinstance(body, str):
        body = body.encode()
    await send(
        {
            "type": "http.response.start",
            "status": status,
            "headers": [
                (b"content-type", content_type.encode()),
                (b"cache-control", b"no-store"),
            ],
        }
    )
    await send({"type": "http.response.body", "body": body})


async def app(scope, receive, send):
    path = scope.get("path", "")
    if scope["type"] == "websocket":
        return await socket_app(scope, receive, send)
    if scope["type"] == "http" and path.startswith("/lab/"):
        if path == "/lab/trace":
            return await respond(send, 200, list(TRACE))
        if path == "/lab/reset-trace":
            TRACE.clear()
            return await respond(send, 200, {"cleared": True})
        if path == "/lab/brand.png":
            return await respond(
                send,
                200,
                (ROOT / "brand.png").read_bytes(),
                "image/png",
            )
        if path.startswith("/lab/run/"):
            number = int(path.rsplit("/", 1)[-1])
            async with LOCK:
                try:
                    from labkit import execute

                    module = importlib.import_module(
                        f"lessons.lesson{number:02d}"
                    )
                    result = await execute(
                        number, module.exercise
                    )
                    result["formatted_records"] = [
                        syntax(record["value"])
                        for record in result["records"]
                    ]
                    result["formatted_trace"] = syntax(
                        result["trace"]
                    )
                    return await respond(send, 200, result)
                except Exception as error:
                    detail = {
                        "lesson": number,
                        "passed": False,
                        "error": str(error),
                        "traceback": traceback.format_exc(),
                    }
                    (ROOT / "evidence").mkdir(exist_ok=True)
                    (
                        ROOT
                        / "evidence"
                        / f"{number:02d}-failure.json"
                    ).write_text(
                        json.dumps(detail, indent=2), "utf-8"
                    )
                    return await respond(send, 500, detail)
        if path.startswith("/lab/source/"):
            number = int(path.rsplit("/", 1)[-1])
            source = (
                ROOT / "lessons" / f"lesson{number:02d}.py"
            ).read_text("utf-8")
            return await respond(
                send,
                200,
                {
                    "source": source,
                    "highlighted": syntax(source, python=True),
                },
            )
        if path.rsplit("/", 1)[-1].isdigit():
            number = int(path.rsplit("/", 1)[-1])
            assert 1 <= number <= 24
            return await respond(
                send,
                200,
                (ROOT / "viewer.html").read_text("utf-8"),
                "text/html; charset=utf-8",
            )
    return await http_app(scope, receive, send)
