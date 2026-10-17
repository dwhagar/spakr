"""The API version: one integer, kept here and nowhere else.

Bump rule: increase API_VERSION by one in the same change that alters the API
description (routes, parameters, request or response fields, error format,
status codes). Do not bump it for internal changes. After bumping, regenerate
the contract snapshot with `python -m spakr.api.snapshot` and commit it; the
test suite fails if the generated OpenAPI description differs from the
snapshot, or if the snapshot changed without a higher API_VERSION than main.

The URL prefix (/api/v1) is the separate, rarely changing major version for
breaking changes; this integer counts every change, additive ones included.
"""

API_VERSION = 1
