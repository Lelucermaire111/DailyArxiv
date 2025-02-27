# arXiv Daily Alert

This Python script queries the latest papers from **arXiv**, filtering them based on specific keywords (e.g., "Semantic Communications"). It sends an email with clickable links to the relevant papers published in the last 5 days.

## Features

- **Keyword-based filtering**: Queries arXiv using specified keywords in the title, abstract, or metadata.
- **Time-based filtering**: Retrieves papers that were submitted in the last 5 days (UTC).
- **Email notification**: Sends an email with the latest matching papers, including clickable links and submission dates.

## Requirements

Before running the script, make sure you have the following Python packages installed:

- `requests`: Used to make HTTP requests to the arXiv API.
- `feedparser`: Parses the Atom feed returned by the arXiv API.
- `smtplib`: Used to send email via Gmail SMTP (comes pre-installed with Python).
- `datetime`: Used for managing and comparing submission dates.

To install the required libraries, run:

```bash
pip install requests feedparser
```

## Setup

1. Create a Gmail account (if you don't have one already) and enable two-factor authentication (2FA).

2. Generate an application-specific password from your Google account:
   - Go to Google Account > Security > App passwords.
   - Generate a password for "Mail" and use it in the script for GMAIL_PASS.

3. Update the configuration:
   - Replace ```your_gmail_account@gmail.com``` with your Gmail address.
   - Replace ```your_gmail_app_password_or_token``` with the app-specific password you generated from Google.
   - Replace ```recipient@example.com``` with the email address where you want to receive the notifications.
4. Keywords: Modify the ```KEYWORD``` to specify the terms you want to search for on arXiv.

## How to Run the Script

1. After making the necessary modifications to the script (especially updating the Gmail credentials and keywords), run the script using Python:

    ```bash
    python arxiv_alert.py
    ```

2. The script will:
   - Query the latest papers on arXiv based on your keywords.
   - Filter the results to include only papers submitted in the last 24 hours.
   - Send an email to the specified recipient with the clickable links to the latest papers.
  
3. You can also schedule this script to run automatically every day using a task scheduler (e.g., cron on Linux or Task Scheduler on Windows) to receive daily updates.
