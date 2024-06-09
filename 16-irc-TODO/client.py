from utils import IRCClient
import threading

# Replace the following values with your own
server = 'irc.dal.net'
port = 6667
nickname = 'seanm6534'
realname = 'YourRealname'
channel = '#Users'
# password = 'YourServerPassword'  # If required for server registration

client = IRCClient(server, port, nickname, realname, channel)
client.connect()

# Run the client to receive messages
thread = threading.Thread(target=client.run)
thread.start()

# Register your nickname with NickServ
client.send("PRIVMSG NickServ :REGISTER YourPassword YourEmail")

# Wait for registration confirmation and handle any challenges if needed

# Join the channel after registration
client.send(f"JOIN {channel}")

# Example: Sending a message after joining the channel
client.send_message("Hello, everyone! I'm here.")

