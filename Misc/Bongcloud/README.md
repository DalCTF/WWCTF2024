# Bongcloud

## Analysis

This problem gives us an endpoint to connect via `netcat`, that is, a persistent TCP connection. It starts by stating that we need to beat the chess bot three times to be considered the chess master and get our reward. What follows is a board of chess with a first move by the server already executed and a prompt for us to enter the our move. We always play from the perspective of blacks, and the system always opens with the Bongcloud opening (`e4`, `Ke2`).

## Solution

The first way to solve this problem is to actually play the games and beat the bot three times in a row. However, I couldn't play chess to save my life, so I employed _Stockfish_, an open-source chess bot, to play for me. This solution involves writing a script that connects to the server using sockets and reads the state of the board to feed to the bot. For every position, it calculates the appropriate move and sends it back to the server. Once it detects that a game has ended, it starts the next game from a blank board. The remainder of the code is used to identify the state of the game and to recognize when the flag (`wwf{...}`) is issued.