"""Bind a fake ``tai42_app`` so the connector module's import-time registration
runs without the skeleton.

``tai42_connector.google.core.connector`` calls
``tai42_app.connectors.register_connector(...)`` at import. The runtime would have
bound the concrete app first; here a recording fake stands in, capturing the
descriptor the plugin registers so the tests can assert on it. Binding happens at
conftest import — before any test module imports the connector.
"""

from __future__ import annotations

from tai42_contract.app import tai42_app
from tai42_contract.connectors.providers import ProviderDescriptor

REGISTERED: list[ProviderDescriptor] = []


class _RecordingConnectors:
    def register_connector(self, descriptor: ProviderDescriptor) -> None:
        REGISTERED.append(descriptor)


class _FakeApp:
    connectors = _RecordingConnectors()


tai42_app.bind(_FakeApp())
