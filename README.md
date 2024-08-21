# Faraday Backend

## Installation

**Important:** Faraday relies on a environment variable `FARADAY_DATABASE_URL`. This _must_ be set or Faraday will not work. The environment variable takes the form of `sqlite://[YOUR URL HERE]`.

I use turso for the mainserver backend because it's free and ThePrimeagean.

### Docker

To run as a docker image run the following commands:

```bash
git clone https://github.com/Faraday-PM/Faraday-backend
cd Farday-backend
docker compose up
# "docker compose -d" to run in background
```

### From Source

To run from source run the following commands

```bash
git clone https://github.com/Faraday-PM/Faraday-backend
cd Faraday-backend
python3 -m virtualenv .venv
# Linux/Mac
.venv/bin/activate
# Windows
. ./venv/Scripts/activate
pip3 install -r requirements.txt
# Linux
source run.sh
# Windows
./run.bat
```
