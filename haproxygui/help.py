'''
Created on Jun 2, 2015

@author: nick
'''

HELP_TEXT = {
'maxconn':
'Fix the maximum number of concurrent connections.',

'timeout_connect':
'Set the maximum time to wait for a connection attempt to a server to succeed.',

'timeout_client':
'Set the maximum inactivity time on the client side.',

'timeout_server':
'Set the maximum inactivity time on the server side.',

'timeout_http_request':
'Set the maximum allowed time to wait for a complete HTTP request',

'retries':
'Set the number of retries to perform on a server after a connection failure.',

'option_redispatch':
'Enable or disable session redistribution in case of connection failure.',

'option_persist':
'Enable or disable forced persistence on down servers. \
When an HTTP request reaches a backend with a cookie which references a dead\
server, by default it is redispatched to another server. It is possible to\
force the request to be sent to the dead server first using "option persist"\
if absolutely needed. A common use case is when servers are under extreme\
load and spend their time flapping. In this case, the users would still be\
directed to the server they opened the session on, in the hope they would be\
correctly served. It is recommended to use "option redispatch" in conjunction\
with this option so that in the event it would not be possible to connect to\
the server at all (server definitely dead), the client would finally be\
redirected to another valid server.',

'option_httpclose':
'Enable or disable passive HTTP connection closing.',


'option_log':
'Enable advanced logging of HTTP or TCP connections with session state and timers.',

'mode':
'Set the running mode or protocol of the instance.',

'bind_address':
'Define one listening addresse in a frontend.',

'bind_port':
'Define one listening port in a frontend.',

'no_sslv3':
'It disables support for SSLv3 on any sockets instantiated from the listener when SSL is supported.',

'force_tls':
'This option enforces use of TLS only on SSL connections instantiated from this listener.',

'balance_method':
'Define the load balancing algorithm to be used in a backend. roundrobin : Each server is used in turns, according to their weights. leastconn : The server with the lowest number of connections receives the connection. source : The source IP address is hashed and divided by the total weight of the running servers to designate which server will receive the request.',

'forwardfor':
'Enable insertion of the X-Forwarded-For header to requests sent to servers.',

'forwardfor_expect':
'An optional argument used to disable this option for sources matching <network>.',

'forwardfor_header':
'Used to supply a different header name to replace the default "X-Forwarded-For".',

'cookie':
'Enable cookie-based persistence in a backend. "rewrite" : This keyword indicates that the cookie will be provided by the server and that haproxy will have to modify its value to set the server identifier in it. "insert" : This keyword indicates that the persistence cookie will have to be inserted by haproxy in server responses if the client did not already have a cookie that would have permitted it to access this server. "refix" : This keyword indicates that instead of relying on a dedicated cookie for the persistence, an existing one will be completed.',

'cookie_option_indirect':
'When this option is specified, no cookie will be emitted to a client which already has a valid one for the server which has processed the request.',

'cookie_option_nocache':
'This option is recommended in conjunction with the insert mode when there is a cache between the client and HAProxy, as it ensures that a cacheable response will be tagged non-cacheable if a cookie needs to be inserted.',

'cookie_option_postonly':
'This option ensures that cookie insertion will only be performed on responses to POST requests.',

'cookie_domain':
'This option allows to specify the domain at which a cookie is inserted.',

'ssl_hello_check':
'Use SSLv3 client hello health checks for server testing.',

'http_check':
'Enable HTTP protocol to check on the servers health.',

'http_method':
'HTTP method used with the requests.',

'http_url':
'URI referenced in the HTTP requests.',

'http_check_expect':
'Make HTTP health checks consider response contents or specific status codes. "status <string>" : test the exact string match for the HTTP status code. "rstatus <regex>" : test a regular expression for the HTTP status code. "string <string>" : test the exact string match in the HTTP response body. "rstring <regex>" : test a regular expression on the HTTP response body.',

'disable_on_404':
'Enable a maintenance mode upon HTTP/404 response to health-checks.',

'timeout_check':
'Set additional check timeout, but only after a connection has been already established.',

'weight':
'Used to adjust the servers weight relative to other servers.',

'check':
'This option enables health checks on the server.',

'check_inter':
'Sets the interval between two consecutive health checks.',

'check_fall':
'States that a server will be considered as dead after <count> consecutive unsuccessful health checks.',

'cookie_value':
'Sets the cookie value assigned to the server.',

}
