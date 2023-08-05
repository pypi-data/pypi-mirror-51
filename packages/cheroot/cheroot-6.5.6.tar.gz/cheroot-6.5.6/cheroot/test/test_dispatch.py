"""Tests for the HTTP server."""
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8 :

from __future__ import absolute_import, division, print_function

from cheroot.wsgi import PathInfoDispatcher


def wsgi_invoke(app, environ):
    """Serve 1 requeset from a WSGI application."""
    response = {}

    def start_response(status, headers):
        response.update({
            'status': status,
            'headers': headers,
        })

    response['body'] = b''.join(
        app(environ, start_response),
    )

    return response


def test_dispatch_no_script_name():
    """Despatch despite lack of SCRIPT_NAME in environ."""
    # Bare bones WSGI hello world app (from PEP 333).
    def app(environ, start_response):
        start_response(
            '200 OK', [
                ('Content-Type', 'text/plain; charset=utf-8'),
            ],
        )
        return [u'Hello, world!'.encode('utf-8')]

    # Build a dispatch table.
    d = PathInfoDispatcher([
        ('/', app),
    ])

    # Dispatch a request without `SCRIPT_NAME`.
    response = wsgi_invoke(
        d, {
            'PATH_INFO': '/foo',
        },
    )
    assert response == {
        'status': '200 OK',
        'headers': [
            ('Content-Type', 'text/plain; charset=utf-8'),
        ],
        'body': b'Hello, world!',
    }
