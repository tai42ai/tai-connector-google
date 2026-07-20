"""Google connector provider for the TAI ecosystem.

A pure ``tai42-contract`` plugin: it declares one
:class:`~tai42_contract.connectors.providers.ProviderDescriptor` for Google
(Gmail, Calendar, Drive) and registers it through the ``tai42_app`` handle when the
manifest loads ``tai42_connector.google.core.connector``. It imports ``tai42-contract``
only — no skeleton, no engine code.
"""
