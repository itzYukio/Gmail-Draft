# Gmail Draft Automator

A simple Python script that automates the creation of email drafts in your Gmail account. 
It generates 100 random order numbers (in the format `XXX-XXXXXXX-XXXXXXX`) and creates a draft for each order, addressed to `ofm@amazon.in`.

## Prerequisites

- Python 3.x
- A Google Cloud Project with the **Gmail API** enabled.
- OAuth 2.0 Client credentials downloaded as `credentials.json`.

## Setup

1. Clone this repository.
2. Install the required dependencies:
   ```bash
   pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib
   ```
3. Place your `credentials.json` file in the root directory of the project.

## Usage

Run the script using Python:

```bash
python main.py
```

The first time you run the script, a browser window will open prompting you to log in with your Google account and grant permissions to create drafts. An authorization token will be saved to `token.json` for future runs.

## Important Note

For security reasons, **never** commit your `credentials.json` or `token.json` files to a public repository. They are ignored by the `.gitignore` file by default.