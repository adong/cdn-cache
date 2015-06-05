from urlparse import parse_qs, urljoin
from urllib import unquote
import urllib2
from bottle import route, run, response, request, abort, debug

cache = {}

@route('/<path:re:.*>')
def index(path):
    if path == 'is-alive':
        return ""

    if request.method == 'HEAD':
        return ""

    opener = urllib2.build_opener()
    opener.addheaders = [('Accept', '*/*'), ('Host', 'localhost')]

    path_pieces = path.split('/')
    base_domain = unquote(path_pieces[0])
    path = "/".join(path_pieces[1:])

    if base_domain and path:
        url = base_domain + "/" + path
        if url in cache:
            url_response = cache[url]
            response_code = url_response['code']
            response_info = url_response['info']
            response_body = url_response['body']
        else:
            url_response = opener.open(url)
            response_info = url_response.info()
            response_body = url_response.read()
            response_code = url_response.getcode()
            cache[url] = {
                "code": response_code,
                "info": response_info,
                "body": response_body
            }

        response.status = response_code
        for header in response_info.headers:
            header_parts = header.split(':')
            if header_parts[0].lower().strip() in ['connection', 'keep-alive', 'proxy-authenticate', 'proxy-authorization', 'te', 'trailers', 'transfer-encoding', 'upgrade']:
                continue
            response.set_header(header_parts[0], ":".join(header_parts[1:])[:-2])

        return response_body

    abort(404)

run(host='localhost', port=8890, server='cherrypy')