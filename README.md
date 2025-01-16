# Google Dorking Tool

This is a Python-based Google Dorking tool that searches for various sensitive files and information exposed on websites using Google search queries. The tool scrapes Google search results directly (no API required) and checks the status of files found, such as configuration files, backup files, database dumps, etc. 

**Important**: Always use this tool ethically and ensure that you have permission to scan the websites you're targeting. Unauthorized scanning of websites could be considered illegal or unethical.

## Features

- Searches for common exposed files and sensitive information using predefined Google dork queries.
- Scrapes Google search results using Python `requests` and `BeautifulSoup` libraries.
- Checks the HTTP status and file size of the found URLs.
- Supports searching for a single site or a list of sites.
- Customizable with new Google dork queries.

## Installation

### Requirements

- Python 3.x
- `requests` library
- `beautifulsoup4` library

### Install dependencies

You can install the required dependencies by running:

```bash
pip install -r requirements.txt
