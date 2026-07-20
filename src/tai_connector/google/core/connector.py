"""Google connector provider — pure descriptor + manifest-load registration.

Declares the Google OAuth provider (Gmail, Calendar, Drive) as a single pure
:class:`~tai_contract.connectors.providers.ProviderDescriptor` and registers it
through the ``tai_app`` contract handle when the manifest loads this module.

The plugin carries no OAuth, probe, or launch behavior — all of that is generic
in the skeleton connector engine, keyed off the descriptor. Each sub-service is a
pkg-launched stdio MCP server declared by its ``entry_point`` (the distribution /
console-script name); the engine resolver synthesizes the launch command from the
provider's ``pkg_manager`` + ``pkg_version``. OAuth client credentials are named
by env var (``client_id_env`` / ``client_secret_env``); the engine resolves them
from the process environment at connect time.

Scope sensitivity (Google's own classification) drives what verification the
provider's OAuth app must clear. ``gmail.readonly`` and ``drive.readonly`` are
**restricted** scopes — they require Google's annual CASA third-party security
assessment. ``gmail.send`` and ``calendar.events`` are **sensitive** scopes —
they require Google app verification. ``openid``, ``email``, and ``drive.file``
are non-sensitive. Keep Drive on ``drive.readonly`` + ``drive.file``: broadening
to the full ``drive`` scope would widen data access to the user's entire Drive —
don't.
"""

from __future__ import annotations

from tai_contract.app import tai_app
from tai_contract.connectors.providers import (
    OAuthEndpoints,
    ProviderDescriptor,
    SubServiceDescriptor,
)


def build_descriptor() -> ProviderDescriptor:
    """Build the pure Google provider descriptor (no engine, no side effects)."""
    return ProviderDescriptor(
        id="google",
        kind="oauth",
        origin="system",
        category="communication",
        display_name="Google",
        description="Connect Gmail, Calendar, and Drive.",
        icon_url="/static/connector-icons/google.svg",
        oauth=OAuthEndpoints(
            authorize="https://accounts.google.com/o/oauth2/v2/auth",
            token="https://oauth2.googleapis.com/token",
            revoke="https://oauth2.googleapis.com/revoke",
        ),
        client_id_env="CONNECTORS_GOOGLE_CLIENT_ID",
        client_secret_env="CONNECTORS_GOOGLE_CLIENT_SECRET",
        # Each sub-service runs its own stdio MCP-server process. The package is
        # launched by ``pkg_manager`` (uvx — the servers are Python distributions);
        # ``pkg_version`` left unset means the resolver launches the latest.
        pkg_manager="uvx",
        sub_services={
            "gmail": SubServiceDescriptor(
                id="gmail",
                display_name="Gmail",
                description="List, read, and send mail.",
                scopes=[
                    "openid",
                    "email",
                    "https://www.googleapis.com/auth/gmail.readonly",
                    "https://www.googleapis.com/auth/gmail.send",
                ],
                entry_point="tai-mcp-google-gmail",
            ),
            "calendar": SubServiceDescriptor(
                id="calendar",
                display_name="Calendar",
                description="List, create, update, and delete events.",
                scopes=[
                    "openid",
                    "email",
                    "https://www.googleapis.com/auth/calendar.events",
                ],
                entry_point="tai-mcp-google-calendar",
            ),
            "drive": SubServiceDescriptor(
                id="drive",
                display_name="Drive",
                description=(
                    "Browse files (read-only) and create/upload app-scoped files. "
                    "Pre-existing files are visible only when shared with this app "
                    "via the Drive Picker."
                ),
                scopes=[
                    "openid",
                    "email",
                    "https://www.googleapis.com/auth/drive.readonly",
                    "https://www.googleapis.com/auth/drive.file",
                ],
                entry_point="tai-mcp-google-drive",
            ),
        },
        # ``access_type``/``prompt`` make Google issue a refresh token on first
        # consent; ``include_granted_scopes`` enables incremental authorization so
        # scopes granted in earlier consents carry forward into each new request.
        extra_authorize_params={
            "access_type": "offline",
            "prompt": "consent",
            "include_granted_scopes": "true",
        },
    )


# Manifest-load registration: importing this module registers the provider through
# the bound ``tai_app`` handle. A connector ships pure data, so this is a plain
# call (not a decorator like the storage/backend plugins, which register a class).
tai_app.connectors.register_connector(build_descriptor())
