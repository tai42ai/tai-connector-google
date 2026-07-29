# Contributing to tai42-connector-google

`tai42-connector-google` is a pure connector **provider plugin**: it declares one
`ProviderDescriptor` (the Google provider — Gmail, Calendar, Drive) and registers
it through the `tai42_app` contract handle when the manifest loads it. The hard rule:
**its only dependency is `tai42-contract`** — no `tai42-skeleton`, no other tai-*, no
engine code. All OAuth / probe / launch behavior is generic in the skeleton engine,
keyed off the descriptor.

## Ground rules

- **Import `tai42_contract` only.** No skeleton, no other tai-* package:
  ```bash
  grep -rnE '(from|import)\s+tai(42)?_' src/ | grep -v tai42_contract   # only this plugin's lines
  grep -rn 'tai42_skeleton' src/                                   # must be empty
  ```
- **The plugin ships pure data, no behavior.** `core/connector.py` builds a
  validated `ProviderDescriptor` and calls
  `tai42_app.connectors.register_connector(...)` at import — a plain call, not a
  decorator (the storage/backend plugins decorate a class because they ship
  behavior; a connector does not).
- **Typed package** (`py.typed`). Pyright runs with 0 errors.

## Layout

- `tai42_connector.google.core.connector` — `build_descriptor()` (pure) + the
  manifest-load `register_connector(...)` call.

## Naming

PyPI is a flat namespace with no owner in the path, so distributions carry the
`tai42-` prefix. GitHub repositories keep their `tai-` names, because the
`tai42ai` organisation already namespaces them. Import packages follow the
distribution.

| Surface | Form |
| --- | --- |
| Distribution — PyPI, `pip install`, dependency pins | `tai42-<name>` |
| Import package | `tai42_<name>` |
| GitHub repository | `tai-<name>` |

So a dependency is declared as `tai42-<name>` while its repository is named
`tai-<name>`, and both spellings are correct in their own context.

Connectors are the one exception to the import-package form: they share the
`tai42_connector` namespace package, so this distribution imports as
`tai42_connector.google` rather than `tai42_connector_google`.

Some surfaces are deliberately neither, and must not be renamed: the `tai` CLI
command (`tai42` is an alias), the Prometheus metric namespace (`tai_tool_*`),
`TAI_*` environment variables, and the `tai-plugin.yml` descriptor filename.

## Dev

```bash
uv venv --python 3.13
uv pip install --no-sources --group dev --editable .
uv run --no-sync ruff check .
uv run --no-sync ruff format --check .
uv run --no-sync pyright
uv run --no-sync pytest --cov --cov-report=term-missing
```

`make dev` installs the sibling `tai-contract` repo as an editable install for local cross-repo development.

Before any commit, run a secret scan over `src/` and `tests/` (e.g.
`detect-secrets scan`).

## License

By contributing you agree your contributions are licensed under Apache-2.0.
