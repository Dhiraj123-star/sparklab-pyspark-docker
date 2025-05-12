# Base Python image
FROM python:3.11-slim

# Install OpenJDK 17 (required for PySpark)
RUN apt-get update && apt-get install -y openjdk-17-jdk && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Set environment variables for Java
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV PATH="$JAVA_HOME/bin:$PATH"

# Install Python dependencies
COPY app/requirements.txt /tmp/
RUN pip install --upgrade pip && pip install -r /tmp/requirements.txt

# Copy application code
COPY app /app
WORKDIR /app

# Run the PySpark app
CMD ["python", "main.py"]
