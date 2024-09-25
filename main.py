import mysql.connector
import mysql.connector
from mysql.connector import Error
from datetime import datetime

HOST = 'localhost'
USER = 'root'
PASSWORD = 'B1gGamingGamer123!'
DATABASE = 'assignment1'


def create_connection():
    try:
        connection = mysql.connector.connect(
            host = HOST,
            user = USER,
            password = PASSWORD,
            database = DATABASE,
            autocommit=False
        )
        if connection.is_connected():
            print('it workey')
            return connection

    except Error as e:
        print(f"Error: {e}")
    print('gamer')
    return None


def read_uncommitted():

    connection1 = create_connection()
    connection2 = create_connection()
    
    try:
        cursor1 = connection1.cursor()
        cursor2 = connection2.cursor()

        print(f"Transaction 1 started: {datetime.now()}")
        connection1.start_transaction(isolation_level='READ UNCOMMITTED')
        cursor1.execute("UPDATE cheeseburgers SET type = 'double beef patty' WHERE name = 'Big burger slam'")

        print(f"Transaction 2 started: {datetime.now()}")
        connection2.start_transaction(isolation_level='READ UNCOMMITTED')
        cursor2.execute("SELECT type FROM cheeseburgers WHERE name = 'Big burger slam'")

        burger_dirty_read = cursor2.fetchone()[0]
        print(f"Dirty Read (READ UNCOMMITTED): Big burger slam burger type: {burger_dirty_read}")

        print(f"Transaction 1 rollback(): {datetime.now()}")
        connection1.rollback()

        cursor1.execute("SELECT type FROM cheeseburgers WHERE name = 'Big burger slam'")
        burger_verify_read = cursor1.fetchone()[0]
        print(f"Rollback verification from cursor 1: Big burger slam burger type: {burger_verify_read}")

        print(f"Transaction 2 commit(): {datetime.now()}")
        connection2.commit()

    except Error as e:
        print(f"Error: {e}")
    
    finally:
        if cursor1:
            cursor1.close()
        if connection1 and connection1.is_connected():
            connection1.close()
        if cursor2:
            cursor2.close()
        if connection2 and connection2.is_connected():
            connection2.close()

#this function illustrates how a non-repeatable read would occur this the sequence of it algorithm
def read_committed():
    connection1 = create_connection()
    connection2 = create_connection()
    
    try:
        cursor1 = connection1.cursor()
        cursor2 = connection2.cursor()

        print(f"Transaction 1 started: {datetime.now()}")
        connection1.start_transaction(isolation_level='READ COMMITTED')
        cursor1.execute("SELECT type FROM cheeseburgers WHERE name = 'Big burger slam'")
        burger_verify_read = cursor1.fetchone()[0]
        print(f"Pre-commit verification from cursor 1: Big burger slam burger type: {burger_verify_read}")

        print(f"Transaction 2 started: {datetime.now()}")
        connection2.start_transaction(isolation_level='READ COMMITTED')
        cursor2.execute("UPDATE cheeseburgers SET type = 'double beef patty' WHERE name = 'Big burger slam'")
        cursor2.execute("SELECT type FROM cheeseburgers WHERE name = 'Big burger slam'")
        burger_commit_read = cursor2.fetchone()[0]
        print(f"Commit verification from cursor 2: Big burger slam burger type: {burger_commit_read}")

        print(f"Transaction 2 rollback(): {datetime.now()}")
        connection2.rollback()

        cursor1.execute("SELECT type FROM cheeseburgers WHERE name = 'Big burger slam'")
        burger_verify_read = cursor1.fetchone()[0]
        print(f"Rollback verification from cursor 1: Big burger slam burger type: {burger_verify_read}")

        print(f"Transaction 1 commit(): {datetime.now()}")
        connection1.commit()

        print(f"Transaction 2 commit(): {datetime.now()}")
        connection2.commit()

    except Error as e:
        print(f"Error: {e}")
    
    finally:
        if cursor1:
            cursor1.close()
        if connection1 and connection1.is_connected():
            connection1.close()
        if cursor2:
            cursor2.close()
        if connection2 and connection2.is_connected():
            connection2.close()


read_committed()
