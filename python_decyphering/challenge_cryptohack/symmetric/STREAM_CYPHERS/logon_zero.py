import json
from pwn import remote

# Configuration
HOST = "socket.cryptohack.org"
PORT = 13399
TOKEN = b"\x00" * 28


def create_command(option, **kwargs):
    """Create a JSON command for the server"""
    command = {"option": option}
    command.update(kwargs)
    return json.dumps(command).encode()


def send_and_receive(conn, command):
    """Send command and receive response"""
    conn.sendline(command)
    return conn.recvline().decode()


def attempt_authentication(conn, token):
    """Attempt to reset password and authenticate"""
    # Reset password with null token
    reset_password_cmd = create_command("reset_password", token=token.hex())
    send_and_receive(conn, reset_password_cmd)
    
    # Attempt authentication with empty password
    auth_cmd = create_command("authenticate", password="")
    response = send_and_receive(conn, auth_cmd)
    
    return response


def main():
    """Main exploit loop"""
    print(f"Connecting to {HOST}:{PORT}...")
    
    with remote(HOST, PORT) as conn:
        # Receive welcome message
        welcome = conn.recvline().decode()
        print(f"Server: {welcome}")
        
        reset_cmd = create_command("reset_connection")
        attempt = 0
        
        while True:
            attempt += 1
            
            # Try authentication
            response = attempt_authentication(conn, TOKEN)
            
            # Check if flag found
            if "crypto" in response:
                print(f"\n{'='*50}")
                print(f"Flag found after {attempt} attempts!")
                print(f"{'='*50}")
                print(response)
                break
            
            # Reset connection for next attempt
            send_and_receive(conn, reset_cmd)
            
            # Progress indicator
            if attempt % 10 == 0:
                print(f"Attempts: {attempt}...")


if __name__ == "__main__":
    main()