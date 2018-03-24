# Start with the bleeding Edge!
FROM python:3.6

# Install Ghostscript so we can generate PDFs if needed
RUN apt-get update
RUN apt-get install -y ghostscript

# Install Python modules
WORKDIR /setup
COPY requirements.txt /setup
RUN pip install -r requirements.txt

# Copy source files into the container
COPY main.py /app/
COPY color_by_numbers /app/color_by_numbers/
WORKDIR /app

CMD ["bash"]
