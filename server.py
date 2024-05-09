import socket


class Server:
    def __init__(self, host, port, server_info, options, mailbox, db, connection_pool):
        self.host = host
        self.port = port
        self.server_info = server_info
        self.options = options
        self.mailbox = mailbox
        self.max_messages = 5
        self.max_message_length = 255
        self.db = db
        self.connection_pool = connection_pool

    class CommandError(Exception):
        pass

    def start(self):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind((self.host, self.port))
                s.listen()
                print(f"Server listening on {self.host}: {self.port}")
                while True:
                    try:
                        conn, addr = s.accept()
                        with conn:
                            print(f"Connected to {addr}")
                            while True:
                                data = conn.recv(1024).decode("utf-8")
                                if not data:
                                    break
                                response = self.handle_command(data, conn, addr)
                                if response is None:
                                    print("Disconnected")
                                    break
                                conn.sendall(response.encode("utf-8"))
                    except KeyboardInterrupt:
                        print("KeyboardInterrupt: Stopping server...")
                        break
                    except Exception as e:
                        print(f"Error accepting connection: {e}")
        except OSError as e:
            print(f"Error binding to address {self.host}: {self.port}: {e}")

    def handle_command(self, command, conn, addr):
        try:
            command_parts = command.split()
            if not command_parts:
                raise self.CommandError("Empty command")

            command_name = command_parts[0].lower()
            command_args = command_parts[1:]

            command_handlers = {
                "uptime": self.options.uptime,
                "info": self.options.info,
                "help": self.options.help,
                "register": self.options.register,
                "login": self.options.login,
                "send": self.options.send_message,
                "read": self.options.read_messages,
                "show_all_m": self.options.show_all_m,
                "show_all_u": self.options.show_all_u,
                "delete": self.options.delete_user,
                "stop": self.options.stop
            }

            handler = command_handlers.get(command_name)
            if not handler:
                raise self.CommandError("Unknown command")

            self.response = handler(*command_args)
            return self.response
        except Exception as e:
            return str(e)
