# Social media post creator

Simple tool powered by AI to help create social media posts.

## How to run

First, create `.env` file base one `.env.example`.

### In Docker

```sh
docker compose up -d
docker exec social-media-post-creator-app python main.py
```

### Locally

```sh
export $(cat .env)
python -m venv .venv
source .venv/bin/activate
cd app
pip install -r requirements.txt
python main.py
deactivate
```
