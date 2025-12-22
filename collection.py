import sqlite3
import game_data
import navigation
import database
from rich.console import Console
from rich.table import Table
from fuzzywuzzy import process, fuzz, utils

class Game:
    def __init__(self, title: str, platform: str, dev: str, publisher: str, summary: str, url: str):
        self.title = title
        self.platform = platform  
        self.dev = dev
        self.url = url
        self.summary = summary 
        self.pub = publisher


def manual_game_create(choice):
    title = choice[4:]
    summary = game_data.find_summary(title)
    dev = game_data.find_dev(title)
    plat = game_data.find_platform(title)
    pub = game_data.find_publisher(title)
    url = game_data.find_url(title)

    new_game = Game(title, plat, dev, pub, summary, url)

    show_single_game(new_game)
    decide = input(f"\nDo you want to add {title} to your collection? (yes/no): ")

    if decide == "yes":
        if dupe_check(title) is None:
            add_game(new_game)
            print()
            print(f"{title} has been added to your collection!")
            navigation.main_menu()
        else:
            print(f"{title} is already in your collection!")    
    elif decide == "no":
        navigation.main_menu()
    else: 
        print("That is not a valid option.")   
        navigation.main_menu()
 

def manual_game_remove(choice):
    remove_choice = choice[7:]
    # think this has broken remove
    table = navigation.game_table()
    
    try:
        table.add_row(*database.db_read_one(remove_choice))
    except:
        print("Game was not found in the collection.")
        navigation.main_menu()   

    console = Console()
    console.print(table)
    print()
    input(f"Would you like to remove {remove_choice}? ")
    remove_game(remove_choice)
    print(f"{remove_choice} has been removed from the collection!")


def list_games():
    connection = sqlite3.connect('game_collection.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM collection")
    result=cursor.fetchall()

    table = navigation.game_table()

    for row in result:
        table.add_row(*(str(item) for item in row))

    console = Console()
    console.print(table)
    navigation.main_menu()
    
    
def add_game(game: Game):
    connection = sqlite3.connect('game_collection.db')
    cursor = connection.cursor()
    sql_insert_query = """
        INSERT INTO collection (title, platform, developer, summary, url, publisher)
        VALUES (?, ?, ?, ?, ?, ?)
                        """
    
    cursor.execute(sql_insert_query, (game.title, game.platform, game.dev, game.summary, game.url, game.pub))
    connection.commit()


def remove_game(game: str):
    connection = sqlite3.connect('game_collection.db')
    cursor = connection.cursor()
    sql_insert_query = """
        DELETE FROM collection WHERE title=?;
                        """
    cursor.execute(sql_insert_query, (game,))
    connection.commit()


def search_collection(choice):
    query = choice[7:]
    connection = sqlite3.connect('game_collection.db')
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM collection")
    result=cursor.fetchall()
    database_read = [(row['title']) for row in result]    
    search_result = (process.extract(query, database_read, scorer=fuzz.token_set_ratio, processor=utils.full_process, limit=3))
    table = navigation.game_table()
   
    for result in search_result:
        if result[1] > 80:
            sql = "SELECT * FROM collection where title=?"
            cursor.execute(sql, [result[0]])
            result_db=cursor.fetchall() # returns tuples

            for tup in result_db:
                table.add_row(*(str(item) for item in tup))


    console = Console()
    console.print(table)
    

def show_single_game(game_info):

    table = navigation.game_table()
    game_details = [game_info.title, game_info.platform, game_info.dev, game_info.pub, game_info.summary, game_info.url]
    
    # populate table          
    table.add_row(*game_details)
    
    console = Console()
    console.print(table)
    

def dupe_check(choice):
    return database.db_read_one(choice)
    
        