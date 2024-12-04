FROM python:3.11

# Set the working directory inside the container
WORKDIR /app

# Set environment variables to avoid interactive prompts during installation
ENV DEBIAN_FRONTEND=noninteractive

# Update package list and install dependencies (including Stockfish)
RUN apt-get update && apt-get install -y \
    stockfish \                    
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies from requirements.txt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Set the environment variable to point to the Stockfish binary
ENV STOCKFISH_PATH=/usr/games/stockfish

# Set the environment variable with the flag
ENV FLAG="wwf{y0u_4r3_4_tru3_ch355_m4st3r}"

# Copy the rest of the application code into the container
COPY server.py .

# Set the environment variable for Python (optional but recommended)
ENV PYTHONUNBUFFERED=1

# Command to run the Python application (replace 'app.py' with your script name)
CMD ["python", "server.py"]