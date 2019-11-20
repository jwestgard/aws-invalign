import sqlite3

class Database():

    def __init__(self, file):

        schema = '''CREATE TABLE restored (
                        id INTEGER PRIMARY KEY,
                        md5 TEXT,
                        path TEXT,
                        filename TEXT,
                        share TEXT,
                        sourceFile TEXT,
                        sourceLine INTEGER
                        )'''

        self.conn = sqlite3.connect(file)
        self.cursor = self.conn.cursor()
        self.cursor.execute(schema)
        self.conn.commit()


    def __del__(self):

        self.conn.commit()
        self.conn.close()


    def deposit(self, asset_tuple):

        query = '''INSERT INTO restored (md5, path, sourceFile, sourceLine)
                    VALUES (?, ?, ?, ?)'''

        self.cursor.execute(query, asset_tuple)
        self.conn.commit()
