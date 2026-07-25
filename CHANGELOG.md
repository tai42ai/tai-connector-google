# Changelog

All notable changes to `tai42-connector-google` are documented here; the format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project adheres to
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

Until 1.0.0 the descriptor surface is not stable: **minor (0.x) releases may
contain breaking changes.**

## [Unreleased]

First release (0.1.0) in preparation — nothing published yet.

### Added

- Descriptor authorize params now set `include_granted_scopes=true`, enabling
  Google's incremental authorization so scopes granted in earlier consents carry
  forward into each new authorization request.
