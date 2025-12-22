import sqlite3
import collection
import csv
import navigation
from rich.console import Console

def csv_export(file_name):
    file_name = file_name[7:]
    connection = sqlite3.connect('game_collection.db')
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM collection")
    result=cursor.fetchall()

    with open (file_name + ".csv", "w") as csv_export:
        writer = csv.writer(csv_export)
        writer.writerow(["Title","Platform","Developer","Publisher","Summary","URL"])
        
    for row in result:
        writer.writerow([row["title"],row["platform"],row["developer"],row["publisher"],row["summary"],row["url"]])


def csv_import(file):
    file_name = file[7:] 
    with open(file_name, "r") as import_file:
        csvreader = csv.DictReader(import_file, delimiter=',')
        table = navigation.game_table()

        for row in csvreader:
            table.add_row(row["Title"], row["Platform"], row["Developer"], row["Publisher"], row["Summary"], row["URL"]) 

    console = Console()
    console.print(table)
    decision = input("Do you want to add the game(s) above to your collection? (yes/no): ")

    if decision == "yes":
        with open(file_name, "r") as import_file:
            csvreader = csv.DictReader(import_file, delimiter=',')
            for row in csvreader:
                new_game = collection.Game(row["Title"], row["Platform"], row["Developer"], row["Publisher"], row["Summary"], row["URL"])
                collection.add_game(new_game)   
          
        print("\nThis is your updated collection:")
        collection.list_games()            
    else:
        navigation.main_menu()    
