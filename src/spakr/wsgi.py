"""WSGI entry point for Apache mod_wsgi (daemon mode).

    WSGIDaemonProcess spakr python-home=/srv/spakr/venv python-path=/srv/spakr/src
    WSGIProcessGroup spakr
    WSGIApplicationGroup %{GLOBAL}
    WSGIPassAuthorization On
    WSGIScriptAlias / /srv/spakr/src/spakr/wsgi.py

The application object never fails to import: a missing or invalid
config.json in the application root is logged and reported by /api/v1/health as not_configured.
"""

from spakr.api import create_app

application = create_app()
