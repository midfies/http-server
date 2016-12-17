# HTTP-server

##Initial Phase - 12-12-2016 - 
A echo server built using the python sockets module.  Any response sent from the client to the server is recorded, printed and return back to the client in the same format. 

##Part 1 - 12-13-2016 - 
The server has been updated to respond with generic Status Code 200 responses for success and 500 code for errors as oppose to returning the original message. 

##Part 2 - 12-14-2016 - 
The server has been updated to check for valid HTTP requests from the client.  There are four failure cases at this point:
    1. HTTP Request does not contain all required arguements (Method, URI and Protocol)
    2. HTTP Request contains more than the three required arguements.
    3. HTTP Request is not a GET request.
    4. HTTP Request is not using the HTTP/1.1 Protocol

##Current Issues - 
1. Non-ASCII messages are causing problems with passing tests in Python2.7.
2. Testing only complete as a complete function, no unit test performed.

##Current Test Coverage - 
```
---------- coverage: platform linux2, python 2.7.6-final-0 -----------
Name                  Stmts   Miss  Cover   Missing
---------------------------------------------------
src/client.py            32      4    88%   13, 21-22, 42
src/server.py            63     63     0%   2-83
src/test_servers.py       6      0   100%
---------------------------------------------------
TOTAL                   101     67    34%
```
```
----------- coverage: platform linux, python 3.5.2-final-0 -----------
Name                  Stmts   Miss  Cover   Missing
---------------------------------------------------
src/client.py            32      5    84%   10-11, 21-22, 42
src/server.py            63     63     0%   2-83
src/test_servers.py       6      0   100%
---------------------------------------------------
TOTAL                   101     68    33%
```

##Instructions for Testing - 
1. Open terminal and navigate to client-server directory
2. Run 'python src/server.py' to begin server listening
3. Open new terminal and again navigate to client server-directory
4. If not already done so, install required dependencies with:
    'pip install -e .[test]'
5. Run 'tox' from client-server directory.


