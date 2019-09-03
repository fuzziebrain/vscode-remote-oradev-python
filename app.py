import cx_Oracle
import os

DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]
DB_SERVICE_NAME = os.environ["DB_SERVICE_NAME"]

CONNECT_STRING = DB_HOST + ":" + DB_PORT + "/" + DB_SERVICE_NAME

## Open a connection pool:
pool = cx_Oracle.SessionPool(dsn=CONNECT_STRING, externalauth=True, 
    homogeneous=False, min=2, max=5, increment=1)
connection = pool.acquire()

## Open a connection without creating a pool:
# connection = cx_Oracle.connect(dsn=CONNECT_STRING)

## Get a cursor, execute a query and then output the result to console.
cur = connection.cursor()

for row in cur.execute("select banner from v$version"):
    print(row[0])

## Closing the connection pool
pool.release(connection)
pool.close()

## 
# connection.close()