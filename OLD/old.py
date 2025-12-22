import sqlite3
import wikipediaapi
import extract
import game_data
import navigation
import database
from rich.console import Console
from rich.table import Table
from fuzzywuzzy import process, fuzz, utils

wiki_wiki = wikipediaapi.Wikipedia(user_agent='MyProjectName (arjmfreelance@gmail.com)', language='en')

def manual_game_create(choice):
        title = choice[4:]
        plat = ""
        dev = ""
        url = ""
        summary = "" 
        pub = ""
        
        new_game = Game(title, plat, dev, pub, summary, url)
    
        # check game exists on wikipedia before rest of input
        if Collection.game_exists(new_game) == True:      
            
            new_game.platform = extract.WikiGet.find_platform(extract.WikiGet.get_content(new_game.title))
            new_game.dev = extract.WikiGet.find_dev(extract.WikiGet.get_content(new_game.title))
            new_game.pub = extract.WikiGet.find_publisher(extract.WikiGet.get_content(new_game.title))
            line_break = wiki_wiki.page(new_game.title).summary.find("\n")
            new_game.summary = game_data.find_summary(new_game.title)
            new_game.url = wiki_wiki.page(new_game.title).fullurl # need to split this into own function

            # create table
            show_single_game(new_game)
            decide = input(f"\nDo you want to add {new_game.title} to your collection? (Yes/No): ")
        else:
            print(f"{new_game.title} not found on Wikipedia.")
            navigation.main_menu()


        if decide == "Yes":
            Collection.add_game(new_game)
            print()
            print(f"{new_game.title} has been added to your collection!")
            navigation.main_menu()
        elif decide == "No":
            navigation.main_menu()
        else: 
            print("That is not a valid answer.")   
            navigation.main_menu() # need to rework main menu so that chocie etc is baked in - make it self-contained
 
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
    Collection.remove_game(remove_choice)
    print(f"{remove_choice} has been removed from the collection!")


class Game:
    def __init__(self, title: str, platform: str, dev: str, publisher: str, summary: str, url: str):
        self.title = title
        self.platform = ""   
        self.dev = ""
        self.url = ""
        self.summary = "" 
        self.pub = ""

class Collection:
    @staticmethod
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
        
    @staticmethod    
    def game_exists(game: Game):        
        return wiki_wiki.page(game.title).exists()

    @classmethod
    def add_game(self, game: Game):
            connection = sqlite3.connect('game_collection.db')
            cursor = connection.cursor()
            sql_insert_query = """
                INSERT INTO collection (title, platform, developer, summary, url, publisher)
                VALUES (?, ?, ?, ?, ?, ?)
                                """
           
            cursor.execute(sql_insert_query, (game.title, game.platform, game.dev, game.summary, game.url, game.pub))
            connection.commit()
    
    @classmethod
    def remove_game(self, game: str):
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
    