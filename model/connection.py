import socket
import pickle

class Connection():
    def __init__(self):
        self.s_in = None
        self.s_out = None
        self.conn_in = None
        self.is_connected = False

    def get_socket_raw(self):
        data = self.conn_in.recv(1024)
        print(f"Read socket and got {data}")
        return data

    def get_socket_text(self):
        return self.get_socket_raw().decode("utf-8")

    def get_socket(self):
        return pickle.loads(self.get_socket_raw())
    
    def send_socket_raw(self, data):
        self.s_out.sendall(data)

    def send_socket_text(self, data):
        self.send_socket_raw(data.encode("utf-8"))

    def send_socket(self, data):
        self.send_socket_raw(pickle.dumps(data))
    
    def get_local_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip

    def get_partner_address(self):
        while(True):
            inpt = input("Are you the server or client? ").lower()
            if inpt == "server":
                return None
            elif inpt == "client":
                while(True):
                    inpt = input("What is your partners IP address? ")
                    confirmation = input(f"Would you like to connect to {inpt}? ")
                    if confirmation.lower() == "y" or confirmation.lower == "yes":
                        return inpt
                    else:
                        continue

    def connect(self):
        HOST = self.get_local_ip()
        PORT = 65432
        self.s_in = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s_in.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s_in.bind((HOST, PORT))
        self.s_in.listen(5)

        print(f"Your local ip is {HOST}")

        partner_address = self.get_partner_address()

        # TODO: This is unnecessarily complex. Just make them both type in the other person's local ip
        # Neither person is really the 'server' or 'client' in a meaningful capacity
        # However, it does make it easier to only input 1 address
        # I am the server, I dont know partners address
        if partner_address == None:
            # Constantly watch for incoming message and then grab its address
            print(f"Listening for connections on {self.s_in}")
            while(True):
                self.conn_in, addr_in = self.s_in.accept()
                print(f"Received connection: {self.conn_in}, {addr_in}")
                data = self.get_socket_text()
                print(f"Got the text {data}")
                # If not the correct code, close the connection and try again
                if data != "1989":
                    self.conn_in.close()
                    continue
                # If it is correct, save that address
                partner_address = addr_in[0]
                break
            # Setup an out socket to that address
            print("Setting up an out socket")
            self.s_out = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s_out.connect((partner_address, PORT))
            # Send something to that address so it knows I exist
            print("Sending a message to the out socket")
            self.send_socket_text("1991")
            print("Message sent to the out socket")
        else:
            # Setup an out socket to the user-provided address
            print("Setting up an out socket")
            self.s_out = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s_out.connect((partner_address, PORT))

            # Send something to that address so it knows I exist
            print("Sending a message to the out socket")
            self.send_socket_text("1989")
            print("Message sent to the out socket")

            # Constantly watch for a response to know we're able to communicate
            print(f"Listening for connections on {self.s_in}")
            while(True):
                self.conn_in, addr_in = self.s_in.accept()
                print(f"Received connection: {self.conn_in}, {addr_in}")
                data = self.get_socket_text()
                print(f"Got the text {data}")
                # If not the correct code, close the connection and try again
                if data != "1991":
                    self.conn_in.close()
                    continue
                break
        
        self.is_connected = True