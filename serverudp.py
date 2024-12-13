import socket
students_db = {}

def check_in(roll_no):
    if roll_no in students_db:
        return f"You are already here."
    students_db[roll_no] = 'Present'
    return f"Welcome Student {roll_no}"

def check_out(roll_no):
    # Check if the student has not checked in
    if roll_no not in students_db:
        return f"You didn’t check in today. Contact System Administrator."
    del students_db[roll_no]
    return f"Goodbye Student {roll_no}! Have a nice day."

def display_students():
    if students_db:
        print("\nCurrent Checked-in Students:")
        for roll_no in students_db:
            print(f" - {roll_no}")
    else:
        print("\nNo students are currently checked in.")

def main():
    # Define server address and port
    server_ip = '127.0.0.1'
    server_port = 2000
    try:
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_socket.bind((server_ip, server_port))
        print("Server socket created and bound.\nListening for messages...\n")
    except socket.error as err:
        print(f"Could not create or bind socket. Error: {err}")
        return

    while True:
        # Receive the message from the client
        try:
            client_message, client_address = udp_socket.recvfrom(2000)
            client_message = client_message.decode()
            print(f"Received Message from {client_address}: {client_message}")
        except socket.error as err:
            print(f"Receive Failed. Error: {err}")
            continue

        # Parse the message format YY-AAAA-CI/CO
        try:
            roll_no, action = client_message[:7], client_message[8:]
        except ValueError:
            udp_socket.sendto("Invalid message format.".encode(), client_address)
            continue

        # Process the message
        if action == "CI":
            response = check_in(roll_no)
        elif action == "CO":
            response = check_out(roll_no)
        else:
            response = "Invalid action. Use CI (Check-In) or CO (Check-Out)."

        # Send the response back to the client
        try:
            udp_socket.sendto(response.encode(), client_address)
        except socket.error as err:
            print(f"Send Failed. Error: {err}")

        # Print the list of students currently checked in
        display_students()

if __name__ == "__main__":
    main()