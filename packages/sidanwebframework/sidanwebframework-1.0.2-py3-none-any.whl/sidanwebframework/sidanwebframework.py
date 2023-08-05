from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, unquote
from json import dumps, loads
from os import getcwd

path_arr = []

class Serv(BaseHTTPRequestHandler):

    def do_OPTIONS(self):
        setCorsHeaders(self)
        self.end_headers()


    def do_POST(self):
        processUrl(self, 'POST')


    def do_GET(self):
        if len(path_arr) == 0:
            response = "\
                <html>\
                    <head>\
                        <title>sidanwebframework</title>\
                    </head>\
                    <body>\
                    <h2>\
                        sidanwebframework is successfully\
                        running\
                    </h2>\
                    </body>\
                </html>"
            self.send_response(200)
            sendResponse(self, response)
        processUrl(self, 'GET')
    
    
    def do_PUT(self):
        processUrl(self, 'PUT')
    
    
    def do_DELETE(self):
        processUrl(self, 'DELETE')


class Server:

    class Settings:
        def __init__(self, ip, port, cors={"allow": False}):
            self.ip = ip
            self.port = port
            self.cors = cors

    settings = Settings('127.0.0.1', 8080)
    def serve(self):
        """ ``serve()`` call this method to start the server."""
        try:
            httpd = HTTPServer((Server.settings.ip, Server.settings.port), Serv)
            link = 'http://{}:{}'.format(Server.settings.ip, Server.settings.port)
            prGreen('Server running at ' + link)
            httpd.serve_forever()
            return True
        except KeyboardInterrupt:
            httpd.socket.close()
            prRed('Server stopped')
        except OSError:
            prRed('Port busy')


class Request:

    def __init__(self, method, headers, body, params):
        self.method = method
        self.headers = headers
        self.body = body
        self.params = params


class Route:

    def __init__(self, path, function):
        self.path = path
        self.function = function


def setCorsHeaders(self):
    if Server.settings.cors['allow']:
        self.send_response(200)
        self.send_header('Access-Control-Allow-Credentials', 'true')
        if 'origin' in Server.settings.cors:
            if self.headers.get('Origin') in Server.settings.cors['origin']:
                self.send_header('Access-Control-Allow-Origin', self.headers.get('Origin'))
            else:
                self.send_response(403)
                self.send_header('Access-Control-Allow-Credentials', 'false')
        else:
            self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'X-Requested-With, Content-type')
    else:
        self.send_response(403)


def route(path):
    """
    ``@route()`` use this decorator to define the route, pass path as argument
    """
    def wrap(func):
        path_obj = Route(path, func)
        path_arr.append(path_obj)
    return wrap


def processUrl(self, method):
    query = urlparse(self.path).query
    url_params = {}
    if len(query) > 1:
        url_params = dict(qc.split('=') for qc in query.split('&'))
    path = self.path
    if self.path.find('?') != -1:
        path = self.path[0:self.path.find('?')]
    flag = 0
    for obj in path_arr:
        if obj.path == path:
            req_body = {}
            if self.headers.get('Content-Length') is not None:
                req_body = self.rfile.read(int(self.headers.get('Content-Length')))
            if len(req_body) > 0:
                if self.headers.get('Content-Type') == 'application/json':
                    req_body = loads(req_body)
                else:
                    req_body = req_body.decode("utf-8")
                    req_body = unquote(req_body)
                    if '+' in req_body:
                        req_body = req_body.replace('+', ' ')
                    req_body = dict(qc.split('=') for qc in req_body.split('&'))
            req_obj = Request(method, self.headers, req_body, url_params)
            response = obj.function(req_obj)
            if response is None:
                prRed('{} does have return statement'.format(obj.path))
                response = '{} does have return statement'.format(obj.path)
            self.send_response(200)
            setCorsHeaders(self)
            sendResponse(self, response)
            return True
        flag = flag + 1
        if flag == len(path_arr):
            self.send_response(404)
            prYellow('404 > Path not found')
            sendResponse(self, "Path not found")


def response(data):
    """``response()`` return this function with arguments, the arguments can be JSON type or String."""
    try:
        if type(data) == dict:
            return dumps(data)
        return str(data)
    except:
        return data


def render(FilePath, context={}):
    """ ``render()`` render the html document with given optional context  """
    try:
        file_obj = open(getcwd() + '/' + FilePath)
        data = file_obj.read()
        keys = list(context.keys())
        to_replace = []
        for index, char in enumerate(data):
            if char == '{':
                if data[index+1] == '{':
                    start = index
            if char == '}':
                if data[index+1] == '}':
                    stop = index
                    if data[start+2:stop] in keys:
                        rp_obj = {
                            "key": data[start-1:stop+2],
                            "value": context[keys[keys.index(data[start+2:stop])]]
                        }
                        to_replace.append(rp_obj)
                    else:
                        rp_obj = {
                            "key": data[start-1:stop+2],
                            "value": ""
                        }
                        to_replace.append(rp_obj)
        for obj in to_replace:
            data = data.replace(obj['key'], str(obj['value']))
        file_obj.close()
        return data
    except Exception as e:
        return str(e)


def sendResponse(self, response):
    try:
        response = loads(response)
        response = dumps(response)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(bytes(response, 'utf-8'))
    except:
        response = str(response)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        self.wfile.write(bytes(response, 'utf-8'))


def prRed(args): print("\033[91m {}\033[00m" .format(args))
def prGreen(args): print("\033[92m {}\033[00m" .format(args))
def prYellow(args): print("\033[93m {}\033[00m" .format(args))
