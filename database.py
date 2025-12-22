import sqlite3


def create_db():
    connection = sqlite3.connect('game_collection.db')
    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS collection (
            title TEXT,
            platform TEXT,
            developer TEXT,
            publisher TEXT, 
            summary TEXT,
            url TEXT            
        )
    ''')

    connection.commit()


# not in use
def access_db():
        connection = sqlite3.connect('game_collection.db')
        cursor = connection.cursor()    


def db_read_one(choice: str):
        connection = sqlite3.connect('game_collection.db')
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        sql_insert_query = """
            SELECT * FROM collection WHERE title=?;
                            """
        cursor.execute(sql_insert_query, (choice,))
        result = cursor.fetchone()

        return result        