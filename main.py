import database
import navigation

# set up app
navigation.setup_app()

# initialise databse
database.create_db()

# launch main menu
navigation.print_logo()
navigation.get_user_credentials()
navigation.main_menu()