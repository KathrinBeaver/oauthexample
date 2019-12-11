from http.server import BaseHTTPRequestHandler, HTTPServer
from sys import argv

import urllib3
import json

def addRedirectScript():
    fileName = "relocate.js"
    retStr = open(fileName).read()
    return retStr

def getVkClickableLogIn():
    fileName = "getVkClickableLogIn.html"
    strJsCode = open(fileName, encoding="utf-8").read()
    return strJsCode

def getResourse(path):
    return open("." + path, "rb").read()

def getFriendIDs(token):
    urlForFriends = "https://api.vk.com/method/friends.get?v=5.103&"

    http = urllib3.PoolManager()

    response = http.request('GET', urlForFriends + token)
    replyData = json.loads(response.data.decode('utf-8'))
    return replyData

def getFriendsDetails(token, listOfFriends):
    urlForFriendsDetails = "https://api.vk.com/method/users.get?v=5.103&"
    http = urllib3.PoolManager()

    response = http.request('GET', urlForFriendsDetails + token + "&fields=photo_200&user_ids=" + ",".join(map(str, listOfFriends)))
    replyData = json.loads(response.data.decode('utf-8'))
    return replyData

class Server(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_headers()

        if self.path.find("res/") != -1:
            self.wfile.write(getResourse(self.path))
        else:
            self.wfile.write(b"<html>")
            self.wfile.write(b"<head><meta charset=\"utf-8\"></head>")

            if self.path == "/":
                self.wfile.write(getVkClickableLogIn().encode('utf-8'))

            if self.path.find("/callback") != -1:
                self.wfile.write(self.processOAuthToken().encode('utf-8'))
            self.wfile.write(b"</html>")

    def processOAuthToken(self):
        tokenString = ""
        if self.path == "/callback":
            tokenString += addRedirectScript()
            tokenString += "<body><h1>Hi!</h1>"

            tokenString += "<p>"

            tokenString += self.path
            tokenString += "<p>"
        else:
            self.token = self.path.split("?")[1].split("&")[0]
            tokenString += "<h1>Success token!!</h1>"
            tokenString += "<p>"
            tokenString += self.token
            tokenString += "<p>"
            tokenString += "ID ваших друзей:"
            tokenString += "<p>"
            friends = getFriendIDs(self.token)
            items = friends.get("response").get("items")
            tokenString += " ".join(map(str, items))
            tokenString += "<p>"
            friendsDetails = getFriendsDetails(self.token, items)
            tokenString += json.dumps(friendsDetails)
        tokenString += "</body>"
        return tokenString

    def do_HEAD(self):
        self._set_headers()

def run(server_class=HTTPServer, handler_class=Server, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print('Starting httpd...')
    httpd.serve_forever()

if __name__ == "__main__":
    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run(port=5000)
