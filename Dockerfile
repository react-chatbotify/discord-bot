# Use the official Python slim image
FROM python:3.13-slim

# Set the working directory inside the container
WORKDIR /app

# Copy only the requirements first (for better caching)
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the entire bot project into the container
COPY . .

# Set the working directory inside the src directory
WORKDIR /app/src

# Run the app
CMD ["python", "-m", "bot.main"]