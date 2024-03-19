

FROM python:3.8-slim-buster

# Install required packages for OpenCV
RUN apt-get update && apt-get install -y \
    mesa-utils \
    libgl1-mesa-glx \
    libgl1-mesa-dev \
    libglib2.0-dev \
    && rm -rf /var/lib/apt/lists/*
    
WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
