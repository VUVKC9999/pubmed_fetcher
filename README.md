# PubMed Fetcher

## Overview
This tool fetches research papers from PubMed based on a user-specified query, filters those with at least one non-academic author, and saves the results as a CSV file.

## Features
- Fetches research papers from the PubMed API.
- Identifies papers with at least one author affiliated with a pharmaceutical/biotech company.
- Extracts key details: **PubMed ID, Title, Publication Date, Non-Academic Authors, Company Affiliations, Corresponding Author Email**.
- Saves results as a **CSV file**.
- Command-line interface with **debugging and file output options**.

## Installation
### Prerequisites
Ensure you have **Python 3.8+** and **Poetry** installed.

### Clone the Repository
```sh
git clone https://github.com/yourusername/pubmed_fetcher.git
cd pubmed_fetcher
```

### Install Dependencies
```sh
poetry install
```

## Usage
### Running the Script
```sh
poetry run get-papers-list "cancer treatment"
```

### Command-Line Options
| Option        | Description |
|--------------|-------------|
| `-f` or `--file` | Specify the output filename (default: `papers.csv`). |
| `-d` or `--debug` | Enable debug mode for verbose logging. |

Example with a custom filename:
```sh
poetry run get-papers-list "diabetes" -f results.csv
```

## Environment Variables
To use an API key, create a `.env` file in the project directory:
```env
PUBMED_API_KEY=your_api_key_here
```

## Development
### Running Tests
```sh
poetry run pytest
```

## License
MIT License

