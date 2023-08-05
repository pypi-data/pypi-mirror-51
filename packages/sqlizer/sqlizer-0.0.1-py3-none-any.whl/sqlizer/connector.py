import psycopg2
import logging
import os
import re
from tabulate import tabulate
connections = dict()
logger = logging.getLogger(os.path.dirname(os.path.relpath(__file__)))


def connect(connection_params: dict):
    user = connection_params.get('user')
    passwd = connection_params.get('pass')
    host = connection_params.get('host')
    port = connection_params.get('port')
    db = connection_params.get('db')
    logger.debug(f'Connecting to {user}:{passwd}@{host}:{port}/{db}')
    conn = psycopg2.connect(user=user,
                            password=passwd,
                            host=host,
                            port=port,
                            dbname=db,
                            sslmode='require')  # , async_=True)
    conn.autocommit = True
    return conn


def init_connections(connection_params: dict):
    try:
        for connection_id, connection_set in connection_params.items():
            connections[connection_id] = connect(connection_set)
    except Exception as ex:
        logger.error(f"Couldn't initialize connection due to: [{str(ex)}]. Aborting.")
        raise


class LoggingCursor(psycopg2.extensions.cursor):
    def execute(self, sql, args=None):
        #self.mogrify(sql, args)
        logger.debug('Executing query: {}'.format(re.sub(r"\s+", " ", sql)))
        try:
            psycopg2.extensions.cursor.execute(self, sql, args)
        except Exception as exc:
            logger.error(f"{exc.__class__.__name__}: {exc}")
            raise


def execute_query(connection_id, query):
    if connection_id not in connections:
        raise AttributeError(f"There's no connection with id [{connection_id}]")
    cur = None
    try:
        cur = connections.get(connection_id).cursor(cursor_factory=LoggingCursor)
        cur.execute(query)
        if cur.description:
            column_names = [desc[0] for desc in cur.description]
            content = cur.fetchall()
            print(tabulate(content, headers=column_names, tablefmt='orgtbl'))
        else:
            logger.info(f'Result: {cur.statusmessage}')
    except Exception as exc:
        logger.error(f"Couldn't execute query due to {str(exc)}")
        logger.error(f'query> {query}')
    finally:
        if cur:
            cur.close


def close_all_connections():
    for conn_id, conn in connections.items():
        try:
            logger.info(f'Closing database connection: {conn_id}')
            conn.close()
        except Exception as ex:
            logger.warning(f'Could not close database connection {conn_id} due to {str(ex)}')


dummy_query="select s.nspname as table_schema, \
                s.oid as schema_id,  \
                u.usename as owner \
            from pg_catalog.pg_namespace s \
            join pg_catalog.pg_user u on u.usesysid = s.nspowner \
            order by table_schema;"