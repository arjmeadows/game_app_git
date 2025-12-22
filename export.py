import sqlite3
import collection
import csv
import database
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

    print(f"Your game collection has been successfully exports as {file_name}.csv!")       


def csv_import(file):
    file_name = file[7:] 
    with open(file_name, "r") as import_file:
        csvreader = csv.DictReader(import_file, delimiter=',')
        table = navigation.game_table()

        for row in csvreader:
            table.add_row(row["Title"], row["Platform"], row["Developer"], row["Publisher"], row["Summary"], row["URL"]) 

    console = Console()
    print("These are the games you want to import to your collection: ")
    console.print(table)
    decision = input("Do you want to add the game(s) above to your collection? (yes/no): ")

    if decision == "yes":
        with open(file_name, "r") as import_file:
            csvreader = csv.DictReader(import_file, delimiter=',')
            for row in csvreader:
                if database.db_read_one(row["Title"]) is not None:
                    new_game = collection.Game(row["Title"], row["Platform"], row["Developer"], row["Publisher"], row["Summary"], row["URL"])
                    dupe = input(f"{row["Title"]} is already in your collection. Do you want to add a duplicate? (yes/no): ")
                    if dupe == "yes": 
                        collection.add_game(new_game)    
                        continue                
                    elif dupe == "no":
                        print(f"{row['Title']} not added to your collection")
                        continue
                else:
                    new_game = collection.Game(row["Title"], row["Platform"], row["Developer"], row["Publisher"], row["Summary"], row["URL"])
                    collection.add_game(new_game)
                    continue

                print("\nThis is your updated collection:")
                collection.list_games()           
    else:
        navigation.main_menu()    
