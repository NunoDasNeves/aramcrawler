import pymysql.cursors
import config
import logging

# connect to mysql database
def getConnection():
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

def setupTables(sql, conn):
    # execute it
    with conn.cursor() as cursor:
        cursor.execute(sql)

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


