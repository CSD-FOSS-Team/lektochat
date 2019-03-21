import sqlite3
import ipaddress
import sys
import queue
import time
from sqlite3 import Error


class LektoServer:
    def __init__(self, db_name, queue_limit=100, index=False):
        # TODO: Read option from file
        if index:
            self.createindex()
        # Time between database cleanup
        # TODO: Cleanup every set amount of time
        self.deletiontimer = 180000
        self.deletionqueue = queue.Queue(queue_limit)
        self.lastcleanup = time.time()
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
                                            username text NOT NULL UNIQUE,
                                            ip text NOT NULL,
                                            connectiontime integer
                                        ); """
        if self.database is not None:
            # Obtain a cursor and execute the query
            self.cursor = self.database.cursor()
            self.cursor.execute(sql_create_table)

    def newconnection(self, username, ip):
        """Creates a new entry in the database for a user. Returns True if successful or False if failed"""
        try:
            sql_query = """INSERT INTO users(id,username,ip,connectiontime) 
                           VALUES(NULL,?,?,strftime('%s','now'));"""
            values = (username, ip)
            # Test if IP is valid
            ipaddress.ip_address(ip)
            # Should be safe from injection
            self.cursor.execute(sql_query, values)
            self.database.commit()
            return True
        except sqlite3.Error as e:
            print('ERROR:', e, file=sys.stderr)
            return False
        except ValueError:
            print('ERROR: Not a valid IP address!', file=sys.stderr)
            return False

    def disconnect(self, ip):
        """Get the IP we want disconnected. Return True if deletion is queued successfully and None
        if the IP does not exist in the database"""
        self.cursor.execute("SELECT * FROM users WHERE ip=?", (ip,))
        results = self.cursor.fetchall()
        sql_query = "DELETE FROM users WHERE id=?"
        # If queue is full empty it
        if self.deletionqueue.full():
            while not self.deletionqueue.empty():
                self.cursor.execute(self.deletionqueue.get())
            self.database.commit()
        if len(results) > 0:
            try:
                self.deletionqueue.put(sql_query)
                return True
            except sqlite3.Error as err:
                print(err)
                return False
        return None

    def search(self, username):
        # Get the IP of the user that matches the given ID
        # If they do not exist return None
        sql_query = "SELECT ip FROM users WHERE username=?"
        self.cursor.execute(sql_query, (username,))
        results = self.cursor.fetchall()
        # Fetchall returns a list of tuples
        if results.__len__() > 0:
            return results[0][0]  # The IP is the third entry in a row
        else:
            return None

    def getallusers(self):
        # TODO: Use dictionary instead of tuple
        """Returns a tuple containing tuples of type (username,ip)"""
        sql_query = "SELECT username, ip FROM users"
        self.cursor.execute(sql_query)
        results = self.cursor.fetchall()
        return tuple(results)

    def processqueue(self):
        while not self.deletionqueue.empty():
            self.cursor.execute(self.deletionqueue.get())
        self.database.commit()

    def createindex(self):
        try:
            self.cursor.execute("CREATE INDEX username_index ON users (username)")
            self.database.commit()
            return True
        except sqlite3.Error as err:
            print(err)
            return False
    # TODO: Create username index for faster searching
    # TODO: Instead of using usernames to ID users, use UUIDs
    # TODO: Use connection time to identify if user is the same(client side work required)
    # TODO: Add checks
    # TODO: Add authentication (?????)
