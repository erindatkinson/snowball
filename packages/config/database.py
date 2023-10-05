"""module to manage database"""
from logging import debug
from sqlite3 import connect, Connection, IntegrityError
from contextlib import closing
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
            count_user TEXT DEFAULT '',
            high_score int NOT NULL DEFAULT 0
            );'''
        with closing(self.conn.cursor()) as cur:
            cur.execute(servers)
        self.conn.commit()

    def initialize_server(self, external_id:str, service_type:str):
        """initiallize a server data store for counting"""
        insert = """INSERT INTO servers (external_id, service_type)
        VALUES (?, ?)"""
        try:
            with closing(self.conn.cursor()) as cur:
                cur.execute(insert, (external_id, service_type,))
            self.conn.commit()
        except IntegrityError:
            debug("initializing server already initialized")

    def get_current_count(self, external_id:str):
        """get the current count for the server"""
        with closing(self.conn.cursor()) as cur:
            res = cur.execute(
                "SELECT count, count_user FROM servers WHERE external_id=?;", 
                (external_id,))
            return res.fetchone()

    def increment_count(self, external_id:str, user:str, count:int):
        """set the server count to the given count"""
        query = """UPDATE servers
            SET count = ?,
            count_user = ?,
            highscore = CASE WHEN high_score < ? THEN ? ELSE highs_core END
            WHERE external_id = ?;"""
        with closing(self.conn.cursor()) as cur:
            cur.execute(query, (count, user, count, count, external_id, ))
        self.conn.commit()

    def reset_count(self, external_id:str):
        """reset the count for the server to zero"""
        reset = """UPDATE servers
            SET count = 0,count_user=NULL
            WHERE external_id = ?"""
        with closing(self.conn.cursor()) as cur:
            cur.execute(reset, (external_id,))
        self.conn.commit()

    def get_highscore(self, external_id:str):
        """get the high score for the server"""
        query = """SELECT high_score
        FROM servers
        WHERE external_id = ?"""
        with closing(self.conn.cursor()) as cur:
            res = cur.execute(query, (external_id, ))
            data = res.fetchone()
            if data is not None:
                return data[0]
            else:
                return "unknown"
