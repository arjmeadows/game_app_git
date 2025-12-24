from rich.console import Console
from rich.panel import Panel
from rich.table import Table
import sys, os
import collection
import export
import config
import getpass


config.TWITCH_CLIENT_ID = None
config.TWITCH_TOKEN = None


def setup_app():
    # Set Terminal Title
    sys.stdout.write("\x1b]2;Game Collector Pro v1.0\x07")
    os.system('mode con: cols=1000 lines=1000')


def print_logo():
    logo = r"""

  ________  ________  _____ ______   _______           ________  ________  ___       ___       _______   ________ _________  ________     
|\   ____\|\   __  \|\   _ \  _   \|\  ___ \         |\   ____\|\   __  \|\  \     |\  \     |\  ___ \ |\   ____|\___   ___|\   __  \    
\ \  \___|\ \  \|\  \ \  \\\__\ \  \ \   __/|        \ \  \___|\ \  \|\  \ \  \    \ \  \    \ \   __/|\ \  \___\|___ \  \_\ \  \|\  \   
 \ \  \  __\ \   __  \ \  \\|__| \  \ \  \_|/__       \ \  \    \ \  \\\  \ \  \    \ \  \    \ \  \_|/_\ \  \       \ \  \ \ \   _  _\  
  \ \  \|\  \ \  \ \  \ \  \    \ \  \ \  \_|\ \       \ \  \____\ \  \\\  \ \  \____\ \  \____\ \  \_|\ \ \  \____   \ \  \ \ \  \\  \| 
   \ \_______\ \__\ \__\ \__\    \ \__\ \_______\       \ \_______\ \_______\ \_______\ \_______\ \_______\ \_______\  \ \__\ \ \__\\ _\ 
    \|_______|\|__|\|__|\|__|     \|__|\|_______|        \|_______|\|_______|\|_______|\|_______|\|_______|\|_______|   \|__|  \|__|\|__|
                                                                                                                                                                                                                                 
    Store, review, and export your game collection with this retro Python program!                                                                                         
    This program was written by Adam Meadows (adamrjmeadows.com).
    """

    print(logo)


def get_user_credentials():

    if config.TWITCH_CLIENT_ID == None and config.TWITCH_TOKEN == None:
        print("This program retrieves information from the Internet Game Database (IGDB). This requires a Client Twitch ID and token.\n")
        print("If you want to use GAME COLLECTR without retrieving information from IGDB, you can use the example database included or add games manually.\n")
        print("For instructions on how to obtain a Twitch Client ID and Token, refer to https://api-docs.igdb.com/#getting-started\n")
        use_Twitch = input("Do you want to provide Twitch credentials? This won't be stored in the GAME COLLECTR database (yes/no): ")

        if use_Twitch == "yes":

            config.TWITCH_CLIENT_ID = getpass.getpass("Enter Twitch Client ID (hidden): ")
            config.TWITCH_TOKEN = getpass.getpass("Enter Twitch Token (hidden): ")
            
        else:
            main_menu()


def main_menu():

    console = Console()

    menu_content = (
        "[bold cyan]get[/bold cyan] [italic white]<title>[/italic white] | "
        "[bold cyan]add[/bold cyan] [italic white]<title>[/italic white] | "
        "[bold red]remove[/bold red] [italic white]<title>[/italic white] | "
        "[bold green]list[/bold green] | "
        "[bold blue]search[/bold blue] [italic white]<term>[/italic white] | "
        "[bold purple]export (CSV)[/bold purple] [italic white]<filename>[/italic white] | "
        "[bold yellow]import (CSV)[/bold yellow] [italic white]<filename.csv>[/italic white] | "
        "[bold white]exit[/bold white]\n"
        "──────────────────────────────────────────────────────────────────────────────────────────\n"
        "[dim]Examples:[/dim]  [bold blue]search[/bold blue] [white]Halo 2[/white]  •  "
        "[bold cyan]add[/bold cyan] [white]Halo 2[/white]  •  "
        "[bold purple]export[/bold purple] [white]games[/white]  •  "
        "[bold yellow]import[/bold yellow] [white]games.csv[/white]"
        "[bold yellow]enter Twitch credentials[/bold yellow] [white]twitch[/white]"
    )

    console.print(Panel(menu_content, title="GAME COLLECTR MENU", expand=False))
    choice = console.input("[bold green]>>> [/bold green]").strip()
    print()

    if "get " in choice:
        collection.manual_game_create(choice)
        main_menu()
    if "add " in choice:
        collection.user_add_game(choice)
        main_menu()
    elif "remove " in choice:
        collection.manual_game_remove(choice)
        main_menu()
    elif choice == "list":
        collection.list_games()
        main_menu()
    elif "search " in choice:
        collection.search_collection(choice)    
        main_menu()
    elif "export " in choice:
        export.csv_export(choice)
        main_menu()
    elif "import " in choice:
        export.csv_import(choice)
        main_menu()
    elif choice == "twitch":
        get_user_credentials()
        main_menu()    
    elif choice == "exit":
        print("Thank you for using GAME COLLECTR!")
        sys.exit

    else:
        print("That is not a valid request.")
        print()
        main_menu()

def game_table():
    table = Table(show_header=True, show_lines=True, header_style="bold magenta")
    table.add_column("Title", style="bold", width=12)
    table.add_column("Platform(s)")
    table.add_column("Developer", justify="left")
    table.add_column("Publisher", justify="left")
    table.add_column("Summary", justify="left", width=80)
    table.add_column("URL", justify="left", overflow="fold")
    return table