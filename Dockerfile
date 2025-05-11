# Use the official Python image
FROM mcr.microsoft.com/playwright/python:latest

# Set the working directory
WORKDIR /app

# Install system dependencies required by Playwright and browsers
RUN apt-get update && apt-get install -y \
    libnss3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libxcomposite1 \
    libxrandr2 \
    libxdamage1 \
    libxkbcommon0 \
    libgbm1 \
    libpango-1.0-0 \
    libasound2 \
    libwayland-client0 \
    libwayland-cursor0 \
    libwayland-egl1 \
    libxshmfence1 \
    libxcb-shm0 \
    libx11-xcb1 \
    libxcursor1 \
    libxfixes3 \
    libgtk-3-0 \
    libgdk-pixbuf2.0-0 \
    libpangocairo-1.0-0 \
    libcairo-gobject2 \
    libcairo2 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright and its browsers
RUN pip install playwright
RUN playwright install  --with-deps

# Copy the application code
COPY . .

# Expose the port the app runs on
#EXPOSE 8000

# Command to run the application
#CMD ["uvicorn", "Controller.resources:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

CMD sh -c "uvicorn Controller.resources:app \
    --host 0.0.0.0 \
    --port ${PORT} \
    --log-level info"
