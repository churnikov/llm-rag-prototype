# Select base image
FROM python:3.12-slim

# Create user name and home directory variables.
# The variables are later used as $USER and $HOME.
ENV USER=username
ENV HOME=/home/$USER

# Add user to system
RUN useradd -m -u 1000 $USER

# Set working directory (this is where the code should go)
WORKDIR $HOME/app

# Update system and install dependencies.
RUN apt-get update && apt-get install --no-install-recommends -y \
    build-essential \
    software-properties-common

# Copy requirements.txt and install packages listed there with pip (this will place the files in home/username/)
COPY requirements.txt $HOME/app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy all files that are needed for your app to run with the directory structure as your files expect
COPY main.py $HOME/app/main.py
COPY start-script.sh $HOME/app/start-script.sh

# Give access to appripriate files and folders to the created user
RUN chmod +x start-script.sh \
    && chown -R $USER:$USER $HOME \
    && rm -rf /var/lib/apt/lists/*

USER $USER
EXPOSE 8000

ENTRYPOINT ["./start-script.sh"]