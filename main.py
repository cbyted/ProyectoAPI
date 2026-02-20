#!/usr/bin/env python3
from API.api import connect_to_api
from UI.ui import banner
from UI.ui import UserInterface

def main():
    banner()
    client  = connect_to_api()
    app = UserInterface(client)
    app.run()

if __name__ == "__main__":
    main()