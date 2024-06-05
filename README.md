# Client Server App - SQlite

## Explanation
This program was restructured from "Client Server App - PostgreSQL" for using SQlite database.


## Overview

This is a simple application with a Server-Client connection using a SQlite database. It includes a connection pool for efficient connection management.
You can perform basic commands with the server (see the notes below).

## Features
- **"uptime** - server work time"
- **"info** - version of the server"
- **"help** - the list of available commands"
- **"stop** - stopping server and client"
- **"register** - allows to register new user"
- **"login** - allows to login"
- **"send** - allows to send a message"
- **"read** - allows to read your mailbox"
- **"delete(admin only)** - deletes user"
- **"show_all_u(admin only)** - shows all users"
- **"show_all_m(admin only)** - shows all messages"

## Installation

1. Clone the repository:

    ```bash
    https://github.com/grzesiek1201/ClientServerAppPostgresql.git
    ```

2. Navigate to the project directory:

    ```bash
    cd ClientServerAppPostgresql
    ```

3. Run the program:

    ```bash
    python main.py
    ```

## How to Use

1. When you start the program, you will need to either create a new user or log in if you have already registered.
2. Once logged in, you can use any of the available commands.

## Applied technologies and libraries
-  socket
-  json
-  sqlite3
-  json
-  threading
-  time
-  queue
  
## License

This project is open-source and available under the MIT License.
