FROM python:3.9

# Pull the base docker image of python with tag 3.9.6

WORKDIR /Assignment-01
# Change the working dir inside the container - cd /app (as workdir is inside container)

COPY ./ ./

# Copy main.py as source code and req.txt as dependency ( into the workdir which is inside container)
RUN python3 -m pip install --upgrade pip
RUN pip3 install --no-cache-dir -r requirements.txt
RUN pip3 install -e .

EXPOSE 8080
CMD ["streamlit", "run", "ui/main.py", "--server.port", "8080"]
