import pymysql.cursors
import config

# connect to mysql database
def getConnection():
    logging.info("Opening a connection to mysql database at {0}".format(creds["db-host"]))
    return pymysql.connect(
            host=config.dbHost,
            user=config.dbUser,
            password=config.dbPassword,
            db=config.dbName,
            charset=config.dbCharset,
            cursorclass=pymysql.cursors.DictCursor)

def setupTables(conn):

    # open the file with our database schema sql in it
    f = open('schema', 'r')
    sql = f.read()
    f.close

    # execute it
    with conn.cursor() as cursor:
        cursor.execute(sql)

    conn.commit()
