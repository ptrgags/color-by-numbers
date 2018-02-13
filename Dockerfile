# Start with the bleeding Edge!
# TODO: Can this be done with the slim version?
FROM python:3.6

# This will be mounted as a volume
WORKDIR /app

# This is easier than installing from source.
RUN pip install opencv-python

CMD ["bash"]
