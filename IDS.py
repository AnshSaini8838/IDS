from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
import tempfile

class MyHandler(FTPHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.failed_attempts = {}

    def on_login(self, username):
        client_address = self.remote_ip
        attempts = self.failed_attempts.get(client_address, 0)
        entered_username = self.username
        entered_password = self.password

        if username == entered_username:
            if entered_password == "":  # Replace with the correct password
                print(f"Login successful! Redirecting {client_address} to the fake FTP server.")
                # Add your notification mechanism here for successful redirection
                
                # Redirect the client to another IP (fake FTP server) upon successful login
                self.respond('220 Redirecting to fake FTP server\r\n')
                

def start_ftp_server(username, password):
    authorizer = DummyAuthorizer()
    temp_dir = tempfile.mkdtemp()  # Create a temporary directory
    authorizer.add_user(username, password, homedir=temp_dir, perm="elradfmw")  # Use the temporary directory
    
    handler = MyHandler
    handler.authorizer = authorizer
    handler.username = username
    handler.password = password

    server = FTPServer(("0.0.0.0", 21), handler)
    server.serve_forever()

entered_username = input("Enter the desired username: ")
entered_password = input("Enter the desired password: ")
start_ftp_server(entered_username, entered_password)
