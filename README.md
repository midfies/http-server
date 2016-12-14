# http-server
An echo server using Python sockets

----------- coverage: platform linux, python 3.5.2-final-0 -----------
Name                  Stmts   Miss  Cover   Missing
---------------------------------------------------
src/client.py            32      5    84%   11-12, 22-23, 45
src/server.py            42     42     0%   2-65
src/test_servers.py       6      0   100%
---------------------------------------------------
TOTAL                    80     47    41%

---------- coverage: platform linux2, python 2.7.12-final-0 ----------
Name                  Stmts   Miss  Cover   Missing
---------------------------------------------------
src/client.py            32      4    88%   14, 22-23, 45
src/server.py            42     42     0%   2-65
src/test_servers.py       6      0   100%
---------------------------------------------------
TOTAL                    80     46    43%

Server initiates when called.
Server accepts connection with client and message client sends.
Server returns a response based on successful or failure.