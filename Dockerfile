# Start with the bleeding Edge!
FROM python:3.6

# Install Python modules
WORKDIR /setup
COPY requirements.txt /setup
RUN pip install -r requirements.txt

# This will be mounted as a volume
WORKDIR /app

# Install Ghostscript so we can generate PDFs if needed
RUN apt-get update
RUN apt-get install -y ghostscript

CMD ["bash"]
