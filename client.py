import socket

def main():
    server_ip = '127.0.0.1'
    server_port = 2000
    
    try:
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print("Client socket created.")
    except socket.error as err:
        print(f"Could not create socket. Error: {err}")
        return

    while True:
        client_message = input("Enter your roll number and action (YY-AAAA-CI/CO): ")
        
        # Send the message to the server
        try:
            udp_socket.sendto(client_message.encode(), (server_ip, server_port))
        except socket.error as err:
            print(f"Send Failed. Error: {err}")
            continue

        # Receive the response from the server
        try:
            server_message, _ = udp_socket.recvfrom(2000)
            print(f"Server Response: {server_message.decode()}")
        except socket.error as err:
            print(f"Receive Failed. Error: {err}")

if __name__ == "__main__":
    main()