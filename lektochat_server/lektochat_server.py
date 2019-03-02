import sqlite3
from sqlite3 import Error


class LektoServer:
    # TODO: Index IPs
    def __init__(self, db_name):
        try:
            # Create database in memory
            # TODO: Add option to store database in file
            # self.database = sqlite3.connect(":memory")
            self.database = sqlite3.connect(db_name)
            # Create table for connected users
        except Error as e:
            print(e)
        sql_create_table = """ CREATE TABLE IF NOT EXISTS users (
                                            id integer PRIMARY KEY,
                                            username text NOT NULL,
                                            ip text NOT NULL,
                                            connectiontime integer
                                        ); """
        if self.database is not None:
            # Obtain a cursor and execute the query
            self.cursor = self.database.cursor()
            self.cursor.execute(sql_create_table)

    def newconnection(self, username, ip):
        try:
            sql_query = """INSERT INTO users(id,username,ip,connectiontime) 
                           VALUES(NULL,?,?,strftime('%s','now'));"""
            values = (username, ip)
            # Should be safe from injetion
            self.cursor.execute(sql_query, values)
            self.database.commit()
        except sqlite3.Error as e:
            print(e)

    def disconnect(self, ip):
        # Get the IP we want disconnected
        self.cursor.execute("SELECT * FROM users WHERE ip=?", (ip,))
        results = self.cursor.fetchall()
        sql_query = "DELETE FROM users WHERE id=?"
        self.cursor.execute(sql_query, (results[0][0],))
        self.database.commit()

    # TODO: Method to get all usernames and IPs
    # TODO: Add checks
    # TODO: Add authentication (?????)
    # TODO: Instead of deleting disconnected users "deactivate" them (move to other DB or sth)
