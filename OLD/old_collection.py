import sqlite3
import wikipediaapi
import extract


wiki_wiki = wikipediaapi.Wikipedia(user_agent='MyProjectName (arjmfreelance@gmail.com)', language='en')

def manual_game_create(title: str):
        
        # ask for game details
        # title = input("Enter the name of a game: ")
        plat = ""
        dev = ""
        url = ""

         # create game object
        new_game = Game(title, plat, dev)

        # check game exists on wikipedia before rest of input
        if Collection.game_exists(new_game) == True:      
            new_game.url = wiki_wiki.page(new_game.title).fullurl # need to split this into own function
            print(f"{new_game.title} exists on Wikipedia at {new_game.url}.")   

            # retrieve platform
            new_game.platform = extract.WikiGet.find_platform(extract.WikiGet.get_content(new_game.title))
            print(f"Platform: {new_game.platform}")

            # retrieve developer
            new_game.dev = extract.WikiGet.find_dev(extract.WikiGet.get_content(new_game.title))
            print(f"Developer: {new_game.dev}")

            # retrieve publisher
            new_game.pub = extract.WikiGet.find_publisher(extract.WikiGet.get_content(new_game.title))
            print(f"Publisher: {new_game.pub}")

    
             # scrape summary from wikipedia
            new_game.summary = wiki_wiki.page(new_game.title).summary[:]
            print(f"Summary: {new_game.summary} ")

        else:
            print(f"{new_game.title} not found on Wikipedia.")
            manual_game_create() 

       
        decide = input(f"Do you want to add {new_game.title} to your collection? (Yes/No): ")

        if decide == "Yes":
            Collection.add_game(new_game)
            print(f"{new_game.title} has been added to your collection!")
        elif decide == "No":
            manual_game_create()
        else: 
            print("That is not a valid answer.")    


def manual_game_remove():

        remove_choice = input("What game would you like to remove? ")
        Collection.remove_game(remove_choice)


class Game:
    def __init__(self, title: str, platform: str, dev: str):
        self.title = title
        self.platform = platform    
        self.dev = dev
        self.url = ""
        self.summary = "" 
        self.pub = ""


class Collection:
    def __init__(self):
        self.game_list = {}


    @staticmethod
    def list_games():
        connection = sqlite3.connect('game_collection.db')
        cursor = connection.cursor()
        sql_query = f"""SELECT * FROM collection"""
        cursor.execute(sql_query)
        game_list = [dict(row) for row in cursor.fetchall()]
    
        for game in game_list:
            print(game)
    
    @staticmethod    
    def game_exists(game: Game):        
        return wiki_wiki.page(game.title).exists()

    @classmethod
    def add_game(self, game: Game):
            connection = sqlite3.connect('game_collection.db')
            cursor = connection.cursor()
            sql_insert_query = """
                INSERT INTO collection (name, platform, developer, summary, url, publisher)
                VALUES (?, ?, ?, ?, ?, ?)
                                """
           
            cursor.execute(sql_insert_query, (game.title, game.platform, game.dev, game.summary, game.url, game.pub))
            connection.commit()
    
    @classmethod
    def remove_game(self, game: str):
            connection = sqlite3.connect('game_collection.db')
            cursor = connection.cursor()
            sql_insert_query = """
                DELETE FROM collection WHERE name=?;
                                """
            cursor.execute(sql_insert_query, (game,))
            connection.commit()
    


