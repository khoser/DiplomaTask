import psycopg2
import yaml

yaml_conf = 'secrets.yaml'
CONFIG = yaml.safe_load(yaml_conf)
DB = CONFIG['db']['name']
DB_USER = CONFIG['db']['oleg']
DB_PASSWORD = CONFIG['db']['password']
DB_HOST = CONFIG['db']['server']
DB_PORT = CONFIG['db']['port']


class Database:
    """PostgreSQL Database class."""

    def __init__(
            self
            # ,DB_HOST,
            # DB_USER,
            # DB_PASSWORD,
            # DB_PORT,
            # DB
    ):
        self.host = DB_HOST
        self.username = DB_USER
        self.password = DB_PASSWORD
        self.port = DB_PORT
        self.dbname = DB
        self.conn = None

    def connect(self):
        """Connect to a Postgres database."""
        if self.conn is None:
            try:
                self.conn = psycopg2.connect(
                    host=self.host,
                    user=self.username,
                    password=self.password,
                    port=self.port,
                    dbname=self.dbname
                )
            except psycopg2.DatabaseError as e:
                raise e

    def select(self, query):
        """Run a SQL query to select rows from table."""
        self.connect()
        with self.conn.cursor() as cur:
            cur.execute(query)
            records = [row for row in cur.fetchall()]
            cur.close()
            return records

    def execute(self, query):
        """Run a SQL query with no result - insert or update or delete etc"""
        self.connect()
        with self.conn.cursor() as cur:
            cur.execute(query)
            self.conn.commit()
            cur.close()
