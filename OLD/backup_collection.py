import sqlite3
import wikipediaapi


wiki_wiki = wikipediaapi.Wikipedia(user_agent='MyProjectName (arjmfreelance@gmail.com)', language='en')

def manual_game_create():
        
        # ask for game details
        title = input("Game name: ")
        plat = input("Platform: ")
        dev = input("Developer: ")

        # create game object
        new_game = Game(title, plat, dev)

        # scrape summary from wikipedia
        if Collection.game_exists(new_game) == True:
            new_game.summary = new_game.title.summary[:300]

        # pass into database
        Collection.add_game(new_game)


class Game:
    def __init__(self, title: str, platform: str, dev: str):
        self.title = title
        self.platform = platform    
        self.dev = dev
        self.summary = "NAH" 


class Collection:
    def __init__(self):
        pass

    @staticmethod    
    def game_exists(game: Game):        
        return wiki_wiki.page(game.title)

    @classmethod
    def add_game(self, game: Game):
            connection = sqlite3.connect('game_collection.db')
            cursor = connection.cursor()
            sql_insert_query = """
                INSERT INTO collection (name, platform, developer, summary)
                VALUES (?, ?, ?, ?)
                                """
           
            cursor.execute(sql_insert_query, (game.title, game.platform, game.dev, game.summary))
            connection.commit()
    
    def remove_game(self, game: Game):
        pass
