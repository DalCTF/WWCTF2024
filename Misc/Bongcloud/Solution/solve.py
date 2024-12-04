from stockfish import Stockfish
import socket


def read(s) -> str:
    response = s.recv(1024).decode("utf-8")
    return response


def read_line(s) -> str:
    data = b""
    while True:
        chunk = s.recv(1)  # Receive one byte at a time
        if not chunk:
            break  # Connection closed or no more data
        data += chunk
        if chunk == b"\n":  # End of line
            break

    line = data.decode("utf-8").strip()
    return line


def send(s, msg):
    s.sendall(msg.encode("utf-8"))


def game(s):
    while True:
        line = read_line(s)
        while not stockfish.is_fen_valid(line):
            if line.startswith("Wow"):
                read_line(s)
                send(s, "\n")
                print("Game won")
                return

            line = read_line(s)
        fern = line

        read_line(s)  # Read 'Your Move'

        stockfish.set_fen_position(fern)
        move = stockfish.get_best_move()
        send(s, move + "\n")


stockfish = Stockfish(path="/opt/homebrew/bin/stockfish")

HOST = "127.0.0.1"  # Netcat server address (change as needed)
PORT = 1337  # Netcat server port (change as needed)

# Create a TCP/IP socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # Connect to the server
    s.connect((HOST, PORT))
    print(f"Connected to {HOST} on port {PORT}")

    read(s)
    send(s, "\n")

    print("Playing Game 1")
    game(s)

    print("Playing Game 2")
    game(s)

    print("Playing Game 3")
    game(s)

    line = read_line(s)
    while "wwf" not in line:
        line = read_line(s)
    print(line)
