# Tigrbl developer labs

24 runnable developer lessons using **Tigrbl 0.4.5** and **Tigrcorn 0.3.18**, with exact dependency resolution in `uv.lock`.

## Run the labs

Install [uv](https://docs.astral.sh/uv/), clone this repository, then:

```sh
uv sync --python 3.13 --locked
uv run python serve.py
```

Open `http://127.0.0.1:8782/lab/1`. Each page executes the actual lesson against the local server. The viewer is companion lesson tooling, not a built-in Tigrbl dashboard.

In another terminal:

```sh
uv run python -m lessons.lesson01
uv run python -m lessons.lesson14
uv run python -m lessons.lesson24
uv run python verify_all.py
```

The server must remain running. All 24 lesson numbers are available as independently runnable modules. Every module contains its own assertions and records actual results under `evidence/`. Generated evidence is local and ignored by Git.

## Application source

- `task_app.py`: Task columns, selected hooks, custom operations, HTTP JSON-RPC, and declarative WebSocket app composition.
- `serve.py`: Tigrcorn public API with explicit WebSocket enablement. The default conservative server profile is not assumed to enable socket upgrades.
- `lab_host.py`: companion viewer and lab orchestration; business HTTP/WS execution delegates to the Tigrbl applications.
- `labkit.py`: test instrumentation, captured requests and assertions.
- `lessons/lesson01.py` … `lessons/lesson24.py`: independently runnable checkpoints.

## Learning path

| Lessons | Focus |
|---|---|
| 01–04 | App, table, registration and diagnostics |
| 05–08 | Storage/field/IO specifications, computed output and validation |
| 09–12 | Custom operations, member/collection arity, owner binding and core handlers |
| 13–16 | Operation-specific hooks, handler entry points, rejected paths and protocol comparisons |
| 17–20 | Real WS JSON-RPC calls, framing codecs, horizontal phases and repeated events |
| 21–24 | Lifecycle matrix metadata, hook legality, selector matching and capstone |

Every page supports a results view and a trace/assertion view. Sources, captured requests, responses, trace events, versions and assertions remain distinguishable.

## Boundaries demonstrated honestly

- The status rule rejects unsupported values through a selected `PRE_HANDLER` hook. It does not claim that mutating a payload in a late hook necessarily changes a previously assembled input.
- Lesson 07 uses an explicit custom projection operation that shares a pure producer with its `vcol` declaration. It does not claim automatic virtual-field inclusion in default CRUD responses in this release.
- Lesson 08 proves generated input-model validation separately from the subsequent valid API call.
- Lesson 14 isolates `core`, `dispatch` and `invoke` and asserts the actual fixture's hook sequences. This is not a claim that all entry points are interchangeable or apply every production policy.
- Lesson 17 uses a real network WebSocket call with the `jsonrpc` subprotocol. Lesson 18 compares codecs and a pure core result; its NDJSON portion is not a second network transport demonstration.
- Lesson 23 proves the selector matcher, not universal owner-level framing enforcement.
- Diagnostics describe declarations/plans; teaching trace events describe observed calls. A compiled label is not proof that a stage ran. The demo preserves observed handler repetitions rather than assuming exactly-once execution.
- The matrix helper is inspected as implementation metadata. Its phase subset is not the full operation lifecycle or a complete app/session/unit lifespan state machine.

Use synthetic local data. This teaching app has no authentication policy and is intended for localhost development, not public deployment.

## Reset and recovery

Restart `serve.py` for a fresh in-memory database. Task IDs in exercises are unique per run. If a port is occupied, stop the previous instance before restarting. If a lab fails, its failure evidence is retained; do not turn an expected diagram into a fabricated successful screenshot.

The production pass verified all 24 lessons over the actual localhost server. Re-run the commands on your platform; protocol, schema and error details are version-specific.
