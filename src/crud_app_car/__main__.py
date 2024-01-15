import argparse

from crud_app_car.auth import is_logged_in, login, logout
from crud_app_car.db import add_song_to_db, connect_to_database, db_sync, search_song_by


def main():
    # Use argparser to create the CLI for the application
    # It uses a subparser to separate the 4 parts of CRUD
    parser = argparse.ArgumentParser(description="CRUD operations over a music DB")
    # Alternatively, you can add here global parameters for login the user
    subparsers = parser.add_subparsers(help="Subcommands", dest="command")

    # Subparser for the 'login' command
    login_parser = subparsers.add_parser('login', help='Login to the DB')
    login_parser.add_argument('--user', help='User to autheticate as', required=True)
    # A password should probably be provided
    
    # Subparser for the 'logout' command
    logout_parser = subparsers.add_parser('logout', help='Logout of the DB')

    # Subparser for the 'create' command
    create_parser = subparsers.add_parser('create', help='Add a song to the DB')
    create_parser.add_argument('--song', help='Name of the song', required=True)
    create_parser.add_argument('--album', help="Name of the album", required=True)
    create_parser.add_argument('--artist', help="Name of the artist", required=True)
    create_parser.add_argument('--genre', help="Name of the genre", required=True)
    create_parser.add_argument('--release_date', help="Release date of the song", default=None, required=False)

    # Subparser for the 'search' command
    search_parser = subparsers.add_parser('search', help='Search in the music db')
    search_parser.add_argument('--song', help='Name of the song', default=None)
    search_parser.add_argument('--artist', help='Name of the artist', default=None)
    

    # Parse the args
    args = parser.parse_args()
    
    # Ensure we are connected to the database
    connect_to_database()

    match args.command:
        case "login":
            login(user=args.user)
        case "logout":
                logout()
        case "create":
            if not is_logged_in():
                print("Please login using the login subcommand")
                exit()
            add_song_to_db(args.song, args.album, args.artist, args.genre, args.release_date)
            print("Success! Song inserted into DB")
        case "search":
            print(search_song_by(args.song, args.artist))
        case _:
            parser.print_help()

    # Sync any possible changes with the database
    db_sync()

if __name__ == '__main__':
    main()
