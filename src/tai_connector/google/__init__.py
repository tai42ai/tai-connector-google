"""Google connector provider for the TAI ecosystem.

A pure ``tai-contract`` plugin: it declares one
:class:`~tai_contract.connectors.providers.ProviderDescriptor` for Google
(Gmail, Calendar, Drive) and registers it through the ``tai_app`` handle when the
manifest loads ``tai_connector.google.core.connector``. It imports ``tai-contract``
only — no skeleton, no engine code.
"""
