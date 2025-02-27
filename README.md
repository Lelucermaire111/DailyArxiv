# arXiv Daily Alert - Keyword-based Semantic Communications Paper Notifier

This Python script queries the latest papers from **arXiv**, filtering them based on specific keywords (e.g., "Semantic Communications"). It sends an email with clickable links to the relevant papers published in the last 24 hours.

## Features

- **Keyword-based filtering**: Queries arXiv using specified keywords in the title, abstract, or metadata (using the `AND` relationship between keywords).
- **Time-based filtering**: Retrieves papers that were submitted in the last 24 hours (UTC).
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
