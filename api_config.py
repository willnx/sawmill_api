"""
Gunicorn WSGI configuation.
"""

import ssl


keepalive = 30  # seconds
threads = 200
workers = 1
wsgi_app = "sawmill_api.app:make_app()"
bind = "0.0.0.0:8000"


# TLS config
def ssl_context(address, port):
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(
        keyfile="/opt/sawmill/certs/api.key",
        certfile="/opt/sawmill/certs/api.cert",
    )
    # Disable TLS 1 and 1.1
    context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1
    return context


# Logging
errorlog = "-"  # stderr
accesslog = "/dev/null"
