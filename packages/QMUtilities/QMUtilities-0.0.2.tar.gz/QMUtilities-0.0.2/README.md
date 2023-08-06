QMUtilities
=============

Its a generic Utils library from where you can import various modules. Below are the modules and their installation steps with usage description

pypi library link: https://pypi.org/project/QMUtilities/

MODULE:1 Config Based IP security
=============

This is a simple security module to check whether client IP is allowed to access the flask`s backend APIs.

Before every endpoint is served, it will check for the remote IP if it exists in the list of white listed IPs and it also checks if it has valid okta token, if it meets both the conditions, it passes through firewall to access API otherwise it throws abort error:

```
HTTPErr: 403 Abort
```


Setup
=====

```
1. Create VirtualENV
2. source VirtualENV
3. pip install 'QMUtilities==0.0.1'
4. create a stored secret at secret manager and store below keys and correspoding values of memcache server
    
    aws_elastic_cache_hostname : <hostname of memcache server>
    port : <port details>
```

``` python
from flask import Flask
from security.validate import ValidateHeader

# Initialize the Flask app
app = Flask(__name__)

# import IP_list from the config file or declare it here

ip_list = <>

secret_name = <secret_name where memcache server access details are saved>

ipcheck= ValidateHeader(app, ip_list, secret_name)

```


Nginx Routing
====

By default headers of the incoming request gets updated with localhost IP when it is passed to the backend Nginx server.
In order to get the real IP of the client/LAN, we need to do following configurations in the nginx config:

```
server {
    real_ip_recursive on;
}

location / {
    proxy_set_header  Host $host;
    proxy_set_header  X-Real-IP $remote_addr;
    proxy_set_header  X-Forwarded-For $remote_addr;
    proxy_set_header  X-Forwarded-Host $remote_addr;
   }
   
```

**sample incoming request header dict after naking above changes in Nginx**
```
{'wsgi.version': (1, 0), 'wsgi.url_scheme': 'http', 
'wsgi.input': '<_io.BufferedReader name=5>', 'wsgi.errors': <_io.TextIOWrapper name='<stderr>' mode='w' encoding='UTF-8'>,
'wsgi.multithread': True, 
'wsgi.multiprocess': False, 'wsgi.run_once': False, 
'werkzeug.server.shutdown': <function WSGIRequestHandler.make_environ.<locals>.shutdown_server at 0x7fba5d1bd598>, 
'SERVER_SOFTWARE': 'Werkzeug/0.14.1', 'REQUEST_METHOD': 'GET', 'SCRIPT_NAME': '', 'PATH_INFO': '/', 'QUERY_STRING': '', 'REMOTE_ADDR': '127.0.0.1', 'REMOTE_PORT': 39534, 'SERVER_NAME': '127.0.0.1', 'SERVER_PORT': '8002', 'SERVER_PROTOCOL': 'HTTP/1.0', 
'HTTP_HOST': '172.30.1.23', 
'HTTP_X_REAL_IP': '10.21.120.11', 
'HTTP_X_FORWARDED_FOR': '10.21.120.11', 
'HTTP_X_FORWARDED_HOST': '10.21.120.11', 
'HTTP_CONNECTION': 'close', 'HTTP_PRAGMA': 'no-cache', 
'HTTP_CACHE_CONTROL': 'no-cache', 'HTTP_UPGRADE_INSECURE_REQUESTS': '1', 
'HTTP_USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36', 
HTTP_ACCEPT': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3', 
'HTTP_ACCEPT_ENCODING': 'gzip, deflate', 'HTTP_ACCEPT_LANGUAGE': 'en-GB,en-US;q=0.9,en;q=0.8', 'werkzeug.request': <Request 'http://10.21.120.11/' [GET]>}

```

MODULE2: Allow access APIs after validating OKTA Tokens
=======

Okta tokens will be read from the headers and validated before accessing any API