from python:slim

workdir /app
copy . /app

run apt-get update && \
    apt-get install -y ffmpeg

run pip install --upgrade pip
run pip install --no-cache-dir -r requirements.txt

run chmod +x SonOro.py
run chmod +x testModules.py

cmd ["python", "SonOro.py"]

ENTRYPOINT [ "/bin/sh", "-c", "if [ \"$1\" = \"test\" ]; then python testModules.py; else python SonOro.py; fi" ]