import ipaddress
import queue
import sqlite3
import sys
import time
import uuid

from sqlite3 import Error


class LektoServer:
    """Server to be used alongside Lektochat client"""

    def __init__(self, db_name, queue_limit=100, index=False):
        """
        Initializes the database
        :param db_name: The  name of the database
        :param queue_limit: Maximum number of items in deletion queue
        :param index: Whether an index should be created
        :type index: bool
        """
        # TODO: Read option from file
        if index:
            self._createindex()
        # Time between database cleanup
        # TODO: Cleanup every set amount of time. Maybe this should not be implemented in the class, but in the server
        self.deletiontimer = 180000
        self.deletionqueue = queue.Queue(queue_limit)
        self._lastcleanup = time.time()
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
                                            uuid text NOT NULL UNIQUE,
                                            ip text NOT NULL UNIQUE,
                                            connectiontime integer,
                                            lastheard integer
                                        ); """
        if self.database is not None:
            # Obtain a cursor and execute the query
            self.cursor = self.database.cursor()
            self.cursor.execute(sql_create_table)

    def newconnection(self, ip):
        """
        Creates a database entry for a new user and assigns her a unique identifier.
        :param ip: The IP address of the new user as a string
        :return: Returns False if an error was encountered, otherwise returns true.
        :rtype bool:
        """
        sql_query = """INSERT INTO users(id,uuid,ip,connectiontime,lastheard)
                       VALUES(NULL,?,?,strftime('%s','now'),strftime('%s','now'));"""
        clientuuid = uuid.uuid4().hex
        values = (clientuuid, ip)
        try:
            # Test if IP is valid
            ipaddress.ip_address(ip)
        except ValueError:
            print('ERROR: Not a valid IP address!', file=sys.stderr)
            return False
        try:
            # Should be safe from injection
            self.cursor.execute(sql_query, values)
            self.database.commit()
            return True
        except sqlite3.Error as e:
            print('ERROR:', e, file=sys.stderr)
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

    def search(self, searchuuid):
        # TODO: This function will be deleted
        """
        Searches for a certain UUID in the database and returns the IP associated to it
        :param searchuuid: UUID
        :return: IP as a string if search is successful, None if the UUID is not found
        :rtype: str or None
        """
        # Get the IP of the user that matches the given ID
        # If they do not exist return None
        sql_query = "SELECT ip FROM users WHERE uuid=?"
        self.cursor.execute(sql_query, (searchuuid,))
        results = self.cursor.fetchall()
        # Fetchall returns a list of tuples
        if results.__len__() > 0:
            return results[0][0]  # The IP is the third entry in a row
        else:
            return None

    def getallusers(self):
        """
        Returns a tuple containing tuples of type (uuid,ip)
        :rtype: tuple
        """
        # TODO: Use dictionary instead of tuple
        sql_query = "SELECT uuid, ip FROM users"
        self.cursor.execute(sql_query)
        results = self.cursor.fetchall()
        return tuple(results)

    def processqueue(self):
        """
        Executes all the deletions that have been queued
        """
        while not self.deletionqueue.empty():
            try:
                self.cursor.execute(self.deletionqueue.get())
            except sqlite3.Error as err:
                print('ERROR:', err, file=sys.stderr)
        self.database.commit()

    def _createindex(self):
        """
        Creates index of the UUID column for faster searching
        :return: True if creation was successful False if
        :rtype: bool
        """
        try:
            self.cursor.execute("CREATE INDEX uuid_index ON users (uuid)")
            self.database.commit()
            return True
        except sqlite3.Error as err:
            print('ERROR:', err, file=sys.stderr)
            return False

    def updateconnection(self, searchuuid):
        """
        Sets last heard time to now for specified UUID
        """
        sql_query = "UPDATE users SET lastheard=strftime('%s','now') WHERE uuid=?"
        values = (searchuuid,)
        try:
            self.cursor.execute(sql_query, values)
            self.database.commit()
        except sqlite3.Error as err:
            print('ERROR:', err, file=sys.stderr)
            return False

    # TODO: Make queue run every set amount of time
    # TODO: Create uuid index for faster searching
    # TODO: Instead of using usernames to ID users, use UUIDs
    # TODO: Use connection time to identify if user is the same(client side work required)
    # TODO: Add checks
    # TODO: Add authentication (?????)
