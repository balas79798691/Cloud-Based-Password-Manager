# Cloud Password Manager - Backend

## Run
1. Install Python 3.10+.
2. `pip install -r requirements.txt`
3. From the project root, run `python backend/app.py`.

The API runs at `http://127.0.0.1:5000`.

For a real cloud deployment, move the database and encryption key to managed/secret infrastructure and never commit `secret.key` or production credentials.
