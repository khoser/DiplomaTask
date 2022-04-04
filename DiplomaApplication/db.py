import psycopg2
import yaml


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
        self.DB = None
        self.DB_USER = None
        self.DB_PASSWORD = None
        self.DB_HOST = None
        self.DB_PORT = None
        self.conn = None

    def connect(self):
        """Connect to a Postgres database."""
        if self.conn is None:
            with open('secrets.yaml', 'r') as yaml_conf:
                config = yaml.safe_load(yaml_conf)
            self.DB = config['db']['name']
            self.DB_USER = config['db']['oleg']
            self.DB_PASSWORD = config['db']['password']
            self.DB_HOST = config['db']['server']
            self.DB_PORT = config['db']['port']
            try:
                self.conn = psycopg2.connect(
                    host=self.DB_HOST,
                    user=self.DB_USER,
                    password=self.DB_PASSWORD,
                    port=self.DB_PORT,
                    dbname=self.DB
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
