FROM python:3.10-slim

# Install system deps
RUN apt-get update && apt-get install -y git espeak ffmpeg && rm -rf /var/lib/apt/lists/*

# Install Coqui TTS
RUN pip install --no-cache-dir TTS

# Set working directory
WORKDIR /app
COPY narration.txt .

# Script to generate TTS
RUN echo "from TTS.api import TTS\n\
text=open('narration.txt').read()\n\
tts=TTS('tts_models/en/jenny/jenny')\n\
tts.tts_to_file(text=text,file_path='narration.mp3')" > run_tts.py

CMD ["python", "run_tts.py"]
