#  coding: utf-8
import socketserver
import os
from urllib.parse import urlparse


# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/

class MyWebServer(socketserver.BaseRequestHandler):

    def handle(self):
        self.data = self.request.recv(1024).strip().decode('utf-8')
        # print("Got a request of:\n%s\n" % self.data)
        # self.request.sendall(bytearray("OK", 'utf-8'))
        try:
            # parsed_url = urlparse(self.data)
            # print("this is :" + parsed_url.path[0:3])
            request = self.data.split('\r\n')[0]
            # print('this is request: ' + request)
            method = request.split()[0]
            path = request.split()[1]
            HTTP = request.split()[2]
        except ValueError:
            pass
        except IndexError:
            pass
        # print('this is method: ' + method)
        # print('this is path: ' + path)
        # print('this is HTTP: ' + HTTP)
        folder_name = 'www'
        if not os.path.isdir(folder_name):
            self.request.sendall(b"HTTP/1.1 404 Not Found\n\n")
            self.request.sendall(b"<html><body><h1>404 Not Found</h1></body></html>")
            return
        try:
            if method != 'GET':
                self.request.sendall(b"HTTP/1.1 405 Method Not Allowed\n\n")
                self.request.sendall(b"<html><body><h1>405 Method Not Allowed</h1></body></html>")
                return
        except ValueError:
            pass
        except UnboundLocalError:
            pass
        try:
            temp = path.split(".")
            print(temp)
            print(path[-1])
            if len(temp) == 1:
                if path[-1] == '/':
                    pass
                if path[-1] == 'p':
                    if len(path) == 5:
                        self.request.sendall(b"HTTP/1.1 301 Moved Permanently\n\n")
                        self.request.sendall(b"<html><body><h1>301 Moved Permanently</h1></body></html>")
                        return
                    elif len(path) == 10:
                        self.request.sendall(b"HTTP/1.1 404 Not Found\n\n")
                        self.request.sendall(b"<html><body><h1>404 Not Found</h1></body></html>")
                        return
                # if path[-1] != '/':
                #     self.request.sendall(b"HTTP/1.1 404 Not Found\n\n")
                #     self.request.sendall(b"<html><body><h1>404 Not Found</h1></body></html>")
                #     return
            elif len(temp) != 1:
                if path[-1] == '/':
                    self.request.sendall(b"HTTP/1.1 404 Not Found\n\n")
                    self.request.sendall(b"<html><body><h1>404 Not Found</h1></body></html>")
                    return
        except ValueError:
            pass
        except IndexError:
            pass
        except UnboundLocalError:
            pass
        try:
            if HTTP != 'HTTP/1.1':
                self.request.sendall(b"HTTP/1.1 400 Bad Request\n\n")
                self.request.sendall(b"<html><body><h1>400 Bad Request</h1></body></html>")
                return
        except ValueError:
            pass
        except UnboundLocalError:
            pass
        if path[-1] == '/':
            path = path + 'index.html'
        try:
            file = open('./www' + path)
            file_data = file.read()
            if path.endswith('.html'):
                self.request.sendall(b"HTTP/1.1 200 OK\nContent-Type: text/html\n\n")
            elif path.endswith('.css'):
                self.request.sendall(b"HTTP/1.1 200 OK\nContent-Type: text/css\n\n")
            else:
                self.request.sendall(b"HTTP/1.1 404 Not Found\n\n")
            self.request.sendall(bytearray(file_data, 'utf-8'))
        except FileNotFoundError:
            self.request.sendall(b"HTTP/1.1 404 Not Found\n\n")
            self.request.sendall(b"<html><body><h1>404 Not Found</h1></body></html>")
            return


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
