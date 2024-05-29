import sqlite3


class DatabaseHelper:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

    def create_database(self):
        self.cursor.execute('''
                            CREATE TABLE IF NOT EXISTS lands (
                                id INTEGER PRIMARY KEY,
                                name TEXT NOT NULL
                            )
                            ''')
        self.cursor.execute('''
                            CREATE TABLE IF NOT EXISTS rides (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                land_id INTEGER,
                                ride_id INTEGER,
                                name TEXT NOT NULL,
                                is_open BOOLEAN,
                                wait_time INTEGER,
                                last_updated TEXT,
                                UNIQUE(ride_id, last_updated),
                                FOREIGN KEY (land_id) REFERENCES lands(ID)
                            )
                            ''')

    def drop_table(self, table):
        self.cursor.execute(f'DROP TABLE IF EXISTS {table}')
        self.conn.commit()

    def validate_database(self):
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = self.cursor.fetchall()
        table_names = {table[0] for table in tables}
        expected_tables = {'lands', 'rides'}
        if not expected_tables.issubset(table_names):
            print(f"missing tables: {expected_tables - table_names}")
            return False

        # Check table schemas
        expected_schemas = {
            'lands': [('id', 'INTEGER'), ('name', 'TEXT')],
            'rides': [
                ('id', 'INTEGER'), ('land_id', 'INTEGER'),
                ('ride_id', 'INTEGER'), ('name', 'TEXT'),
                ('is_open', 'BOOLEAN'), ('wait_time', 'INTEGER'),
                ('last_updated', 'TEXT')]
            }

        for table, expected_schema in expected_schemas.items():
            self.cursor.execute(f"PRAGMA table_info({table});")
            columns = self.cursor.fetchall()
            column_info = [(col[1], col[2]) for col in columns]

            if column_info != expected_schema:
                print(f"Schema mismatch in {table}: expected {expected_schema}, found {column_info}")
                return False

        print("Database validation passed.")
        return True

    def insert_rides(self, rides):
        try:
            for ride in rides:

                self.cursor.execute('''
                                INSERT INTO rides (land_id, ride_id, name, is_open, wait_time, last_updated)
                                VALUES (?, ?, ?, ?, ?, ?)
                                ''', ride)
            self.conn.commit()

        except sqlite3.Error as e:
            print(f"Error inserting ride: {e}")
            return


    def print_table(self, table):
        # Get column names
        self.cursor.execute(f"PRAGMA table_info({table})")
        columns = [col[1] for col in self.cursor.fetchall()]
        # Fetch and print table data
        self.cursor.execute(f"SELECT * FROM {table}")
        rows = self.cursor.fetchall()
        # Print column names
        print(', '.join(columns))
        # Print table data
        for row in rows:
            print(', '.join(map(str, row)))

    def execute_query(self, query):
        pass

    def fetch_ride_by_id(self, ride_id):
        self.cursor.execute("SELECT * FROM rides WHERE ride_id = ?", (ride_id,))
        return self.cursor.fetchall()

    def fetch_ride_ids_and_names(self):
        self.cursor.execute("SELECT DISTINCT ride_id, name FROM rides")
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()
