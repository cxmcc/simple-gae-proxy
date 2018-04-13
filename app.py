
from google.appengine.ext import vendor
vendor.add('lib')
import logging

import requests
from requests_toolbelt.adapters import appengine
appengine.monkeypatch()

from flask import Flask, request, Response

app = Flask(__name__)

TARGET = 'https://cxm.cc/'
`
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def inspect(path):
    proxied_url = '{}{}'.format(TARGET, path)
    resp = requests.request(
        request.method,
        proxied_url,
        data=request.data,
        files=request.files,
        headers=dict(request.headers))
    return Response(
        resp.content,
        headers=dict(resp.headers),
        status=resp.status_code)

@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
        An internal error occurred: <pre>{}</pre>
        See logs for full stacktrace.
        """.format(e), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
