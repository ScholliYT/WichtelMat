FROM python:3.7-alpine

# Install python packages via pip
COPY requirements.txt ./
RUN  pip install --no-cache-dir -r requirements.txt

# Copy src files
WORKDIR /app
COPY server_rest.py /app/server_rest.py

# start the webserver
ENTRYPOINT [ "python" ]
CMD [ "/app/server_rest.py" ]
