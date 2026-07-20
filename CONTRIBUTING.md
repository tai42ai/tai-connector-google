# Contributing to tai-connector-google

`tai-connector-google` is a pure connector **provider plugin**: it declares one
`ProviderDescriptor` (the Google provider — Gmail, Calendar, Drive) and registers
it through the `tai_app` contract handle when the manifest loads it. The hard rule:
**its only dependency is `tai-contract`** — no `tai-skeleton`, no other tai-*, no
engine code. All OAuth / probe / launch behavior is generic in the skeleton engine,
keyed off the descriptor.

## Ground rules

- **Import `tai_contract` only.** No skeleton, no other tai-* package:
  ```bash
  grep -rnE '(from|import)\s+tai_' src/ | grep -v tai_contract   # only this plugin's lines
  grep -rn 'tai_skeleton' src/                                   # must be empty
  ```
- **The plugin ships pure data, no behavior.** `core/connector.py` builds a
  validated `ProviderDescriptor` and calls
  `tai_app.connectors.register_connector(...)` at import — a plain call, not a
  decorator (the storage/backend plugins decorate a class because they ship
  behavior; a connector does not).
- **Typed package** (`py.typed`). Pyright runs with 0 errors.

## Layout

- `tai_connector.google.core.connector` — `build_descriptor()` (pure) + the
  manifest-load `register_connector(...)` call.

## Dev

```bash
uv sync
uv run ruff check .
uv run ruff format --check .
uv run pyright
uv run pytest
```

For local cross-repo work, `make dev` editable-installs the sibling `tai-*`
checkouts this package builds on into the venv. While `[tool.uv.sources]` pins
those siblings to local paths, `uv sync` already installs them editable and
`make dev` changes nothing; once the lock resolves them from the registry,
`uv sync` / `uv run` installs the published builds instead, so re-run
`make dev` afterward to restore the editable links.

Before any commit, run a secret scan over `src/` and `tests/` (e.g.
`detect-secrets scan`).

## License

By contributing you agree your contributions are licensed under Apache-2.0.
