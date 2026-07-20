"""Bind a fake ``tai_app`` so the connector module's import-time registration
runs without the skeleton.

``tai_connector.google.core.connector`` calls
``tai_app.connectors.register_connector(...)`` at import. The runtime would have
bound the concrete app first; here a recording fake stands in, capturing the
descriptor the plugin registers so the tests can assert on it. Binding happens at
conftest import — before any test module imports the connector.
"""

from __future__ import annotations

from tai_contract.app import tai_app
from tai_contract.connectors.providers import ProviderDescriptor

REGISTERED: list[ProviderDescriptor] = []


class _RecordingConnectors:
    def register_connector(self, descriptor: ProviderDescriptor) -> None:
        REGISTERED.append(descriptor)


class _FakeApp:
    connectors = _RecordingConnectors()


tai_app.bind(_FakeApp())
