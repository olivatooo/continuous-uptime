FROM ubuntu:22.04

# Install required packages
RUN apt-get update && apt-get install -y \
    lib32gcc-s1 \
    curl \
    python3 \
    python3-pip \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install SteamCMD
RUN mkdir -p /opt/steamcmd && \
    cd /opt/steamcmd && \
    curl -sqL "https://steamcdn-a.akamaihd.net/client/installer/steamcmd_linux.tar.gz" | tar zxvf - && \
    chmod +x steamcmd.sh && \
    ./steamcmd.sh +quit && \
    ln -s steamcmd.sh steamcmd

# Add steamcmd to PATH
ENV PATH="/opt/steamcmd:${PATH}"

# Copy project files
WORKDIR /app
COPY *.py ./
COPY requirements.txt ./

# Install Python dependencies
RUN pip3 install -r requirements.txt

# Set default command
CMD ["python3", "main.py"]
