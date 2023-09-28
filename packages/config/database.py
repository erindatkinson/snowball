"""module to manage database"""
from logging import debug
from sqlite3 import connect, Connection, IntegrityError
class Database:
    """the object to manage the access of the database"""
    conn:Connection

    def __init__(self, db_file:str):
        self.conn = connect(db_file)
        self.__schemas()

    def __schemas(self):
        """build out the schema for the server data"""
        servers = '''CREATE TABLE IF NOT EXISTS servers (
            external_id TEXT UNIQUE NOT NULL,
            service_type TEXT NOT NULL,
            count INT NOT NULL DEFAULT 0,
            count_user TEXT DEFAULT ''
            );'''
        cur = self.conn.cursor()
        cur.execute(servers)
        self.conn.commit()

    def initialize_server(self, external_id:str, service_type:str):
        """initiallize a server data store for counting"""
        insert = """INSERT INTO servers (external_id, service_type)
        VALUES (?, ?)"""
        try:
            cur = self.conn.cursor()
            cur.execute(insert, (external_id, service_type,))
            self.conn.commit()
        except IntegrityError:
            debug("initializing server already initialized")

    def get_current_count(self, external_id:str):
        """get the current count for the server"""
        cur = self.conn.cursor()
        res = cur.execute(
            "SELECT count, count_user FROM servers WHERE external_id=?;", 
            (external_id,))
        self.conn.commit()
        return res.fetchone()

    def increment_count(self, external_id:str, user:str, count:int):
        """set the server count to the given count"""
        increment = """UPDATE servers
            SET count = ?,count_user = ?
            WHERE external_id = ?;"""
        cur = self.conn.cursor()
        cur.execute(increment, (count, user, external_id,))
        self.conn.commit()

    def reset_count(self, external_id:str):
        """reset the count for the server to zero"""
        reset = """UPDATE servers
            SET count = 0,count_user=NULL
            WHERE external_id = ?"""
        cur = self.conn.cursor()
        cur.execute(reset, (external_id,))
