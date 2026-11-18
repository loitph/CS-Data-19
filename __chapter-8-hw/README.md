# Reward Data Analysis

Loads `data/du_lieu_giai_thuong.xlsx` into MySQL and runs analysis queries on it.

## Requirements

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (runs MySQL)
- Python 3.15 or newer

## Setup (first time only)

Run every command from this folder (`__chapter-8-hw`).

**1. Create the config file and set a password**

```bash
cp .env.example .env
```

Open `.env` and change `DB_PASSWORD`. If port 3307 is already in use on your computer, change `DB_PORT` too (for example to `3308`).

**2. Start MySQL**

```bash
docker compose up -d --wait
```

This creates the MySQL container and the `Reward` database. Your data is kept in a Docker volume, so it survives restarts.

**3. Create a virtual environment and install packages**

macOS / Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirement.txt
```

Windows (PowerShell):

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirement.txt
```

## Run the app

```bash
python main.py
```
