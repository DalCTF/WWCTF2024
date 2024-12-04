import re
import socket
import threading

import chess
import chess.engine
import os

FLAG = os.environ["FLAG"]
HOST = "0.0.0.0"
PORT = 1337


def visual(board: chess.Board) -> bytes:
    chess_pieces = {
        "K": "♔",
        "Q": "♕",
        "R": "♖",
        "B": "♗",
        "N": "♘",
        "P": "♙",
        "k": "♚",
        "q": "♛",
        "r": "♜",
        "b": "♝",
        "n": "♞",
        "p": "♟",
    }

    flipped_board = board.transform(chess.flip_vertical)
    lines = str(flipped_board).splitlines()
    new_lines = ["\n"]

    for i, line in enumerate(lines):
        line = re.sub("([a-zA-z.]) +", "\\1", line)
        new_line = ""

        for j, piece in enumerate(line):
            if piece in "12345678":
                new_line += f"   {piece}"
            elif (i + j) % 2 == 0:  # White square
                new_line += f"\033[48;5;255m {chess_pieces.get(piece, ' '):<2}\033[0m"
            else:  # Black square
                new_line += f"\033[48;5;235m {chess_pieces.get(piece, ' '):<2}\033[0m"

        new_line += f"   {i+1}"
        new_lines.append(new_line)
    new_lines.append("")
    new_lines.append(" a  b  c  d  e  f  g  h  ")
    new_lines.append("")

    return "\n".join(new_lines).encode()


def make_move(board: chess.Board, move: str | chess.Move) -> bool:
    try:
        if type(move) is str:
            board.push_san(move.strip())
            return True

        if type(move) is chess.Move:
            board.push(move)
            return True

        return False
    except ValueError as e:
        print("Couldn't make move:", e)
        return False


def game(client: socket.socket, address):
    print(f"New connection from {address}")

    start_string = "\nBongcloud\n=========\n\nYou will challenge the master chess bot in three games.\nIf you manage to beat it, you will be rewarded.\n\nGood luck!\n\nPress [ENTER] to continue\n"
    client.sendall(start_string.encode())
    _ = client.recv(1024)

    for i in range(3):
        client.sendall(f"Starting game {i+1}\n".encode())

        with chess.engine.SimpleEngine.popen_uci(os.environ["STOCKFISH_PATH"]) as bot:
            bot.configure({"Skill Level": 5})
            board = chess.Board()

            opening = ["e4", "Ke2"]
            game_running = True
            game_won = False

            try:
                while game_running:
                    if board.is_game_over():
                        game_running = False
                        if board.result() == "0-1":
                            client.sendall("\nWow, you won!\n\n".encode())
                            game_won = True
                            break
                        else:
                            client.sendall("\nYou didn't win!\n\n".encode())
                            game_won = False
                            break

                    move = (
                        opening.pop(0)
                        if len(opening) > 0
                        else bot.play(board, chess.engine.Limit(time=0.5)).move
                    )

                    if not make_move(board, move):
                        print("Failed to make move", move, "from", board.fen())
                        exit(1)

                    fen = board.fen()
                    print(fen)

                    client.sendall(visual(board))
                    client.sendall(f"\n{fen}\n\n> ".encode())

                    while True:
                        move = client.recv(1024).decode()

                        if not move:
                            print(f"Client {address} disconnected.")
                            game_running = False
                            break

                        if make_move(board, move):
                            break

                        client.sendall("\nInvalid move.\n\n> ".encode())

            except Exception as e:
                print(f"Error handling client {address}: {e}")
                game_won = False

            if not game_won:
                break

    if game_won:
        client.sendall(
            f"You are a true chess master!\nHere's your reward: {FLAG}".encode()
        )

    client.close()


def start():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_socket.bind((HOST, PORT))
    server_socket.listen(5)

    print(f"Server listening on {HOST}:{PORT}...")

    while True:
        client_socket, client_address = server_socket.accept()

        client_thread = threading.Thread(
            target=game, args=(client_socket, client_address)
        )
        client_thread.daemon = True  # Allow threads to exit when the main program exits
        client_thread.start()


if __name__ == "__main__":
    start()
