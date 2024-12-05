# Use official Node.js image as a base image
FROM node:18-buster

# Set the working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json first for caching dependencies
COPY package*.json ./

# Install Node.js dependencies (including express and happy-dom)
RUN npm install

# Copy the rest of the application files
COPY api.js .

# Copy the file with the flag
COPY flag.txt /

# Expose the port the app will run on
EXPOSE 3000

# Command to start the Express server
CMD ["npm", "start"]
