import pymysql.cursors
import config
import logging

def getConnection():
    """ Connect to the mysql database with the details in config.py and return the connection object """
    logging.info("Opening a connection to mysql database at {0}".format(config.dbHost))
    try:
        return pymysql.connect(
            host=config.dbHost,
            user=config.dbUser,
            password=config.dbPassword,
            db=config.dbName,
            charset=config.dbCharset,
            cursorclass=pymysql.cursors.DictCursor)
    except:
        logging.error("Could not connect to database!")
        return None

def setupTables(conn):
    """ Setup tables """
    from crawler.schema.match import SCHEMA as CRAWLER_SCHEMA
    from crawler.schema.static import SCHEMA as STATIC_SCHEMA
    bigDict = STATIC_SCHEMA.copy()
    bigDict.update(CRAWLER_SCHEMA)
    queries = []
    for tableName, tableData in bigDict.items():
        queries.append("DROP TABLE IF EXISTS {}".format(tableName))
        rows=[]
        for rowName, rowData in tableData.items():
            rows.append(rowName+" "+rowData['type'])
        queries.append("CREATE TABLE {} ({})".format(tableName, ', '.join(rows)))
    # execute it
    with conn.cursor() as cursor:
        for q in queries:
            print ('    '+q)
            cursor.execute(q)

    conn.commit()

def updateTable(sql, conn):
    """ Update a table and don't return anything """
    logging.info("updating table!")
    logging.info(str(sql))
    # execute it
    with conn.cursor() as cursor:
        for line in sql:
            cursor.execute(line)

    conn.commit()

def getById(sql, conn):
    """ return a single row """
     # execute it
    with conn.cursor() as cursor:
        cursor.execute(sql)
        result = cursor.fetchone()
        return result


